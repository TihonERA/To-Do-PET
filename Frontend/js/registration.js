const form = document.querySelector('.form-box');
const emailInput = document.querySelector('.email');
const loginInput = document.querySelector('.login');
const passInput = document.querySelector('.pass');
const confirmInput = document.querySelector('.confirm-pass');
const submitBtn = document.querySelector('.submit-btn');
const errorMess = document.querySelector('.error-mess')

async function userDate(email, login, password) {
    const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, login, password })
    });
    const data = await response.json();
    return data.access_token; 
}
form.addEventListener('submit', async (e) => {
    e.preventDefault();
submitBtn.disabled = true
const email = emailInput.value.trim()
const login = loginInput.value.trim()
const password = passInput.value
const confirm = confirmInput.value
    try{
    if (!email || !login || !password || !confirm) {
        alert('Заполните все поля')
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
        })}
        catch(err){
        errorMess.textContent = err.message || 'Ошибка соединения с сервером';
        console.error(err);
        submitBtn.disabled = false; 
        }
}); 