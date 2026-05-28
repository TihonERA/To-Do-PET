const form = document.querySelector('.form-box');
const emailInput = document.querySelector('.email');
const loginInput = document.querySelector('.login');
const passInput = document.querySelector('.pass');
const confirmInput = document.querySelector('.confirm-pass');
const submitBtn = document.querySelector('.submit-btn'); 

async function userDate(email, login, password) {
    const response = await fetch('http://api.localhost:8000/registration', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, login, password })
    });
    const data = await response.json();
    return data.access_token; 
}
form.addEventListener('submit', async (e) => {
    e.preventDefault();

const email = emailInput.value.trim()
const login = loginInput.value.trim()
const password = passInput.value
const confirm = confirmInput.value
    
    if (!email || !login || !password || !confirm) {
        alert('Заполните всеполя')
        return
    }
    if (password.length < 16) {
        alert('Пароль должен быть не менее 16 символов')
        return
    }
    if (password !== confirm) {
        alert('Пароли не совпадают')
        return
    }
    if (password.length > 72) {
        alert('Пароль не может быть больше 72 символо')
        return
    }
        const token = await userDate(email, login, password);
        localStorage.setItem('usertoken', token);
        submitBtn.addEventListener('click' , () =>{
            window.location.href = 'http://localhost:8000/'
        })
});