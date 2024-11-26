import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import httpx

# Replace these with your actual credentials
TELEGRAM_BOT_TOKEN = "7057865734:AAEBB12yJESX5sZ278UYumyectVPx3PuzpI"
CASHFREE_APP_ID = "TEST1027828340bdc693b933350cd9b738287201"
CASHFREE_SECRET_KEY = "cfsk_ma_test_ee2923adec8914232ae79d9826252885_d6faea13"

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /pay command."""
    # Generate a dynamic payment link
    payment_data = {
        "customer_details": {
            "customer_id": "12345",
            "customer_email": "test@example.com",
            "customer_phone": "9999999999"
        },
        "order_amount": 100.0,
        "order_currency": "INR",
        "order_note": "Test Payment",
        "order_id": "Order_" + str(int(asyncio.time() * 1000)),
        "return_url": "https://example.com/success"
    }
    headers = {
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://sandbox.cashfree.com/pg/orders",
            json=payment_data,
            headers=headers
        )
        result = response.json()

    if response.status_code == 200 and result.get("status") == "OK":
        payment_link = result["payment_link"]
        await update.message.reply_text(f"Here is your payment link: {payment_link}")
    else:
        await update.message.reply_text("Failed to generate payment link. Please try again later.")

async def main():
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add the /pay command handler
    application.add_handler(CommandHandler("pay", pay))

    # Run the bot
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
