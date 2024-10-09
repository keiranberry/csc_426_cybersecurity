import mysql.connector
from mysql.connector import Error
import bcrypt
import pyotp
import qrcode
from PIL import Image

try:
    # Create a connection to the database.
    connection = mysql.connector.connect(
        host='localhost',
        user='keiran',  # replace with your MySQL username
        password='thisisap455w0rd',  # replace with your MySQL password
        database='userdb'  # replace with your MySQL database name
    )

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        
        # Prompt the user for their information.
        username = input("Enter your username: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        # Generate a salt and hash the password.
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Generate the OTP secret with pyotp.
        totp_secret = pyotp.random_base32()

        # Create a cursor object using the connection.
        cursor = connection.cursor()

        # Insert the username, email, salt, hashed password, and TOTP secret into the lab4users table.
        insert_query = """
        INSERT INTO lab4users (username, email, salt, password, totp_secret) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (username, email, salt.decode('utf-8'), hashed_password.decode('utf-8'), totp_secret))
        connection.commit()  # Commit the transaction

        print("User data inserted successfully.")
        
        # Generate a TOTP URI for the user.
        totp = pyotp.TOTP(totp_secret)
        otp_uri = totp.provisioning_uri(name=username, issuer_name="Lab4")

        # Generate a QR code for the OTP URI.
        qr_code = qrcode.make(otp_uri)

        # Save the QR code as an image.
        qr_code_file = f'{username}_qr_code.png'
        qr_code.save(qr_code_file)

        # Open and display the QR code.
        img = Image.open(qr_code_file)
        img.show()

        print(f"Scan this QR code with an authenticator app (e.g., Google Authenticator).")

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
