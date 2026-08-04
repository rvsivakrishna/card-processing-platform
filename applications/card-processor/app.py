from flask import Flask, jsonify
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "service": "Card Processor",
        "hostname": socket.gethostname()
    })

@app.route("/process")
def process():

    return jsonify({

        "transaction": "APPROVED",

        "authorization": "SUCCESS",

        "hostname": socket.gethostname()

    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
