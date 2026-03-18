from flask import Flask, request
import os
import datetime
import requests

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")

def get_expiry():
    today = datetime.datetime.now()
    weekday = today.weekday()

    if weekday == 1:
        days = 7
    else:
        days = (1 - weekday) % 7

    expiry = today + datetime.timedelta(days=days)
    return expiry.strftime("%d %b").upper()

def get_strike():
    # simple approx
    return 23750

def place_order(symbol, side):
    url = "https://api.dhan.co/orders"

    headers = {
        "access-token": ACCESS_TOKEN,
        "client-id": CLIENT_ID,
        "Content-Type": "application/json"
    }

    payload = {
        "transactionType": side,
        "exchangeSegment": "NSE_FNO",
        "productType": "INTRADAY",
        "orderType": "MARKET",
        "quantity": 65,
        "tradingSymbol": symbol
    }

    r = requests.post(url, json=payload, headers=headers)
    return r.text

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    action = data.get("action")

    expiry = get_expiry()
    strike = get_strike()

    if action == "BUY_CE":
        symbol = f"NIFTY {expiry} {strike} CE"
        return place_order(symbol, "BUY")

    if action == "BUY_PE":
        symbol = f"NIFTY {expiry} {strike} PE"
        return place_order(symbol, "BUY")

    if action == "EXIT":
        return place_order("", "SELL")

    return "OK"

app.run(host="0.0.0.0", port=5000)
