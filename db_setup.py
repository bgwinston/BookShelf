from dbConnection import cnx, cursor

def create_users_table(cnx, cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        firstname VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        country VARCHAR(255) NOT NULL
    );
    """
    try:
        cursor.execute(create_table_query)
        cnx.commit()  # Commit the changes to the database
        print("Users table created successfully!")
    except Exception as e:
        print(f"An error occurred while creating the users table: {e}")

def create_mybooks_table(cnx, cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS mybooks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        origin ENUM('Purchased', 'Borrowed') NOT NULL,
        genre VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        user_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """
    try:
        cursor.execute(create_table_query)
        cnx.commit()  # Commit the changes to the database
        print("MyBooks table created successfully!")
    except Exception as e:
        print(f"An error occurred while creating the mybooks table: {e}")

def create_wishlist_table(cnx, cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS wishlist (
        id INT AUTO_INCREMENT PRIMARY KEY,
        book_name VARCHAR(255) NOT NULL,
        author VARCHAR(255),
        genre VARCHAR(100),
        user_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """
    try:
        cursor.execute(create_table_query)
        cnx.commit()  # Commit the changes to the database
        print("Wishlist table created successfully!")
    except Exception as e:
        print(f"An error occurred while creating the wishlist table: {e}")

# Call the table creation functions
create_users_table(cnx, cursor)
create_mybooks_table(cnx, cursor)
create_wishlist_table(cnx, cursor)