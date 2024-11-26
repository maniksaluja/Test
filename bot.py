import threading
from flask import Flask, request
import json
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import datetime
import requests

app = Flask(__name__)

# Flask endpoint for payment status
@app.route('/payment-status', methods=['POST'])
def payment_status():
    data = request.get_json()
    if data.get('status') == 'SUCCESS':
        print("Payment successful")
    else:
        print("Payment failed or pending")
    return json.dumps({"status": "success"}), 200

# Cashfree and Telegram Bot Credentials
APP_ID = "73553954db925af2b456a26e07935537"
SECRET_KEY = "cfsk_ma_prod_2d76755985f4b26b8a93f770157c6514_167eab6c"
BOT_TOKEN = "7341469021:AAFKFWX__rS5Et-Qco1ATpeA7EU92js3Pc0"
WEBHOOK_URL = "http://154.12.228.186:5001/payment-status"

# Webhook call function
def send_payment_status_to_webhook(status: str):
    payload = {"status": status}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    if response.status_code == 200:
        print("Webhook called successfully")
    else:
        print(f"Error in calling webhook: {response.text}")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Welcome! Use /pay to generate a payment link for INR 2."
    )

async def generate_payment_link(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    customer_details = {
        "customer_id": str(user.id),
        "customer_email": "maniksaluja2004@gmail.com",
        "customer_phone": "8708366003"
    }
    order_id = f"ORDER_{user.id}_{int(datetime.datetime.now().timestamp())}"
    order_amount = 2
    expiry_time = (datetime.datetime.now() + datetime.timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%S+05:30")

    payload = {
        "customer_details": customer_details,
        "order_id": order_id,
        "order_amount": order_amount,
        "order_currency": "INR",
        "order_expiry_time": expiry_time,
        "version": "2023-08-01"
    }

    url = "https://api.cashfree.com/pg/links"
    headers = {
        "Content-Type": "application/json",
        "x-client-id": APP_ID,
        "x-client-secret": SECRET_KEY,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            payment_link = response.json().get("data", {}).get("link_url", "")
            await update.message.reply_text(f"Here is your payment link (valid for 20 minutes):\n{payment_link}")
            send_payment_status_to_webhook("SUCCESS")
        else:
            await update.message.reply_text(f"Error: {response.text}")
            send_payment_status_to_webhook("FAILED")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pay", generate_payment_link))
    await application.run_polling()

def run_flask():
    app.run(host='0.0.0.0', port=5001)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
