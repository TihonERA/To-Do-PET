const form = document.querySelector('.form-box form');
    const loginInput = document.querySelector('.login');
    const passwordInput = document.querySelector('.pass');
    const submitBtn = document.querySelector('button[type="submit"]');
    let errorDiv = document.querySelector('.login-error');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'login-error';
        errorDiv.style.color = 'red';
        errorDiv.style.marginTop = '10px';
        errorDiv.style.textAlign = 'center';
        form.appendChild(errorDiv);
    }
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); 
        errorDiv.textContent = '';
        const login = loginInput.value.trim();
        const password = passwordInput.value;

        if (!login || !password) {
            errorDiv.textContent = 'Заполните все поля';
            return;
        }
        try {
            const response = await fetch('http://localhost:8000/registration', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ login, password })
            });

            const data = await response.json();

            if (response.ok) {
                window.location.href = '/http://localhost:8000/registration';
            } else {
                // Ошибка авторизации – показываем сообщение от сервера
                errorDiv.textContent = data.message || 'Неверный логин или пароль';
            }
        } catch (err) {
            console.error('Ошибка соединения:', err);
            errorDiv.textContent = 'Сервер временно недоступен. Попробуйте позже.';
        } finally {
            // Разблокируем кнопку
            submitBtn.disabled = false;
            submitBtn.textContent = 'Вход';
        }
    });