from flask import Flask, jsonify
import requests

app = Flask(manik)

app_id = '73553954db925af2b456a26e07935537'
secret_key = 'cfsk_ma_prod_2d76755985f4b26b8a93f770157c6514_167eab6c'
url = 'https://api.cashfree.com/api/v2/cft/payment-links'

headers = {
    'x-client-id': app_id,
    'x-client-secret': secret_key,
    'Content-Type': 'application/json'
}

@app.route('/generate_payment_link')
def generate_payment_link():
    payload = {
        "order_id": "order12345",
        "order_amount": 2,
        "order_currency": "INR",
        "order_note": "Payment for order order12345",
        "customer_email": "maniksaluja2004@gmail.com",
        "customer_phone": "8708366003",
        "link_expiry_time": 1200
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        response_data = response.json()
        return jsonify({"payment_link": response_data.get('payment_link')})
    else:
        return jsonify({"error": response.json()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
