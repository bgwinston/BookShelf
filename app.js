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

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const username = document.getElementById('username').value;
            window.location.href = `dashboard.html?username=${encodeURIComponent(username)}`;
        });
    }

    const dashboardWelcomeContainer = document.getElementById('dashboard-message-container');
    if (dashboardWelcomeContainer) {
        const username = getQueryParam('username') || 'Guest';
        const template = document.getElementById('welcome-template').innerHTML;
        const rendered = Mustache.render(template, { username });
        dashboardWelcomeContainer.innerHTML = rendered;
    }
});
