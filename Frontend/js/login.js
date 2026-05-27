    const form = document.querySelector('.form-box form');
    const loginInput = document.querySelector('.login');
    const passwordInput = document.querySelector('.pass');
    const submitBtn = document.querySelector('button');
    const token = localStorage.getItem('token')

    const responce = await fetch('http://localhost:8000/login' , {
        headers: {'Authorization': `Bearer ${token}`}
    })

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); 
        const login = loginInput.value.trim();
        const password = passwordInput.value;
        if (!login || !password) {
            alert('Заполните все поля');
            return 
        }})

    submitBtn.addEventListener('click' , () => {
        e.preventDefault() 
        window.location.href = 'http://localhost:8000/'
    })

    if(!login.length < 0){
        alert('Введите логин')
        return
    } 
    if(!password.length < 0){
        alert('Введите пароль')
        return
    }
    if(token){
        window.location.href = 'http://localhost:8000/'
    }
            
