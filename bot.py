from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests
import datetime

# Cashfree API credentials
APP_ID = "73553954db925af2b456a26e07935537"
SECRET_KEY = "cfsk_ma_prod_2d76755985f4b26b8a93f770157c6514_167eab6c"
BOT_TOKEN = "7341469021:AAFKFWX__rS5Et-Qco1ATpeA7EU92js3Pc0"

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Welcome! Use /pay to generate a payment link for INR 2."
    )

async def generate_payment_link(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    customer_details = {
        "customer_id": str(user.id),
        "customer_email": "maniksaluja2004@gmail.com",
        "customer_phone": "8708366003"
    }
    order_id = f"ORDER_{user.id}_{int(datetime.datetime.now().timestamp())}"
    order_amount = 2
    expiry_time = (datetime.datetime.now() + datetime.timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%S+05:30")

    payload = {
        "customer_details": customer_details,
        "order_id": order_id,
        "order_amount": order_amount,
        "order_currency": "INR",
        "order_expiry_time": expiry_time,
        "version": "2023-08-01"
    }

    url = "https://api.cashfree.com/pg/links"
    headers = {
        "Content-Type": "application/json",
        "x-client-id": APP_ID,
        "x-client-secret": SECRET_KEY,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            payment_link = response.json().get("data", {}).get("link_url", "")
            await update.message.reply_text(f"Here is your payment link (valid for 20 minutes):\n{payment_link}")
        else:
            await update.message.reply_text(f"Error: {response.text}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def main():
    # Create the application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pay", generate_payment_link))

    # Start polling
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
