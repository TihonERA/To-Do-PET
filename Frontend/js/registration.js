const form = document.querySelector('.form-box');
const emailInput = document.querySelector('.email');
const loginInput = document.querySelector('.login');
const passInput = document.querySelector('.pass');
const confirmInput = document.querySelector('.confirm-pass');
const submitBtn = document.querySelector('.submit-btn');
const errorDiv = document.querySelector('.error-mess');

function showError(message) {
  errorDiv.textContent = message;
  errorDiv.style.display = 'block'
}
function clearError() {
  errorDiv.textContent = '';
  errorDiv.style.display = 'none';
}
console.log('1')
async function userDate(email, login, password) {
  const response = await fetch('http://localhost:8000/register', {
    method: 'POST',
    headers: {
       'Content-Type': 'application/json' , 
       'accept': 'application/json'
      },
    body: JSON.stringify({ email, login, password})
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const detail = errorData.detail || `Ошибка ${response.status}: ${response.statusText}`;
    throw new Error(detail);
  }
  const data = await response.json();
  console.log(data);
  return data.access_token;
}
console.log('2')
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearError();
  submitBtn.disabled = true;

  const email = emailInput.value.trim();
  const login = loginInput.value.trim();
  const password = passInput.value;
  const confirm = confirmInput.value;
console.log('3')
  if (!email || !login || !password || !confirm) {
    showError('Заполните все поля');
    submitBtn.disabled = false;
    return;
  }
  if (password.length < 16) {
    showError('Пароль должен быть не менее 16 символов');
    submitBtn.disabled = false;
    return;
  }
  if (password !== confirm) {
    showError('Пароли не совпадают');
    submitBtn.disabled = false;
    return;
  }
  if (password.length > 72) {
    showError('Пароль не может быть больше 72 символов');
    submitBtn.disabled = false;
    return;
  }
  if (response.status || response.textContent == 'userToken is not defined'){
    submitBtn.disabled = false
  }
console.log('4')
  try {
    const token = await userDate(email, login, password);
    localStorage.setItem('usertoken', token);
    console.log('Проверка')
    
    window.location.href = 'http://localhost:8000/';
  } catch (err) {
    showError(err.message || 'Произошла ошибка при регистрации' || 'userToken is not defined');
    submitBtn.disabled = false;
  }
});