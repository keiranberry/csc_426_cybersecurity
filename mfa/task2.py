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
        
        # Prompt the user for their information.
        username = input("Enter your username: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        # Generate a salt and hash the password.
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Create a cursor object using the connection.
        cursor = connection.cursor()

        # Insert the username, email, salt, and hashed password into the lab4users table.
        insert_query = """
        INSERT INTO lab4users (username, email, salt, password) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (username, email, salt.decode('utf-8'), hashed_password.decode('utf-8')))
        connection.commit()  # Commit the transaction

        print("User data inserted successfully.")

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
