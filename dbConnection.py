import mysql.connector  # Ensure this import is at the top

# Define the database connection parameters
username = "root"
password = "root1234"
host = "127.0.0.1"
port = 3306
database = "MyBookshelf"


try:
    # Create a connection to the MySQL server
    cnx = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        port=port
    )

    cursor = cnx.cursor()
    
    # Create the database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")

    # Switch to the  database
    cnx.database = database
    print("Database connection established successfully!")

except mysql.connector.Error as err:
    print("Error connecting to database:", err)
    exit(1)

# Check if the connection is active
if cnx.is_connected():
    print("Database connection is active!")
else:
    print("Database connection is not active!")