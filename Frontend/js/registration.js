const form = document.querySelector('.form-box');
const emailInput = document.querySelector('.email');
const loginInput = document.querySelector('.login');
const passInput = document.querySelector('.pass');
const confirmInput = document.querySelector('input[type="password"]:not(.pass)');
const submitBtn = document.querySelector('.submit-btn');

// Создаем элемент для ошибок
const errorDiv = document.createElement('div');
form.insertBefore(errorDiv, form.firstChild);

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = emailInput.value.trim();
    const login = loginInput.value.trim();
    const password = passInput.value;
    const confirm = confirmInput.value;

    if (!email || !login || !password || !confirm) {
        errorDiv.textContent = 'Заполните все поля';
        return;
    }
    
    if (password.length < 16) {
        errorDiv.textContent = 'Пароль должен быть не менее 16 символов';
        return;
    }
    
    if (password.length > 72) {
        errorDiv.textContent = 'Пароль не может быть больше 72 символов';
        return;
    }
    
    if (password !== confirm) {
        errorDiv.textContent = 'Пароли не совпадают';
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, login, password })
        });

        if (!response.ok) {
            const errorMess = await response.json();
            errorDiv.textContent = errorMess.message || 'Ошибка регистрации';
            return;
        }

        const data = await response.json();
        const token = data.access_token;
        localStorage.setItem('usertoken', token);
        
        // Перенаправление после успешной регистрации
        window.location.href = 'http://localhost:8000/';
        
    } catch (error) {
        console.error('Ошибка:', error);
        errorDiv.textContent = 'Ошибка соединения с сервером';
    }
});