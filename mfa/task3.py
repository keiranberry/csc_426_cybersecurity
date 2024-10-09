import mysql.connector
from mysql.connector import Error
import bcrypt

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
        
        # Prompt the user for their username and password.
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Create a cursor object using the connection.
        cursor = connection.cursor()

        # Retrieve the stored hashed password and salt for the entered username.
        query = "SELECT password, salt FROM lab4users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            stored_hashed_password, salt = result

            # Hash the entered password using the retrieved salt.
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))

            # Compare the hashed version of the entered password with the stored hashed password.
            if hashed_password.decode('utf-8') == stored_hashed_password:
                print("Authentication successful!")
            else:
                print("Incorrect password.")
        else:
            print("Username does not exist.")

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")