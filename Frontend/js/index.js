const CreateToDo = document.querySelector('.create')
const ContainerToDo = document.querySelector('.create-container')
const CloseToDo = document.querySelector('.offwind')

CreateToDo.addEventListener('click' , function(e){
    e.preventDefault();
    ContainerToDo.classList.add('active');
});
CloseToDo.addEventListener('click', () => {
    ContainerToDo.classList.remove('active')
})
