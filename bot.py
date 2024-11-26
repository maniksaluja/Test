import asyncio
from flask import Flask, request, jsonify
from telethon import TelegramClient, events
import requests
import threading

# Telegram Bot Token
API_ID = 'your_api_id'  # You need to get your own API ID and API Hash
API_HASH = 'your_api_hash'
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
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("payment_link")
        else:
            print(f"Error: {response.json()}")  # Debugging
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Telethon Bot Commands
async def start(event):
    await event.respond("Welcome to the bot! Use /pay <amount> to create a payment link.")

async def pay(event):
    try:
        amount = float(event.pattern_match.group(1))
        user_id = event.sender_id
        email = "user@example.com"  # Default email, can be dynamic
        phone = "8708366003"  # Default phone, can be dynamic
        order_id = f"Order{user_id}"

        payment_link = generate_payment_link(order_id, amount, email, phone)
        if payment_link:
            await event.respond(f"Pay using this link: {payment_link}")
        else:
            await event.respond("Failed to generate payment link. Try again!")
    except (IndexError, ValueError):
        await event.respond("Usage: /pay <amount>")

# Start Telethon Client
async def start_telethon_bot():
    client = TelegramClient('bot', API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)

    @client.on(events.NewMessage(pattern='/start'))
    async def handler_start(event):
        await start(event)

    @client.on(events.NewMessage(pattern=r'/pay (\d+\.?\d*)'))
    async def handler_pay(event):
        await pay(event)

    await client.run_until_disconnected()

# Run Flask and Telethon in Separate Threads
def main():
    # Run Telethon bot in a separate thread
    bot_thread = threading.Thread(target=lambda: asyncio.run(start_telethon_bot()))
    bot_thread.start()

    # Run Flask app for webhook
    app.run(host="0.0.0.0", port=5000)

# Run the main function
if __name__ == "__main__":
    main()
