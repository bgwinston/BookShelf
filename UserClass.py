import mysql.connector  # Required for MySQL database connection
#import bcrypt  # Required for password hashing

class User:
    def __init__(self, firstname=None, password=None, email=None, country=None):
        self.firstname = firstname
        self.password = password  # Plain text password; will hash before storing
        self.email = email
        self.country = country

    # Method to create a new user in the database
    def create_account(self, cnx, cursor):
        try:
            # Check if the email already exists
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (self.email,))
            if cursor.fetchone():
                return "Email already exists!"
            
            # Hash the password
            #hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            
            # Insert new user into the database
            query = "INSERT INTO users (firstname, password, email, country) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (self.firstname, self.password, self.email, self.country))
            cnx.commit()
            return "Account created successfully!"
        
        except mysql.connector.Error as err:
            return f"Error creating account: {err}"
        
    def login(self, cnx, cursor):
        try:
            # Debug email and password values
            print(f"Attempting login with email: {self.email}, password: {self.password}")

            # Debug query
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            print(f"Executing query: {query}")
            print(f"With parameters: email={self.email}, password={self.password}")

            # Execute the query
            cursor.execute(query, (self.email, self.password))
            user = cursor.fetchone()

            # Debug the query result
            print(f"Query result: {user}")

            # Check if user exists
            if user:
                return "Login successful"
            else:
                return "Invalid username or password!"
        except Exception as e:
            print(f"Error during login: {e}")
            return "An error occurred while logging in"