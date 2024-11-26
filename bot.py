from telegram.ext import Application, CommandHandler
import httpx

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7057865734:AAEBB12yJESX5sZ278UYumyectVPx3PuzpI"

# Cashfree Credentials
CASHFREE_APP_ID = "TEST1027828340bdc693b933350cd9b738287201"
CASHFREE_SECRET_KEY = "cfsk_ma_test_ee2923adec8914232ae79d9826252885_d6faea13"

# Payment Function
async def generate_payment_link(update, context):
    user_id = update.effective_user.id
    payment_data = {
        "order_id": f"ORDER_{user_id}_{int(update.message.date.timestamp())}",
        "order_amount": 100.0,
        "order_currency": "INR",
        "customer_details": {
            "customer_id": str(user_id),
            "customer_email": "user@example.com",
            "customer_phone": "9999999999"
        },
        "order_note": "Payment for your order",
        "notify_url": "https://your-server.com/webhook"
    }

    headers = {
        "Content-Type": "application/json",
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://sandbox.cashfree.com/pg/orders", json=payment_data, headers=headers)

    if response.status_code == 200:
        payment_link = response.json().get("payment_link", "Error: Link not generated")
        await update.message.reply_text(f"Here is your payment link: {payment_link}")
    else:
        await update.message.reply_text(f"Error generating payment link: {response.text}")

# Main Function to Run the Bot
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("pay", generate_payment_link))
    application.run_polling()

if __name__ == "__main__":
    main()
