from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
CLIENT_ID = os.environ.get("CLIENT_ID")

DHAN_URL = "https://api.dhan.co/orders"

def place_order(option_type):
    payload = {
        "dhanClientId": CLIENT_ID,
        "transactionType": "BUY",
        "exchangeSegment": "NSE_FNO",
        "productType": "INTRADAY",
        "orderType": "MARKET",
        "validity": "DAY",
        "securityId": "NIFTY",  # temporary
        "quantity": 65
    }

    headers = {
        "access-token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    print("Sending order to Dhan:", payload)

    response = requests.post(DHAN_URL, json=payload, headers=headers)

    print("Dhan response:", response.text)

    return response.text


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Received:", data)

    action = data.get("action")

    if action == "BUY_CE":
        return place_order("CE")

    elif action == "BUY_PE":
        return place_order("PE")

    elif action == "EXIT":
        return jsonify({"status": "exit received"})

    return jsonify({"error": "invalid action"})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
