    const form = document.querySelector('.form-box form');
    const emailInput = document.querySelector('.email');
    const loginInput = document.querySelector('.login');
    const passInput = document.querySelector('.pass');
    const confirmInput = document.querySelector('input[type="password"]:not(.pass)'); 
    const submitBtn = document.querySelector('button[type="submit"]');


    let errorDiv = document.querySelector('.reg-error');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'reg-error';
        errorDiv.style.color = 'red';
        errorDiv.style.marginTop = '10px';
        errorDiv.style.textAlign = 'center';
        form.appendChild(errorDiv);
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorDiv.textContent = '';

        const email = emailInput.value.trim();
        const login = loginInput.value.trim();
        const password = passInput.value;
        const confirm = confirmInput.value;

        if (!email || !login || !password || !confirm) {
            errorDiv.textContent = 'Заполните все поля';
            return;
        }
        if (password.length < 6) {
            errorDiv.textContent = 'Пароль должен быть не менее 6 символов';
            return;
        }
        if (password !== confirm) {
            errorDiv.textContent = 'Пароли не совпадают';
            return;
        }
        try {
            const response = await fetch('http://localhost:8000/registration', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, login, password })
            });

            const data = await response.json();

            if (response.ok) {
                window.location.href = 'http://localhost:8000/';
            } else {
                errorDiv.textContent = data.message || 'Ошибка регистрации. Попробуйте другой логин или email.';
            }
        } catch (err) {
            console.error(err);
            errorDiv.textContent = 'Сервер недоступен. Попробуйте позже.';
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Регистрация';
        }
    });