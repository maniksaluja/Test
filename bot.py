import requests
import json
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Cashfree API details
CASHFREE_MERCHANT_ID = 'TEST1027828340bdc693b933350cd9b738287201'
CASHFREE_SECRET_KEY = 'cfsk_ma_test_ee2923adec8914232ae79d9826252885_d6faea13'

# Telegram bot token
TELEGRAM_BOT_TOKEN = '7057865734:AAEBB12yJESX5sZ278UYumyectVPx3PuzpI'

# Cashfree payment link creation function
def create_payment_link(amount, order_id):
    url = "https://api.cashfree.com/api/v2/cashfree/payment-links"
    
    headers = {
        "Content-Type": "application/json",
        "x-client-id": CASHFREE_MERCHANT_ID,
        "x-client-secret": CASHFREE_SECRET_KEY
    }

    data = {
        "order_id": order_id,
        "order_amount": amount,
        "order_currency": "INR",
        "customer_details": {
            "customer_email": "customer@example.com",
            "customer_phone": "1234567890"
        },
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("status") == "OK":
            return response_data["payment_link_url"]
        else:
            return "Error: " + response_data.get("message", "Unable to create payment link")
    else:
        return f"Error: {response.status_code}"

# Function to handle the /pay command
def pay(update: Update, context: CallbackContext):
    # Generate new order ID
    order_id = "order_" + str(int(time.time()))
    
    # Generate payment link
    amount = 100  # Example amount in INR
    payment_link = create_payment_link(amount, order_id)
    
    # Send the payment link to the user
    update.message.reply_text(f"Here is your payment link: {payment_link}")

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
