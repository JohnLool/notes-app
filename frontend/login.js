const loginForm = document.getElementById('login-form');
const errorMessage = document.getElementById('error-message');

loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://localhost:8000/auth/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ username: email, password }), // `username` для совместимости с FastAPI
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Login failed');
        }

        const data = await response.json();
        console.log('Access Token:', data.access_token);

        // Сохраняем токен в localStorage
        localStorage.setItem('access_token', data.access_token);

        // Редирект на страницу профиля
        window.location.href = 'profile.html';
    } catch (error) {
        console.error('Error:', error);
        errorMessage.textContent = error.message;
    }
});
// test
