from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import datetime
import requests
import asyncio

# Cashfree Credentials
APP_ID = "73553954db925af2b456a26e07935537"
SECRET_KEY = "cfsk_ma_prod_2d76755985f4b26b8a93f770157c6514_167eab6c"
ENVIRONMENT = "PROD"  # Use "TEST" for sandbox environment

# Telegram Bot Token
BOT_TOKEN = "7341469021:AAFKFWX__rS5Et-Qco1ATpeA7EU92js3Pc0"

async def start(update: Update, context: CallbackContext) -> None:
    """Handles /start command."""
    await update.message.reply_text(
        "Welcome! Use /pay to generate a payment link for INR 2."
    )


async def generate_payment_link(update: Update, context: CallbackContext) -> None:
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
        "order_expiry_time": expiry_time,
        "version": "2023-08-01"  # Added version parameter
    }

    # Create Payment Link
    url = "https://api.cashfree.com/pg/links"
    headers = {
        "Content-Type": "application/json",
        "x-client-id": APP_ID,
        "x-client-secret": SECRET_KEY,
    }

    try:
        # Make the API request to Cashfree
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            payment_link = response.json().get("data", {}).get("link_url", "")
            await update.message.reply_text(
                f"Here is your payment link (valid for 20 minutes):\n{payment_link}"
            )
        else:
            await update.message.reply_text(f"Error: {response.text}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def main() -> None:
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Register Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pay", generate_payment_link))

    # Start the Bot
    await application.run_polling()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
