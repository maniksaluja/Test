import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# Production Cashfree credentials
APP_ID = "73553954db925af2b456a26e07935537"
SECRET_KEY = "cfsk_ma_prod_a137f4b96e800e1356e2a4476b6bea75_82b9f03e"
BASE_URL = "https://api.cashfree.com/pg/orders"

# Set up logging to see what's happening
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to generate the payment link
def create_payment_link(order_id, amount):
    payload = {
        "order_id": order_id,
        "order_amount": amount,
        "order_currency": "INR",
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

# Function to handle the /pay command
async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_id = "ORDER123"  # Replace with a unique order ID for each payment
    amount = 2.0  # Amount in INR
    
    # Generate the payment link
    payment_link = create_payment_link(order_id, amount)

    # Send the payment link to the user
    await update.message.reply_text(f"Here is your payment link: {payment_link}")

# Main function to run the bot
def main():
    # Initialize the Application with your bot token
    application = Application.builder().token("7057865734:AAEBB12yJESX5sZ278UYumyectVPx3PuzpI").build()

    # Add /pay command handler
    pay_handler = CommandHandler('pay', pay)
    application.add_handler(pay_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
