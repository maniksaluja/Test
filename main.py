import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Cashfree API details
CASHFREE_APP_ID = 'TEST1027828340bdc693b933350cd9b738287201'
CASHFREE_SECRET_KEY = 'cfsk_ma_test_ee2923adec8914232ae79d9826252885_d6faea13'

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7057865734:AAEBB12yJESX5sZ278UYumyectVPx3PuzpI'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to generate dynamic payment link
def generate_payment_link():
    url = "https://test.cashfree.com/api/v2/cftoken/order"
    
    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "appId": CASHFREE_APP_ID,
        "secretKey": CASHFREE_SECRET_KEY,
        "orderAmount": "2",  # Set payment amount
        "orderCurrency": "INR",
        "orderNote": "Test payment",
        "customerPhone": "1234567890",  # Dummy phone number
        "customerEmail": "test@example.com",  # Dummy email
        "orderId": "order_001",  # Unique order ID
    }

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        payment_data = response.json()
        if payment_data.get('status') == 'OK':
            payment_link = payment_data['paymentLink']
            return payment_link
        else:
            return "Error: " + payment_data.get('message', 'Unknown error')
    else:
        return "Error: Unable to generate payment link"

# Command handler to trigger payment link generation
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Type /pay to generate a payment link.')

def pay(update: Update, context: CallbackContext) -> None:
    # Generate the dynamic payment link
    payment_link = generate_payment_link()
    update.message.reply_text(f"Here is your payment link: {payment_link}")

def main():
    # Initialize the Updater
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("pay", pay))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
