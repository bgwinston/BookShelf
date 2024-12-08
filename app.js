// Check if we are on the "Create Account" page
if (document.getElementById('create-account-form')) {
    // Listen for the form submission event
    document.getElementById('create-account-form').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent form from submitting traditionally

        // Get the first name from the form
        const firstname = document.getElementById('firstname').value;

        // Save the first name to localStorage
        localStorage.setItem('firstname', firstname);

        // Get the Mustache template for the welcome message
        const template = document.getElementById('welcome-template').innerHTML;

        // Render the template with the user's data
        const rendered = Mustache.render(template, { firstname });

        // Display the rendered template in the welcome message container
        document.getElementById('welcome-message-container').innerHTML = rendered;

        // Optionally hide the form after submission
        document.querySelector('.create-account-container').style.display = 'none';
    });
}

// Check if we are on the "Dashboard" page
if (document.getElementById('welcome-message-container')) {
    // Simulated user data
    const userData = {
        firstname: localStorage.getItem('firstname') || 'Guest',
        books: JSON.parse(localStorage.getItem('books')) || [] // Books from storage
    };

    // Render Welcome Message
    const welcomeTemplate = document.getElementById('welcome-template').innerHTML;
    const welcomeRendered = Mustache.render(welcomeTemplate, userData);
    document.getElementById('welcome-message-container').innerHTML = welcomeRendered;

    // Render Book Collection or No Books Message
    const bookContainer = document.getElementById('book-collection-container');
    if (userData.books.length === 0) {
        // Render "No Books" message
        const noBooksTemplate = document.getElementById('no-books-template').innerHTML;
        const noBooksRendered = Mustache.render(noBooksTemplate);
        bookContainer.innerHTML = noBooksRendered;
    } else {
        // Render book list
        const bookListTemplate = document.getElementById('book-list-template').innerHTML;
        const bookListRendered = Mustache.render(bookListTemplate, userData);
        bookContainer.innerHTML = bookListRendered;
    }
}
