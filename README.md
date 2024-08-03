# Billing API
This project provides RESTful APIs for handling bill inquiries, bill payments, and bill inquiry responses. The APIs are implemented using Flask and MySQL.

## Features
- Login: Using JWT to produce access token
- Bill Inquiry Request: Endpoint to submit a bill inquiry.
- Bill Payment Information: Endpoint to submit bill payment information.
- Logs: Save all endpoints responses to logs Table

## Requirements
- Python 3.6+
- Flask
- MySQL
- mysql-connector-python package
- python-dotenv package

## Installation

1. Clone the repository:
~~~bash
    git clone https://github.com/AhmadTNofal/billingAPI.git
    cd billing-api
~~~

2. Install the required Python packages:
~~~bash
    pip install Flask mysql-connector-python python-dotenv
~~~

## Database Setup

~~~sql
CREATE DATABASE billing;

USE billing;

CREATE TABLE bill_inquiries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_number VARCHAR(255) NOT NULL,
    reference_number VARCHAR(255),
    service_code VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bill_payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_number VARCHAR(255) NOT NULL,
    reference_number VARCHAR(255),
    service_code VARCHAR(255) NOT NULL,
    paid_amount DECIMAL(10, 2) NOT NULL,
    process_date BIGINT NOT NULL,
    payment_type VARCHAR(1) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INT NOT NULL,
    request_body TEXT,
    response_body TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


~~~

## Environment Variables
- Create a .env file in the project directory with the following content, replacing the placeholders with your actual database credentials and API access key:
~~~bash
DB_HOST=your_remote_host_address
DB_NAME=billing
DB_USER=your_db_user
DB_PASSWORD=your_db_password
JWT_SECRET_KEY=HS256
~~~


## API Endpoints
### Login
- Endpoint: **/login**
- Method: **POST**
- Headers:
    - **Content-Type: application/json**
-Body:
~~~json
{
  "username": "admin",
  "password": "password"
}

~~~

### Bill Inquiry Request
- Endpoint: **/billing/api/v1/bi**
- Method: **POST**
- Headers:
    - **Authorization: Bearer <access_token>**
    - **Content-Type: application/json**
-Body:
~~~json
{
  "bill_number": "12345",
  "reference_number": "67890",
  "service_code": "155"
}
~~~

- Response:
    - **201 Created** on success
    - **400 Bad Request** if required fields are missing
    - **401 Unauthorized** if API key is invalid
    - **500 Internal Server** Error on server error

### Bill Payment Information
- Endpoint: **/billing/api/v1/bp**
- Method: **POST**
- Headers:
    - **Authorization: Bearer <access_token>**
    - **Content-Type: application/json**
-Body:
~~~json
{
  "bill_number": "12345",
  "reference_number": "67890",
  "service_code": "155",
  "paid_amount": 100.50,
  "process_date": 1625140800,
  "payment_type": "F"
}
~~~

- Response:
    - **201 Created** on success
    - **400 Bad Request** if required fields are missing
    - **401 Unauthorized** if API key is invalid
    - **500 Internal Server** Error on server error


## Testing the APIs

You can use a tool like Postman to test the APIs. Follow these steps for each endpoint:
1. Open Postman and create a new request.
2. Set the request method to **POST**.
3. Enter the URL for the endpoint.
4. Add the required headers:
    - **Authorization: ApiKey YOUR_API_ACCESS_KEY**
    - **Content-Type: application/json**
5. Add the JSON body according to the endpoint specifications.
6. Send the request and check the response.

## Example: Testing Bill Inquiry Request API
- URL: **http://localhost:5000/billing/api/v1/bi**
- Headers:
    - **Authorization: ApiKey YOUR_API_ACCESS_KEY**
    - **Content-Type: application/json**
- Body:
~~~json
{
  "bill_number": "12345",
  "reference_number": "67890",
  "service_code": "155"
}
~~~