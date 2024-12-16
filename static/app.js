document.addEventListener('DOMContentLoaded', () => {
    // Reference to the create-account-welcome container and create-account-header
    const welcomeWrapper = document.getElementById('create-account-welcome');
    const createAccountHeader = document.getElementById('create-account-header');
    const createAccountForm = document.getElementById('create-account-form');

    // Dynamically set the welcome message using the `firstname` variable
    if (welcomeWrapper && typeof firstname !== 'undefined') {
        const welcomeMessage = `
            <div class="welcome-message">
                <h2>Welcome, ${firstname}!</h2>
                <p>Thank you for creating an account. We're excited to have you on board!</p>
                <a href="/login" class="btn btn-primary">Login</a>
            </div>
        `;
        welcomeWrapper.innerHTML = welcomeMessage;
    }

    if (createAccountForm) {
        createAccountForm.addEventListener('submit', async function (event) {
            event.preventDefault(); // Prevent the default form submission

            // Collect form data
            const formData = new FormData(createAccountForm);

            console.log("FormData entries:");
            for (let [key, value] of formData.entries()) {
                console.log(`${key}: ${value}`);
            }

            // Send the form data to the backend using fetch
            try {
                const response = await fetch('/createaccount', {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    const firstname = formData.get('firstname');
                    console.log("Firstname retrieved from formData:", firstname);

                    // Inject the welcome message dynamically
                    if (welcomeWrapper) {
                        const welcomeMessage = `
                            <div class="welcome-message">
                                <h2>Welcome, ${firstname}!</h2>
                                <p>Thank you for creating an account. We're excited to have you on board!</p>
                                <a href="/login" class="btn btn-primary">Login</a>
                            </div>
                        `;
                        welcomeWrapper.innerHTML = welcomeMessage;
                        welcomeWrapper.style.display = 'block'; // Show the welcome message
                    }

                    // Hide the form and header
                    if (createAccountHeader) {
                        createAccountHeader.style.display = 'none';
                    }

                } else {
                    console.error('Error creating account:', response.statusText);
                    alert('Failed to create account. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again later.');
            }
        });
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            window.location.href = `dashboard.html?email=${encodeURIComponent(email)}`;
        });
    }

    const dashboardWelcomeContainer = document.getElementById('dashboard-message-container');
    if (dashboardWelcomeContainer && typeof firstname !== 'undefined') {
        // Create the dashboard welcome message
        const welcomeMessage = `
            <h2>We're glad you're here, ${firstname}!</h2>
            <p>Let's explore your bookshelf and make reading more fun!</p>
        `;
        // Inject the message into the container
        dashboardWelcomeContainer.innerHTML = welcomeMessage;
    }
});