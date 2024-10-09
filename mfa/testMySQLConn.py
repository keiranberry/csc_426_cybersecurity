import mysql.connector
from mysql.connector import Error

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
        
        # Create a cursor object using the connection.
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
