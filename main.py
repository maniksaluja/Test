import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import json
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Cashfree API credentials (Test)
api_key = 'TEST1027828340bdc693b933350cd9b738287201'  # Cashfree AppID
api_secret = 'cfsk_ma_test_ee2923adec8914232ae79d9826252885_d6faea13'  # Cashfree Secret Key
api_url = 'https://testapi.cashfree.com/api/v2/cft/payment-links'

# Function to generate payment link
def generate_payment_link():
    payment_data = {
        "order_id": "order_" + str(int(time.time())),  # Unique order ID
        "order_amount": 2,  # ₹2
        "order_currency": "INR",
        "order_note": "Payment for testing",
        "customer_email": "customer@example.com",  # Change as needed
        "customer_phone": "9999999999",  # Change as needed
        "notify_url": "https://www.yourwebsite.com/notify",  # Optional
        "redirect_url": "https://www.yourwebsite.com/success",  # Success URL
        "callback_url": "https://www.yourwebsite.com/callback"  # Optional callback URL
    }

    headers = {
        'Content-Type': 'application/json',
        'x-client-id': api_key,
        'x-client-secret': api_secret,
    }

    # Make the POST request to Cashfree API
    response = requests.post(api_url, headers=headers, data=json.dumps(payment_data))
    response_data = response.json()

    if response_data['status'] == 'OK':
        return response_data['payment_link']
    else:
        return "Error generating payment link: " + response_data['message']

# Command function for '/pay'
def pay(update: Update, context: CallbackContext):
    payment_link = generate_payment_link()
    update.message.reply_text(f"Your payment link: {payment_link}")

# Command function for '/start'
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome! Use /pay to generate a payment link.')

# Main function to run the bot
def main():
    # Telegram Bot API token
    bot_token = '7057865734:AAEBB12yJESX5sZ278UYumyectVPx3PuzpI'  # Your Bot Token
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('pay', pay))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()