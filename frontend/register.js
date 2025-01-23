const registerForm = document.getElementById('register-form');
const errorMessage = document.getElementById('error-message');

registerForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value; // Добавляем поле email
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://localhost:8000/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }), // Отправляем все три поля
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Registration failed');
        }

        const data = await response.json();
        console.log('User created:', data);

        // Редирект на страницу логина
        window.location.href = 'login.html';
    } catch (error) {
        console.error('Error:', error);
        errorMessage.textContent = error.message;
    }
});
