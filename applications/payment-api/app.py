import os
import uuid
import time
from datetime import datetime

import requests
from flask import Flask, jsonify, Response
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

app = Flask(__name__)

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

FRAUD_SERVICE_URL = os.getenv(
    "FRAUD_SERVICE_URL",
    "http://fraud-service:8081/fraud"
)

CARD_PROCESSOR_URL = os.getenv(
    "CARD_PROCESSOR_URL",
    "http://card-processor-service:8080/process"
)

AUDIT_SERVICE_URL = os.getenv(
    "AUDIT_SERVICE_URL",
    "http://audit-service:8082/audit"
)

DEFAULT_AMOUNT = 2500

RELEASE = "Sprint-11-Monitoring"

# ------------------------------------------------------------------
# Prometheus Metrics
# ------------------------------------------------------------------

PAYMENT_REQUESTS = Counter(
    "payment_requests_total",
    "Total number of payment requests"
)

PAYMENT_STATUS = Counter(
    "payment_status_total",
    "Total payments by final status",
    ["status"]
)

PAYMENT_RISK = Counter(
    "payment_risk_total",
    "Total payments by fraud risk level",
    ["risk"]
)

PAYMENT_ERRORS = Counter(
    "payment_errors_total",
    "Total number of payment processing errors",
    ["type"]
)

PAYMENT_DURATION = Histogram(
    "payment_request_duration_seconds",
    "Payment request processing duration in seconds"
)

# ------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------

def generate_transaction_id():
    return (
        "TXN-"
        + datetime.now().strftime("%Y%m%d%H%M%S")
        + "-"
        + str(uuid.uuid4())[:6].upper()
    )


def check_fraud():
    response = requests.get(
        FRAUD_SERVICE_URL,
        timeout=5
    )

    response.raise_for_status()

    return response.json()


def process_card():
    response = requests.get(
        CARD_PROCESSOR_URL,
        timeout=5
    )

    response.raise_for_status()

    return response.json()


def send_audit(transaction, amount, risk, status):

    payload = {
        "transaction": transaction,
        "amount": amount,
        "risk": risk,
        "status": status,
        "release": RELEASE
    }

    try:

        requests.post(
            AUDIT_SERVICE_URL,
            json=payload,
            timeout=5
        )

    except Exception as e:
        print("Audit Service Error:", e)


# ------------------------------------------------------------------
# Health Endpoints
# ------------------------------------------------------------------

@app.route("/")
def index():

    return jsonify({
        "service": "Payment API",
        "status": "Running",
        "release": RELEASE
    })


@app.route("/health")
def health():

    return jsonify({
        "service": "Payment API",
        "status": "Running",
        "release": RELEASE
    })


# ------------------------------------------------------------------
# Prometheus Metrics Endpoint
# ------------------------------------------------------------------

@app.route("/metrics")
def metrics():

    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


# ------------------------------------------------------------------
# Payment Endpoint
# ------------------------------------------------------------------

@app.route("/payment")
def payment():

    PAYMENT_REQUESTS.inc()

    start_time = time.time()

    try:

        transaction = generate_transaction_id()

        amount = DEFAULT_AMOUNT

        fraud = check_fraud()

        risk = fraud.get("risk", "UNKNOWN")

        PAYMENT_RISK.labels(risk=risk).inc()

        # ----------------------------------------------------------
        # HIGH RISK
        # ----------------------------------------------------------

        if risk == "HIGH":

            PAYMENT_STATUS.labels(status="DECLINED").inc()

            send_audit(
                transaction,
                amount,
                risk,
                "DECLINED"
            )

            return jsonify({

                "transaction": transaction,

                "status": "DECLINED",

                "reason": "Fraud detected",

                "fraud": fraud,

                "release": RELEASE

            })

        # ----------------------------------------------------------
        # MEDIUM RISK
        # ----------------------------------------------------------

        if risk == "MEDIUM":

            PAYMENT_STATUS.labels(
                status="PENDING_VERIFICATION"
            ).inc()

            send_audit(
                transaction,
                amount,
                risk,
                "PENDING_VERIFICATION"
            )

            return jsonify({

                "transaction": transaction,

                "status": "PENDING_VERIFICATION",

                "otp_required": True,

                "fraud": fraud,

                "release": RELEASE

            })

        # ----------------------------------------------------------
        # LOW RISK
        # ----------------------------------------------------------

        processor = process_card()

        PAYMENT_STATUS.labels(status="APPROVED").inc()

        send_audit(
            transaction,
            amount,
            risk,
            "APPROVED"
        )

        return jsonify({

            "transaction": transaction,

            "payment": "received",

            "status": "APPROVED",

            "fraud": fraud,

            "processor_response": processor,

            "release": RELEASE

        })

    except requests.exceptions.RequestException as e:

        PAYMENT_STATUS.labels(status="FAILED").inc()

        PAYMENT_ERRORS.labels(
            type="dependency_error"
        ).inc()

        return jsonify({

            "status": "FAILED",

            "error": str(e),

            "release": RELEASE

        }), 500

    except Exception as e:

        PAYMENT_STATUS.labels(status="FAILED").inc()

        PAYMENT_ERRORS.labels(
            type="application_error"
        ).inc()

        return jsonify({

            "status": "FAILED",

            "error": str(e),

            "release": RELEASE

        }), 500

    finally:

        PAYMENT_DURATION.observe(
            time.time() - start_time
        )


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8080
    )
