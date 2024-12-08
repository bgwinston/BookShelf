document.addEventListener('DOMContentLoaded', () => {
    // Listen for the form submission
    document.getElementById('create-account-form').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent traditional form submission

        // Get the first name value
        const firstname = document.getElementById('firstname').value;

        // Retrieve the Mustache template
        const template = document.getElementById('welcome-template').innerHTML;

        // Render the template with the first name
        const rendered = Mustache.render(template, { firstname });

        // Update the welcome message container
        const welcomeMessageContainer = document.getElementById('welcome-message-container');
        welcomeMessageContainer.innerHTML = rendered;

        // Show the welcome message and hide the form
        welcomeMessageContainer.style.display = 'block';
        document.querySelector('.create-account-container').style.display = 'none';
    });
});
