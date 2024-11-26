import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Cashfree API credentials
app_id = '73553954db925af2b456a26e07935537'  # Replace with your Client ID
secret_key = 'cfsk_ma_prod_2d76755985f4b26b8a93f770157c6514_167eab6c'  # Replace with your Secret Key

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create payment link using Cashfree API
def create_payment_link(amount, order_id):
    url = 'https://api.cashfree.com/api/v2/cft/payment-links'

    headers = {
        'x-client-id': app_id,
        'x-client-secret': secret_key,
        'Content-Type': 'application/json'
    }

    payload = {
        "order_id": order_id,
        "order_amount": amount,
        "order_currency": "INR",
        "order_note": f"Payment for order {order_id}",
        "customer_email": "maniksaluja2004@gmail.com",  # Replace with actual email
        "customer_phone": "8708366003",  # Replace with actual phone
        "link_expiry_time": 1200  # Expiry time (20 minutes)
    }

    # Log the request for debugging
    logger.debug(f"Request Payload: {payload}")

    # Send the request to Cashfree API
    response = requests.post(url, headers=headers, json=payload)

    # Log response for debugging
    logger.debug(f"Response Status Code: {response.status_code}")
    logger.debug(f"Response Text: {response.text}")

    if response.status_code == 200:
        response_data = response.json()
        logger.debug(f"Response JSON: {response_data}")
        payment_link = response_data.get('payment_link', None)
        if payment_link:
            return payment_link
        else:
            return f"Error: Payment link not found in response: {response_data}"
    else:
        # Log detailed error information
        error_message = response.json().get('message', 'Unknown error')
        error_code = response.json().get('subCode', 'No subcode')
        logger.error(f"Error generating payment link: {error_message} (subCode: {error_code})")
        return f"Error generating payment link: {error_message} (subCode: {error_code})"

# /pay command handler
async def pay(update: Update, context: CallbackContext) -> None:
    order_id = "order12345"  # Generate a unique order ID or get from context
    amount = 2  # Amount in INR

    # Generate payment link
    payment_link = create_payment_link(amount, order_id)

    # Send the payment link to the user
    await update.message.reply_text(f"Here is your payment link: {payment_link}")

# Main function to start the bot
def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token("7341469021:AAFKFWX__rS5Et-Qco1ATpeA7EU92js3Pc0").build()

    # Register the /pay command handler
    application.add_handler(CommandHandler('pay', pay))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
