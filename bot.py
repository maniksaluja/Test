import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests
import json

# Replace with your bot token
bot_token = "7341469021:AAFKFWX__rS5Et-Qco1ATpeA7EU92js3Pc0"

# Cashfree API credentials
app_id = '73553954db925af2b456a26e07935537'
secret_key = 'cfsk_ma_prod_a137f4b96e800e1356e2a4476b6bea75_82b9f03e'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Create payment link using Cashfree API
def create_payment_link(amount, order_id):
    url = 'https://api.cashfree.com/api/v2/cft/payment-links'

    headers = {
        'x-client-id': app_id,
        'x-client-secret': secret_key,
        'Content-Type': 'application/json'
    }

    payload = {
        "order_id": order_id,
        "order_amount": amount,
        "order_currency": "INR",
        "order_note": "Payment for order " + order_id,
        "customer_email": "customer@example.com",
        "customer_phone": "9999999999"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        payment_link = response.json()['payment_link']
        return payment_link
    else:
        return f"Error generating payment link: {response.text}"

# /pay command handler
async def pay(update: Update, context: CallbackContext) -> None:
    order_id = "order12345"  # Generate a unique order ID or get from context
    amount = 2  # Amount in INR

    # Generate payment link
    payment_link = create_payment_link(amount, order_id)

    # Send the payment link to the user
    await update.message.reply_text(f"Here is your payment link: {payment_link}")

# Main function to start the bot
def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(bot_token).build()

    # Register the /pay command handler
    application.add_handler(CommandHandler('pay', pay))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
