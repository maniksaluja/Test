from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Cashfree Credentials
CASHFREE_APP_ID = "73553954db925af2b456a26e07935537"
CASHFREE_SECRET_KEY = "cfsk_ma_prod_2d76755985f4b26b8a93f770157c6514_167eab6c"

# Function to Generate Payment Link
def generate_payment_link(order_id, amount, email, phone):
    url = "https://api.cashfree.com/pg/orders"
    headers = {
        "Content-Type": "application/json",
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY,
    }
    payload = {
        "order_id": order_id,
        "order_amount": amount,
        "order_currency": "INR",
        "customer_details": {
            "customer_id": order_id,
            "customer_email": email,
            "customer_phone": phone,
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("payment_link")
    else:
        print("Error:", response.json())  # Debugging
        return None

# Telegram Bot Commands
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Use /pay <amount> to make a payment.")

def pay(update: Update, context: CallbackContext):
    try:
        # Parse amount from user message
        amount = float(context.args[0])
        user_id = update.message.from_user.id
        email = "user@example.com"  # Replace with dynamic user email if needed
        phone = "9876543210"  # Replace with dynamic user phone if needed
        order_id = f"Order{user_id}"  # Unique order ID per user

        # Generate Payment Link
        payment_link = generate_payment_link(order_id, amount, email, phone)
        if payment_link:
            update.message.reply_text(f"Pay using this link: {payment_link}")
        else:
            update.message.reply_text("Failed to generate payment link. Try again!")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /pay <amount>")

# Bot Setup
updater = Updater("7057865734:AAEBB12yJESX5sZ278UYumyectVPx3PuzpI")
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("pay", pay))

# Start Bot
updater.start_polling()
updater.idle()
