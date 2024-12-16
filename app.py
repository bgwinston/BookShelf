from flask import Flask, render_template, request, redirect, session
from UserClass import User
from BookClass import Book
from dbConnection import cnx, cursor

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for sessions


@app.route('/') 
def index():
    return render_template('index.html')


@app.route('/createaccount', methods=['GET', 'POST'])
def create_account():
    print("Route '/createaccount' accessed")

    message=None
    firstname=None

    if request.method == 'POST':
        
        print(request.form)

        firstname = request.form['firstname']
        password = request.form['password']
        email = request.form['email']
        country = request.form['country']

        firstname = request.form.get('firstname')

        print(f"Received: firstname={firstname}, password={password}, email={email}, country={country}")

        
        new_user = User(firstname, password, email, country)

        message = new_user.create_account(cnx, cursor)
        print(f"Database result: {message}")


    return render_template('createaccount.html',message=message, firstname=firstname)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Route '/login' accessed")
    message = None

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        print(f"email: {email}, password: {password}")

        # Ensure correct parameter order
        user = User(email=email, password=password)

        # Login the user
        message = user.login(cnx, cursor)
        print(f"Login message: {message}")

        if message == 'Login successful':
            session['email'] = email
            return redirect('/dashboard')

    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    print("User logged out successfully")
    # Redirect to the login page
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect('/login')  # Redirect to login if session is missing

    email = session['email']
    query = "SELECT firstname FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    firstname = user[0] if user else 'Guest'  # Default to 'Guest' if no user is found

    query_books = """
    SELECT title 
    FROM mybooks 
    WHERE user_id = (SELECT id FROM users WHERE email = %s)
    ORDER BY id DESC 
    LIMIT 3
    """
    cursor.execute(query_books, (email,))
    books = cursor.fetchall()  # Fetch the result as a list of tuples
    
    # Extract titles as a list
    book_titles = [book[0] for book in books]

    # Pass the titles to the template
    wishlist_query = """
    SELECT book_name 
    FROM wishlist 
    WHERE user_id = (SELECT id FROM users WHERE email = %s)
    ORDER BY id DESC 
    LIMIT 3
    """
    cursor.execute(wishlist_query, (email,))
    wishlist_books = cursor.fetchall()  # Fetch the result as a list of tuples
    wishlist_titles = [book[0] for book in wishlist_books]

    return render_template('dashboard.html', email=email, firstname=firstname,book_titles=book_titles, wishlist_titles=wishlist_titles)


@app.route('/addbook', methods=['GET', 'POST'])
def add_book():
    print("Accessed /addbook route")
    print(f"Request method: {request.method}")
    if 'email' not in session:
        return redirect('/login')  # Redirect to login if the user is not logged in
    print(f"Request method: {request.method}")
    if request.method == 'POST':
        # Retrieve form data
        title = request.form.get('title')
        author = request.form.get('author')
        origin = request.form.get('origin')  # Purchased or Borrowed
        genre = request.form.get('genre')
        description = request.form.get('description')

        # Debug: Print the form data
        print(f"Form Data: title={title}, author={author}, origin={origin}, genre={genre}, description={description}")

        # Fetch user ID from session
        email = session['email']
        query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user:
            user_id = user[0]
            print(f"User ID: {user_id}")  # Debug: Verify user ID

            try:
                # Insert book into the database
                add_book_query = """
                INSERT INTO mybooks (title, author, origin, genre, description, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(add_book_query, (title, author, origin, genre, description, user_id))
                cnx.commit()
                print(f"Book '{title}' added successfully for user {email}.")
                return redirect('/dashboard')  # Redirect to dashboard after adding the book
            except Exception as e:
                print(f"Error adding book: {e}")
                return "An error occurred while adding the book. Please try again.", 500

    return render_template('addbook.html')  # Render the add book form

@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    if 'email' not in session:
        return redirect('/login')  # Redirect to login if the user is not logged in

    email = session['email']  # Fetch the logged-in user's email

    if request.method == 'POST':
        # Check if the form is for adding or deleting
        if 'book_name' in request.form:  # Adding a book
            # Retrieve form data
            book_name = request.form.get('book_name')
            author = request.form.get('author')
            genre = request.form.get('genre')

            # Debug: Print the form data
            print(f"Form Data: book_name={book_name}, author={author}, genre={genre}")

            query = "SELECT id FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user:
                user_id = user[0]
                try:
                    # Insert the book into the wishlist
                    add_to_wishlist_query = """
                    INSERT INTO wishlist (book_name, author, genre, user_id)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(add_to_wishlist_query, (book_name, author, genre, user_id))
                    cnx.commit()
                    print(f"Book '{book_name}' added to wishlist for user {email}.")
                except Exception as e:
                    print(f"Error adding to wishlist: {e}")
                    return "An error occurred while adding to the wishlist. Please try again.", 500

        elif 'delete_books' in request.form:  # Deleting books
            delete_ids = request.form.getlist('delete_books')  # Get all selected IDs
            print(f"Books to delete: {delete_ids}")

            if delete_ids:
                try:
                    # Create the placeholders dynamically for the number of IDs
                    placeholders = ', '.join(['%s'] * len(delete_ids))
                    delete_query = f"""
                    DELETE FROM wishlist 
                    WHERE id IN ({placeholders}) AND user_id = (
                        SELECT id FROM users WHERE email = %s
                    )
                    """
                    # Add `email` to the parameters for the query
                    params = delete_ids + [email]
                    cursor.execute(delete_query, params)
                    cnx.commit()
                    print(f"Deleted books with IDs: {delete_ids}")
                except Exception as e:
                    print(f"Error deleting from wishlist: {e}")
                    return "An error occurred while deleting from the wishlist. Please try again.", 500

    # Fetch wishlist items for the current user
    query = """
    SELECT id, book_name, author, genre 
    FROM wishlist 
    WHERE user_id = (SELECT id FROM users WHERE email = %s)
    """
    cursor.execute(query, (email,))
    wishlist_items = cursor.fetchall()  # Fetch all rows

    return render_template('wishlist.html', books=wishlist_items)

if __name__ == '__main__':
    app.run(debug=True)