from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

CARD_PROCESSOR_URL = os.getenv(
    "CARD_PROCESSOR_URL",
    "http://card-processor-service:8080/process"
)

FRAUD_SERVICE_URL = os.getenv(
    "FRAUD_SERVICE_URL",
    "http://fraud-service:8081/fraud"
)

@app.route("/")
def home():
    return jsonify({
        "service": "Payment API",
        "status": "Running"
    })

@app.route("/payment")
def payment():
    try:
        # Step 1: Fraud Check
        fraud = requests.get(FRAUD_SERVICE_URL, timeout=5).json()

        decision = fraud["decision"]

        # Step 2: High Risk - Reject
        if decision == "BLOCK":
            return jsonify({
                "status": "DECLINED",
                "reason": "Fraud detected",
                "fraud": fraud
            }), 403

        # Step 3: Medium Risk - OTP Required
        elif decision == "REVIEW":
            return jsonify({
                "status": "PENDING_VERIFICATION",
                "message": "OTP verification required",
                "fraud": fraud
            }), 202

        # Step 4: Low Risk - Process Payment
        processor = requests.get(
            CARD_PROCESSOR_URL,
            timeout=5
        ).json()

        return jsonify({
            "status": "APPROVED",
            "payment": "received",
            "fraud": fraud,
            "processor_response": processor,
            "release": "Sprint-7"
        })

    except Exception as e:
        return jsonify({
            "status": "FAILED",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
