import logging
from telegram import Update
from telegram.ext import Application, CommandHandler
from telegram.error import NetworkError
import time

# Enable logging for better debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Command handler for /pay
async def pay(update: Update, context):
    try:
        # Example payment link (Replace with your actual dynamic payment link logic)
        payment_link = "https://your-payment-link"  # Change this to your payment link or dynamic generation
        await update.message.reply_text(f"Here is your payment link: {payment_link}")
    except NetworkError as e:
        # Handle network issues like Bad Gateway
        logger.error(f"Network Error: {str(e)}")
        await update.message.reply_text("Network issue, please try again later.")
    except Exception as e:
        # Catch all other exceptions
        logger.error(f"Error while handling /pay: {str(e)}")
        await update.message.reply_text("Sorry, something went wrong!")

# Retry mechanism for the bot in case of network issues
def start_bot():
    try:
        # Replace with your new bot token
        application = Application.builder().token("7341469021:AAFKFWX__rS5Et-Qco1ATpeA7EU92js3Pc0").build()

        # Add the /pay command handler
        pay_handler = CommandHandler('pay', pay)
        application.add_handler(pay_handler)

        # Start polling for updates
        application.run_polling()
    except NetworkError:
        # If network issue occurs, retry after a delay
        logger.error("Network error occurred, retrying...")
        time.sleep(5)  # Retry after 5 seconds
        start_bot()

if __name__ == '__main__':
    start_bot()
