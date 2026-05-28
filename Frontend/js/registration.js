    const form = document.querySelector('.form-box');
    const emailInput = document.querySelector('.email');
    const loginInput = document.querySelector('.login');
    const passInput = document.querySelector('.pass');
    const confirmInput = document.querySelector('input[type="password"]:not(.pass)'); 
    const submitBtn = document.querySelector('submit-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault()
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
            return
        }
        if (password !== confirm) {
            alert('Пароли не совпадают')
            return;
        }
        if (!password_length >72){
            alert('Пароль не может быть больше 72 символов') 
            return
        }
        async function userDate (email , password , login){
            const responce = await fetch('http://api.localhost:8000/registration' , {
                method: 'POST' ,
                headers: {'Content-Type' : 'application/json'}, 
                body: JSON.stringify({email , login , password})
            })
            if (!responce.ok) {
                const errorMess = await responce.json()
                const errorAlert = await alert('Ошибка Регистрации') 
                throw new Error(errorAlert)
            }
        };
    });
        const data = await responce.json()
        const token = data.access_token
        localStorage.setItem('usertoken' , token)

        submitBtn.addEventListener('click' , () =>{
            if(submitBtn == 'click') 
                window.location.href = 'http://localhost:8000/'
        })
    

