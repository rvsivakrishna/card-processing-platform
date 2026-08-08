from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

AUDIT_FILE = "/data/audit.log"


@app.route("/health")
def health():
    return jsonify({
        "service": "Audit Service",
        "status": "Running"
    })


@app.route("/audit", methods=["POST"])
def audit():

    data = request.json

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "transaction": data.get("transaction"),
        "status": data.get("status"),
        "risk": data.get("risk"),
        "amount": data.get("amount")
    }

    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return jsonify({
        "message": "Audit record stored"
    })


@app.route("/history")
def history():

    if not os.path.exists(AUDIT_FILE):
        return jsonify([])

    records = []

    with open(AUDIT_FILE) as f:
        for line in f:
            records.append(json.loads(line))

    return jsonify(records)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
