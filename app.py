from flask import Flask, request, jsonify, g
import mysql.connector
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from passlib.hash import pbkdf2_sha256 as sha256

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

jwt = JWTManager(app)

# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

# Log request and response
def log_request_response(endpoint, method, status_code, request_body, response_body):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO logs (endpoint, method, status_code, request_body, response_body) VALUES (%s, %s, %s, %s, %s)',
            (endpoint, method, status_code, request_body, response_body)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        app.logger.error(f"Error logging request and response: {e}")

# Middleware to log requests and responses
@app.after_request
def after_request(response):
    endpoint = request.path
    method = request.method
    status_code = response.status_code
    request_body = request.get_data(as_text=True)
    response_body = response.get_data(as_text=True)
    log_request_response(endpoint, method, status_code, request_body, response_body)
    return response

# User login to get a JWT token
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    # Validate username and password
    if user and sha256.verify(password, user['password_hash']):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'msg': 'Bad username or password'}), 401

# Endpoint for bill inquiry request
@app.route('/billing/api/v1/bi', methods=['POST'])
@jwt_required()
def bill_inquiry():
    data = request.get_json()

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
@jwt_required()
def bill_payment():
    data = request.get_json()
    
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

if __name__ == '__main__':
    app.run(debug=True)
