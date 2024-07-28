from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

# Validate API Key
def validate_api_key(api_key):
    return api_key == os.getenv('API_ACCESS_KEY')

# Endpoint for bill inquiry request
@app.route('/billing/api/v1/bi', methods=['POST'])
def bill_inquiry():
    api_key = request.headers.get('Authorization')
    if not validate_api_key(api_key):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    bill_number = data.get('bill_number')
    reference_number = data.get('reference_number')
    service_code = data.get('service_code')

    if not bill_number or not service_code:
        return jsonify({'error': 'bill_number and service_code are required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO bill_inquiries (bill_number, reference_number, service_code) VALUES (%s, %s, %s)',
            (bill_number, reference_number, service_code)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

    return jsonify({'status': 'success'}), 201

# Endpoint for bill payment information
@app.route('/billing/api/v1/bp', methods=['POST'])
def bill_payment():
    api_key = request.headers.get('Authorization')
    if not validate_api_key(api_key):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    bill_number = data.get('bill_number')
    reference_number = data.get('reference_number')
    service_code = data.get('service_code')
    paid_amount = data.get('paid_amount')
    process_date = data.get('process_date')
    payment_type = data.get('payment_type')

    if not bill_number or not service_code or not paid_amount or not process_date or not payment_type:
        return jsonify({'error': 'bill_number, service_code, paid_amount, process_date, and payment_type are required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO bill_payments (bill_number, reference_number, service_code, paid_amount, process_date, payment_type) VALUES (%s, %s, %s, %s, %s, %s)',
            (bill_number, reference_number, service_code, paid_amount, process_date, payment_type)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

    return jsonify({'status': 'success'}), 201

# Endpoint for bill inquiry response
@app.route('/billing/api/v1/bi/response', methods=['POST'])
def bill_inquiry_response():
    api_key = request.headers.get('Authorization')
    if not validate_api_key(api_key):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    bill_inquiry_id = data.get('bill_inquiry_id')
    response_code = data.get('response_code')
    response_message = data.get('response_message')

    if not bill_inquiry_id or not response_code:
        return jsonify({'error': 'bill_inquiry_id and response_code are required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO bill_inquiry_responses (bill_inquiry_id, response_code, response_message) VALUES (%s, %s, %s)',
            (bill_inquiry_id, response_code, response_message)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

    return jsonify({'status': 'success'}), 201

if __name__ == '__main__':
    app.run(debug=True)
