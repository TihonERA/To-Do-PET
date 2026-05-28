const form = document.querySelector('.form-box form');
const loginInput = document.querySelector('.login');
const passwordInput = document.querySelector('.pass');
const submitBtn = document.querySelector('button');

// Создаём errorDiv один раз
let errorDiv = document.querySelector('.login-error');
if (!errorDiv) {
    errorDiv = document.createElement('div');
    errorDiv.className = 'login-error';
    errorDiv.style.color = 'red';
    errorDiv.style.marginTop = '10px';
    errorDiv.style.textAlign = 'center';
    form.appendChild(errorDiv);
}

// Убираем запрос, который был здесь — он не нужен пошел нахуй пидорас на дипсике ротан твой ебал хуесос!

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorDiv.textContent = '';
    submitBtn.disabled = true;
    submitBtn.textContent = 'Загрузка...';
    
    const login = loginInput.value.trim();
    const password = passwordInput.value;

    if (!login || !password) {
        errorDiv.textContent = 'Заполните все поля';
        submitBtn.disabled = false;
        submitBtn.textContent = 'Вход';
        return;
    }

    try {
        const formData = new FormData();
        formData.append('login_or_email', login);
        formData.append('password', password);

        const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
        login_or_email: login,
        password: password
    })
});

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('access_token', data.access_token);
            window.location.href = 'http://localhost:8000/';
        } else {
            errorDiv.textContent = data.detail || 'Неверный логин или пароль';
        }
    } catch (err) {
        console.error('Ошибка соединения:', err);
        errorDiv.textContent = 'Сервер временно недоступен. Попробуйте позже.';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Вход';
    }
});