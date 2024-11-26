import os
import requests
from flask import Flask, request
from telegram import Bot
from telegram.ext import CommandHandler, Updater

# Flask app setup
app = Flask(__name__)

# Telegram Bot API token and details
TELEGRAM_API_KEY = "7057865734:AAEBB12yJESX5sZ278UYumyectVPx3PuzpI"
bot = Bot(token=TELEGRAM_API_KEY)

# Cashfree API details
CASHFREE_APP_ID = "TEST1027828340bdc693b933350cd9b738287201"
CASHFREE_SECRET_KEY = "cfsk_ma_test_ee2923adec8914232ae79d9826252885_d6faea13"
CASHFREE_API_URL = "https://test.cashfree.com/api/v2/cftoken/order"

# Function to create dynamic payment link
def create_payment_link(amount):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        "order_amount": amount,
        "order_currency": "INR",
        "order_id": "order123",  # Make it dynamic or unique
        "customer_details": {
            "customer_id": "customer123",  # Unique customer ID
            "customer_email": "test@example.com",
            "customer_phone": "9876543210"
        },
        "return_url": "https://yourdomain.com/return",  # Replace with your domain URL
        "notify_url": "https://yourdomain.com/notify"  # Replace with your domain URL
    }

    response = requests.post(CASHFREE_API_URL, json=data, headers=headers, auth=(CASHFREE_APP_ID, CASHFREE_SECRET_KEY))

    if response.status_code == 200:
        result = response.json()
        payment_link = result.get("payment_link", "")
        return payment_link
    else:
        return "Error generating payment link"

# Flask route to handle webhook from Telegram
@app.route(f'/{TELEGRAM_API_KEY}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telegram.Update.de_json(json.loads(json_str), bot)
    
    # Command handler for /pay
    def pay(update, context):
        try:
            amount = 100  # Example amount
            payment_link = create_payment_link(amount)

            if payment_link:
                update.message.reply_text(f"Your payment link: {payment_link}")
            else:
                update.message.reply_text("Failed to generate payment link.")
        except Exception as e:
            update.message.reply_text(f"Error: {e}")
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("pay", pay))
    
    return "OK"

# Vercel specific: webhook for /webhook
@app.route('/')
def home():
    return "Telegram Bot is running!"

if __name__ == "__main__":
    # Set webhook with Telegram
    bot.set_webhook(url='https://your-vercel-app-url.com/' + TELEGRAM_API_KEY)
    
    app.run(debug=True)
