from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/payment-status', methods=['POST'])
def payment_status():
    data = request.get_json()
    
    # Cashfree se aane wali data ko handle karein
    if data.get('status') == 'SUCCESS':
        print("Payment successful")
    else:
        print("Payment failed or pending")
    
    return json.dumps({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
