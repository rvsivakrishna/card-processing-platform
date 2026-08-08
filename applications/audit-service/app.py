from flask import Flask, request, jsonify
from datetime import datetime, timezone
import os
import pymysql

app = Flask(__name__)

MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql-service")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "auditdb")
MYSQL_USER = os.getenv("MYSQL_USER", "audituser")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")


def get_db_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route("/health")
def health():
    return jsonify({
        "service": "Audit Service",
        "status": "Running"
    })


@app.route("/audit", methods=["POST"])
def audit():
    data = request.get_json()

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "transaction": data.get("transaction"),
        "status": data.get("status"),
        "risk": data.get("risk"),
        "amount": data.get("amount")
    }

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO transactions
                (timestamp, transaction_id, status, risk, amount)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    entry["timestamp"],
                    entry["transaction"],
                    entry["status"],
                    entry["risk"],
                    entry["amount"]
                )
            )

        connection.commit()

    finally:
        connection.close()

    return jsonify({
        "message": "Audit record stored",
        "transaction": entry["transaction"]
    })


@app.route("/history")
def history():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    timestamp,
                    transaction_id AS transaction,
                    status,
                    risk,
                    amount
                FROM transactions
                ORDER BY id ASC
                """
            )

            records = cursor.fetchall()

    finally:
        connection.close()

    return jsonify(records)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
