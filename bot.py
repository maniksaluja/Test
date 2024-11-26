import logging
import random
import string
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Telegram bot token
TELEGRAM_BOT_TOKEN = '7057865734:AAEBB12yJESX5sZ278UYumyectVPx3PuzpI'

# Cashfree API details
BASE_URL = "https://api.cashfree.com/api/v2/cftoken/order"
APP_ID = "73553954db925af2b456a26e07935537"
SECRET_KEY = "cfsk_ma_prod_a137f4b96e800e1356e2a4476b6bea75_82b9f03e"

# Setting up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Generate a random order ID
def generate_order_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Function to create payment link
def create_payment_link(order_id, amount):
    payload = {
        "order_id": order_id,
        "order_amount": amount,
        "order_currency": "INR",
        "version": "2023-08-01",  # API version
        "customer_details": {
            "customer_id": "12345",
            "customer_email": "test@example.com",
            "customer_phone": "9999999999"
        }
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-client-id": APP_ID,
        "x-client-secret": SECRET_KEY
    }

    response = requests.post(BASE_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("payment_link", "Error generating link")
    else:
        return f"Error: {response.text}"

# Command handler for /pay
async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    amount = 2  # Payment amount (in INR)
    
    # Generate order ID
    order_id = generate_order_id()
    
    # Call Cashfree API to create payment link
    payment_link = create_payment_link(order_id, amount)
    
    # Send payment link to the user
    await update.message.reply_text(f"Here is your payment link: {payment_link}")

# Main function to run the bot
def main():
    # Initialize the Application with your bot token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add /pay command handler
    pay_handler = CommandHandler('pay', pay)
    application.add_handler(pay_handler)
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
