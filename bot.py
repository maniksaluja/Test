from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests
import threading

# Telegram Bot Token
BOT_TOKEN = "7057865734:AAEBB12yJESX5sZ278UYumyectVPx3PuzpI"

# Cashfree Credentials
CASHFREE_APP_ID = "73553954db925af2b456a26e07935537"
CASHFREE_SECRET_KEY = "cfsk_ma_prod_2d76755985f4b26b8a93f770157c6514_167eab6c"

# Flask App for Webhook
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Webhook Data Received:", data)  # For debugging
    # Respond to Cashfree webhook
    return jsonify({"status": "success"}), 200

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
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to the bot! Use /pay <amount> to create a payment link.")

async def pay(update: Update, context: CallbackContext):
    try:
        amount = float(context.args[0])
        user_id = update.message.from_user.id
        email = "user@example.com"  # Default email, can be dynamic
        phone = "8708366003"  # Default phone, can be dynamic
        order_id = f"Order{user_id}"

        payment_link = generate_payment_link(order_id, amount, email, phone)
        if payment_link:
            await update.message.reply_text(f"Pay using this link: {payment_link}")
        else:
            await update.message.reply_text("Failed to generate payment link. Try again!")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /pay <amount>")

# Start Telegram Bot in a Thread
def start_telegram_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pay", pay))
    
    application.run_polling()

# Main Script
if __name__ == "__main__":
    # Run Telegram bot in a separate thread
    bot_thread = threading.Thread(target=start_telegram_bot)
    bot_thread.start()

    # Run Flask app for webhook
    app.run(host="0.0.0.0", port=5000)
