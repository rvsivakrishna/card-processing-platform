from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "service": "Fraud Service",
        "status": "Running"
    })


@app.route("/fraud")
def fraud_check():
    """
    Simulate a fraud decision.

    CLEAR  -> Safe transaction
    REVIEW -> Requires additional verification (OTP/MFA)
    BLOCK  -> High fraud risk
    """

    decision = random.choices(
        population=["CLEAR", "REVIEW", "BLOCK"],
        weights=[70, 20, 10],   # 70% low risk, 20% review, 10% blocked
        k=1
    )[0]

    if decision == "CLEAR":
        return jsonify({
            "decision": "CLEAR",
            "risk": "LOW",
            "score": random.randint(1, 40),
            "message": "Transaction approved for processing"
        })

    elif decision == "REVIEW":
        return jsonify({
            "decision": "REVIEW",
            "risk": "MEDIUM",
            "score": random.randint(41, 75),
            "message": "Additional verification required (OTP)"
        })

    else:
        return jsonify({
            "decision": "BLOCK",
            "risk": "HIGH",
            "score": random.randint(76, 100),
            "message": "Transaction blocked due to fraud risk"
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
