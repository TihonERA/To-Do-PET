const ToDo = document.getElementsByClassName('.create')
const CreateCont = document.getElementsByClassName('.create-container')

ToDo.addEventListener('click' , function(e){
    e.preventDefault(); 
    CreateCont.classList.add('active');
})
