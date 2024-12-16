import mysql.connector  # Required for MySQL database connection


class Book:

    def __init__(self, title, author, origin, genre, description, user_id):
        self.title = title
        self.author = author
        self.origin = origin
        self.genre = genre
        self.description = description
        self.user_id = user_id

    def save_to_db(self, cnx, cursor):
        try:
            query = """
            INSERT INTO mybooks (title, author, origin, genre, description, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (self.title, self.author, self.origin, self.genre, self.description, self.user_id))
            cnx.commit()
            print(f"Book '{self.title}' added successfully!")
            return True
        except Exception as e:
            print(f"Error saving book to database: {e}")
            return False