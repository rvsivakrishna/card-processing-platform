from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

CARD_PROCESSOR_URL = os.getenv(
    "CARD_PROCESSOR_URL",
    "http://card-processor-service:8080/process"
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
        response = requests.get(CARD_PROCESSOR_URL, timeout=5)
        return jsonify({
            "payment": "received",
            "processor_response": response.json()
        })
    except Exception as e:
        return jsonify({
            "status": "FAILED",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
