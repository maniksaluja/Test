import requests
import telegram
import logging
import asyncio
from flask import Flask, request
from telegram import Bot
import json

# Replace with your actual Telegram API Key
TELEGRAM_API_KEY = '7057865734:AAEBB12yJESX5sZ278UYumyectVPx3PuzpI'
bot = Bot(token=TELEGRAM_API_KEY)

# Cashfree API details
CASHFREE_APP_ID = "TEST1027828340bdc693b933350cd9b738287201"
CASHFREE_SECRET_KEY = "cfsk_ma_test_ee2923adec8914232ae79d9826252885_d6faea13"
CASHFREE_API_URL = "https://test.cashfree.com/api/v2/cftoken/order"

# Enable logging for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)

# Function to set webhook asynchronously
async def set_webhook():
    await bot.set_webhook(url=f'https://154.12.228.186/{TELEGRAM_API_KEY}')

# Run the webhook function
def start_webhook():
    asyncio.run(set_webhook())

# Function to create dynamic payment link
def create_payment_link(amount):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        "order_amount": amount,
        "order_currency": "INR",
        "order_id": "order123",  # Unique order ID
        "customer_details": {
            "customer_id": "customer123",
            "customer_email": "test@example.com",
            "customer_phone": "9876543210"
        },
        "return_url": "https://yourdomain.com/return",  # You can use any placeholder URL here
        "notify_url": "https://yourdomain.com/notify"  # Placeholder URL
    }

    response = requests.post(CASHFREE_API_URL, json=data, headers=headers, auth=(CASHFREE_APP_ID, CASHFREE_SECRET_KEY))

    if response.status_code == 200:
        result = response.json()
        payment_link = result.get("payment_link", "")
        return payment_link
    else:
        return "Error generating payment link"

# Function to handle /pay command
@app.route(f'/{TELEGRAM_API_KEY}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telegram.Update.de_json(json.loads(json_str), bot)

    # Check if the message is a /pay command
    if update.message.text == "/pay":
        try:
            amount = 100  # Example amount
            payment_link = create_payment_link(amount)

            if payment_link:
                update.message.reply_text(f"Your payment link: {payment_link}")
            else:
                update.message.reply_text("Failed to generate payment link.")
        except Exception as e:
            logger.error(f"Error in /pay command: {e}")
            update.message.reply_text(f"Error: {e}")
    return "OK"

# Root route to check if server is up
@app.route('/')
def hello_world():
    return 'Telegram Bot Webhook is Set Successfully!'

if __name__ == "__main__":
    # Set webhook with Telegram bot
    start_webhook()

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
