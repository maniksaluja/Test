from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from cashfree_pg import CashfreePG
import datetime

# Cashfree Credentials
APP_ID = "73553954db925af2b456a26e07935537"
SECRET_KEY = "cfsk_ma_prod_2d76755985f4b26b8a93f770157c6514_167eab6c"
ENVIRONMENT = "PROD"  # Use "TEST" for sandbox environment

# Telegram Bot Token
BOT_TOKEN = "7341469021:AAFKFWX__rS5Et-Qco1ATpeA7EU92js3Pc0"

# Initialize Cashfree
cashfree_pg = CashfreePG(app_id=APP_ID, secret_key=SECRET_KEY, environment=ENVIRONMENT)


def start(update: Update, context: CallbackContext) -> None:
    """Handles /start command."""
    update.message.reply_text(
        "Welcome! Use /pay to generate a payment link for INR 2."
    )


def generate_payment_link(update: Update, context: CallbackContext) -> None:
    """Generates a Cashfree payment link."""
    user = update.message.from_user

    # Customer Details
    customer_details = {
        "customer_id": str(user.id),
        "customer_email": "maniksaluja2004@gmail.com",  # Static email for now
        "customer_phone": "8708366003"  # Static phone number for now
    }

    # Payment Link Details
    order_id = f"ORDER_{user.id}_{int(datetime.datetime.now().timestamp())}"
    order_amount = 2  # Fixed amount
    expiry_time = (datetime.datetime.now() + datetime.timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%S+05:30")

    # Request body
    payload = {
        "customer_details": customer_details,
        "order_id": order_id,
        "order_amount": order_amount,
        "order_currency": "INR",
        "order_expiry_time": expiry_time
    }

    # Create Payment Link
    try:
        response = cashfree_pg.payment_links.create(payload)
        if response["status"] == "OK":
            payment_link = response["data"]["link_url"]
            update.message.reply_text(
                f"Here is your payment link (valid for 20 minutes):\n{payment_link}"
            )
        else:
            update.message.reply_text(
                f"Failed to generate payment link. Error: {response['message']}"
            )
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")


def main() -> None:
    """Start the bot."""
    updater = Updater(BOT_TOKEN)

    # Register Handlers
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("pay", generate_payment_link))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
