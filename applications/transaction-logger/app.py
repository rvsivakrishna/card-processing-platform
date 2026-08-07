from flask import Flask
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "/data/transactions.log"


@app.route("/log")
def log_transaction():

    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} PAYMENT RECEIVED\n")

    return {
        "status": "logged"
    }


@app.route("/history")
def history():

    try:
        with open(LOG_FILE) as f:
            return "<pre>" + f.read() + "</pre>"

    except FileNotFoundError:
        return "No Transactions"
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
