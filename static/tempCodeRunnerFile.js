document.addEventListener('DOMContentLoaded', () => {
    function getQueryParam(param) {
        const params = new URLSearchParams(window.location.search);
        return params.get(param);
    }

    const createAccountForm = document.getElementById('create-account-form');
    if (createAccountForm) {
        createAccountForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const firstname = document.getElementById('firstname').value;
            const template = document.getElementById('welcome-template').innerHTML;
            const rendered = Mustache.render(template, { firstname });
            const welcomeMessageContainer = document.getElementById('welcome-message-container');
            welcomeMessageContainer.innerHTML = rendered;
            welcomeMessageContainer.style.display = 'block';
            document.querySelector('.create-account-container').style.display = 'none';
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        const createAccountForm = document.getElementById('create-account-form');
    
        if (createAccountForm) {
            createAccountForm.addEventListener('submit', function (event) {
                event.preventDefault(); // Prevent form from submitting
    
                // Get the firstname value
                const firstname = document.getElementById('firstname').value;
    
                // Get the Mustache template
                const template = document.getElementById('welcome-template').innerHTML;
    
                // Render the template with the firstname
                const rendered = Mustache.render(template, { firstname });
    
                // Display the welcome message
                const welcomeMessageContainer = document.getElementById('welcome-message-container');
                welcomeMessageContainer.innerHTML = rendered;
                welcomeMessageContainer.style.display = 'block';
    
                // Hide the form container
                document.querySelector('.create-account-container').style.display = 'none';
            });
        }
    });

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            window.location.href = `dashboard.html?email=${encodeURIComponent(email)}`;
        });
    }

    const dashboardWelcomeContainer = document.getElementById('dashboard-message-container');
    if (dashboardWelcomeContainer) {
        const email = getQueryParam('email') || 'Guest';
        const template = document.getElementById('welcome-template').innerHTML;
        const rendered = Mustache.render(template, { email });
        dashboardWelcomeContainer.innerHTML = rendered;
    }
});
