import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7341469021:AAFKFWX__rS5Et-Qco1ATpeA7EU92js3Pc0'

# Cashfree Payment API Details
CASHFREE_APP_ID = '73553954db925af2b456a26e07935537'
CASHFREE_SECRET_KEY = 'cfsk_ma_prod_2d76755985f4b26b8a93f770157c6514_167eab6c'

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Welcome to the payment bot. Type /pay to generate a payment link.")

async def generate_payment_link(update: Update, context: CallbackContext):
    # Define the amount and other payment link parameters
    amount = 2  # INR
    expiry_minutes = 20  # Link expiry time in minutes
    
    # Create the payment link via Cashfree API
    url = "https://api.cashfree.com/api/v2/cashpay/links"
    headers = {
        "x-api-key": CASHFREE_SECRET_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "order_amount": amount,
        "order_currency": "INR",
        "order_note": "Test Payment",
        "notify_url": "https://yourdomain.com/notify",
        "redirect_url": "https://yourdomain.com/redirect",
        "expire_time": expiry_minutes * 60  # Expiry in seconds
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if result.get("status") == "OK":
        payment_link = result["payment_link"]
        await update.message.reply_text(f"Your payment link is: {payment_link}")
    else:
        await update.message.reply_text(f"Error generating payment link: {result.get('message', 'Unknown error')}")

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pay", generate_payment_link))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
