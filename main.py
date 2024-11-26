import json
import requests
from flask import Flask, jsonify

# Cashfree API details
CASHFREE_APP_ID = 'TEST1027828340bdc693b933350cd9b738287201'
CASHFREE_SECRET_KEY = 'cfsk_ma_test_ee2923adec8914232ae79d9826252885_d6faea13'

app = Flask(__name__)

# Function to generate dynamic payment link
def generate_payment_link():
    url = "https://test.cashfree.com/api/v2/cftoken/order"
    
    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "appId": CASHFREE_APP_ID,
        "secretKey": CASHFREE_SECRET_KEY,
        "orderAmount": "2",  # Set payment amount
        "orderCurrency": "INR",
        "orderNote": "Test payment",
        "customerPhone": "1234567890",  # Dummy phone number
        "customerEmail": "test@example.com",  # Dummy email
        "orderId": "order_001",  # Unique order ID
    }

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        payment_data = response.json()
        if payment_data.get('status') == 'OK':
            payment_link = payment_data['paymentLink']
            return payment_link
        else:
            return "Error: " + payment_data.get('message', 'Unknown error')
    else:
        return "Error: Unable to generate payment link"

# Route to trigger payment link generation
@app.route('/pay', methods=['GET'])
def pay():
    # Generate the dynamic payment link
    payment_link = generate_payment_link()
    return jsonify({'payment_link': payment_link})

# Home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to Payment Link Generator! Use /pay to generate payment link.'})

if __name__ == "__main__":
    app.run(debug=True)
