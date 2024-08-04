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

# Endpoint to check payment status
@app.route('/checkPaymentStatus', methods=['POST'])
@jwt_required()
def check_payment_status():
    data = request.get_json()
    orderID = data.get('orderID')
    billingNumber = data.get('billingNumber')

    if not orderID or not billingNumber:
        return jsonify({'success': 'false', 'message': 'Order ID and Billing Number are required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM billing WHERE orderID = %s AND billingNumber = %s', (orderID, billingNumber))
        billing = cursor.fetchone()

        cursor.close()
        conn.close()

        if billing:
            billing['success'] = 'true'
            billing['message'] = 'successful'
            return jsonify(billing), 200
        else:
            return jsonify({'success': 'false', 'message': 'Order ID or Billing Number not found'}), 404

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'success': 'false', 'message': 'Internal Server Error'}), 500

# Endpoint to update payment status
@app.route('/updatePaymentStatus', methods=['POST'])
@jwt_required()
def update_payment_status():
    data = request.get_json()
    orderID = data.get('orderID')
    billingNumber = data.get('billingNumber')

    if not orderID or not billingNumber:
        return jsonify({'success': 'false', 'message': 'Order ID and Billing Number are required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM billing WHERE orderID = %s AND billingNumber = %s', (orderID, billingNumber))
        billing = cursor.fetchone()

        if billing:
            if billing['paymentStatus'] == 'paid':
                return jsonify({'success': 'false', 'message': 'payment is already paid'}), 400

            cursor.execute('UPDATE billing SET paymentStatus = %s WHERE orderID = %s AND billingNumber = %s',
                           ('paid', orderID, billingNumber))
            conn.commit()

            cursor.execute('SELECT * FROM billing WHERE orderID = %s AND billingNumber = %s', (orderID, billingNumber))
            updated_billing = cursor.fetchone()

            cursor.close()
            conn.close()

            updated_billing['success'] = 'true'
            updated_billing['message'] = 'payment is successful'
            return jsonify(updated_billing), 200
        else:
            cursor.close()
            conn.close()
            return jsonify({'success': 'false', 'message': 'Order ID or Billing Number not found'}), 404

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'success': 'false', 'message': 'Internal Server Error'}), 500

# Endpoint to get all billing records
@app.route('/getAllBilling', methods=['GET'])
@jwt_required()
def get_all_billing():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM billing')
        billing_records = cursor.fetchall()

        cursor.close()
        conn.close()

        for billing in billing_records:
            billing['success'] = 'true'
            billing['message'] = 'retrieved successfully'

        return jsonify(billing_records), 200

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'success': 'false', 'message': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
