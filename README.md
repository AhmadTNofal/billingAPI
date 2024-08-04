# Billing API
This project provides RESTful APIs for handling bill inquiries, bill payments, and bill inquiry responses. The APIs are implemented using Flask and MySQL.

## Features
- Login: Using JWT to produce access token
- Check Payment Status
- UpdatePaymentStatus
- Get All Billing
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

CREATE TABLE billing (
    customerAccountName VARCHAR(255),
    customerID INT UNIQUE,
    orderID INT UNIQUE,
    billingNumber INT UNIQUE,
    paymentAmount DECIMAL(10, 2),
    currency ENUM('USD', 'IQD'),
    description TEXT,
    paymentStatus ENUM('paid', 'unpaid'),
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
- Response:
~~~json
{
    "access_token": "<Token>"
}
~~~

### Check Payment Status
- Endpoint: **/checkPaymentStatus**
- Method: **POST**
- Headers:
    - **Authorization: Bearer <token>**
    - **Content-Type: application/json**
-Body:
~~~json
     {
       "orderID": 4499494,
       "billingNumber": 333333
     }
~~~
- Response:
~~~json
{
    "billingNumber": 333333,
    "createdAt": "Sun, 04 Aug 2024 12:23:11 GMT",
    "currency": "IQD",
    "customerAccountName": "Ahmed Rahman",
    "customerID": 73737373,
    "description": "test",
    "message": "successful",
    "orderID": 4499494,
    "paymentAmount": "50000.00",
    "paymentStatus": "unpaid",
    "success": "true"
}
~~~

### Update Payment Status
- Endpoint: **/updatePaymentStatus**
- Method: **POST**
- Headers:
    - **Authorization: Bearer <token>**
    - **Content-Type: application/json**
- Body:
~~~json
     {
       "orderID": 4499494,
       "billingNumber": 333333
     }
~~~
- Response:
~~~json
{
    "billingNumber": 333333,
    "createdAt": "Sun, 04 Aug 2024 12:23:11 GMT",
    "currency": "IQD",
    "customerAccountName": "Ahmed Rahman",
    "customerID": 73737373,
    "description": "test",
    "message": "payment is successful",
    "orderID": 4499494,
    "paymentAmount": "50000.00",
    "paymentStatus": "paid",
    "success": "true"
}
~~~


### Get All Billing
- Endpoint: **/getAllBilling**
- Method: **GET**
- Headers:
    - **Authorization: Bearer <token>**
    - **Content-Type: application/json**
- Body
~~~json
~~~
- Response
~~~json
     [
       {
         "success": "true",
         "message": "payment is successful",
         "orderID": "4499494",
         "billingNumber": "333333",
         "paymentAmount": 50000,
         "currency": "IQD",
         "paymentStatus": "unpaid"
       },
       {
         "success": "true",
         "message": "payment is successful",
         "orderID": "4499495",
         "billingNumber": "333334",
         "paymentAmount": 75000,
         "currency": "USD",
         "paymentStatus": "paid"
       }
     ]
~~~


## Testing the APIs

You can use a tool like Postman to test the APIs. Follow these steps for each endpoint:
1. Open Postman and create a new request.
2. Set the request method to **POST**.
3. Enter the URL for the endpoint.
4. Add the required headers:
    - **Authorization: Bearer YOUR_API_ACCESS_KEY**
    - **Content-Type: application/json**
5. Add the JSON body according to the endpoint specifications.
6. Send the request and check the response.

## Example: Testing Bill Inquiry Request API
- URL: **http://localhost:5000/billing/api/v1/bi**
- Headers:
    - **Authorization: Bearer YOUR_API_ACCESS_KEY**
    - **Content-Type: application/json**
- Body:
~~~json
{
  "bill_number": "12345",
  "reference_number": "67890",
  "service_code": "155"
}
~~~