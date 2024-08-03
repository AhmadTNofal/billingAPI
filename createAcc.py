from passlib.hash import pbkdf2_sha256 as sha256
import mysql.connector
# Replace these with your actual values
username = 'test'
password = 'password'

password_hash = sha256.hash(password)

# Connect to MySQL and insert the admin user
conn = mysql.connector.connect(
    host='localhost',
    database='restfulapi',
    user='root',
    password=''
)
cursor = conn.cursor()
cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', (username, password_hash))
conn.commit()
cursor.close()
conn.close()
