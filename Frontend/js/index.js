document.addEventListener("DOMContentLoaded", function() {

    const token = localStorage.getItem('usertoken')
    fetch("/users/me", {
        method: "GET", 
        headers: {
            'Content-Type': 'application/json', 
            'accept': 'application/json' , 
            'Authorization': `Bearer ${token}`
        }, 
        })
    })
    // 1. Поиск элементов интерфейса заметок
    const create = document.querySelector('.create');
    const todoContainer = document.querySelector('.todo-container');
    const todoTitle = document.querySelector('.todo-title');
    const todoDescription = document.querySelector('.todo-description');
    const closeTodo = document.querySelector('.close-todo');
    const closeWarContainer = document.querySelector('.close-war-container');
    const warCancel = document.querySelector('.war-cancel');
    const warConfirm = document.querySelector('.war-confirm');
    const addTodo = document.querySelector('.add-todo');
    const notesList = document.querySelector('.notes-list');
    const priorityContainer = document.querySelector('.priority-container');
    const selectPriorityContainer = document.querySelector('.select-priority-container');
    const priorityInput = document.querySelector('.priority-input');
    const priorityOptions = document.querySelectorAll('.select-priority-container > div');
    const dataInput = document.querySelector('.data-input');
    
    // Элементы настроек и фильтра
    const filterBtn = document.querySelector('.filter');
    const settBtn = document.querySelector('.sett-btn'); 
    const settCont = document.querySelector('.settings-container'); 
    const settingsForm = document.getElementById('settingsForm'); // Было пропущено!

    let selectedPriority = null; 
    let selectedDate = "";     
    const originalPriorityHTML = priorityInput ? priorityInput.innerHTML : '';
    const originalDataHTML = dataInput ? dataInput.innerHTML : '';

    // 2. Инициализация Flatpickr
    if (dataInput && typeof flatpickr !== 'undefined') {
        flatpickr(dataInput, {
            enableTime: true,           
            dateFormat: "d.m.Y H:i",    
            time_24hr: true,            
            disableMobile: "true",      
            onChange: function(selectedDates, dateStr) {
                selectedDate = dateStr;
                dataInput.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 16 16" class="data-icon" aria-hidden="true">
                        <path fill="#6194e7" d="M12 2a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm0 1H4a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1m-1.25 7a.75.75 0 1 1 0 1.5.75.75 0 0 1 0-1.5m.75-5a.5.5 0 1 1 0 1h-7a.5.5 0 0 1 0-1z"></path>
                    </svg>
                    ${dateStr}
                `;
            }
        });
    }

    // 3. Выпадающий список приоритетов
    if (priorityContainer && selectPriorityContainer) {
        priorityContainer.addEventListener('click', function(e) {
            e.stopPropagation(); 
            selectPriorityContainer.classList.toggle('visible');
        });
    }

    document.addEventListener('click', function() {
        if (selectPriorityContainer) {
            selectPriorityContainer.classList.remove('visible');
        }
    });

    priorityOptions.forEach(option => {
        option.addEventListener('click', function(e) {
            e.stopPropagation();
            const svgPath = this.querySelector('path');
            const color = svgPath ? svgPath.getAttribute('fill') : '#bbb7b7';
            
            selectedPriority = {
                text: this.innerText.trim(),
                color: color,
                rawHTML: this.innerHTML
            };
          
            if (priorityInput) {
                priorityInput.innerHTML = selectedPriority.rawHTML;
                priorityInput.style.color = '#ecf1fb';
            }
            selectPriorityContainer.classList.remove('visible');
        });
    });

    // 4. Функция сброса формы
    function resetForm() {
        todoTitle.value = "";
        todoDescription.value = "";
        selectedDate = "";
        selectedPriority = null;
        if (priorityInput) {
            priorityInput.innerHTML = originalPriorityHTML;
            priorityInput.style.color = '';
        }
        if (dataInput) {
            dataInput.innerHTML = originalDataHTML;
        }
    }

    // Открытие/закрытие модального окна создания заметки
    if (create) {
        create.addEventListener('click', function() {
            todoContainer.classList.add('visible');
        });
    }

    if (closeTodo) {
        closeTodo.addEventListener('click', function() {
            const hasText = (todoTitle.value && todoTitle.value.trim() !== "") || 
                            (todoDescription.value && todoDescription.value.trim() !== "") ||
                            selectedDate !== "" || selectedPriority !== null;

            if (hasText) {
                closeWarContainer.style.display = 'flex'; 
            } else {
                todoContainer.classList.remove('visible'); 
            }
        });
    }

    if (warCancel) {
        warCancel.addEventListener('click', function() {
            closeWarContainer.style.display = 'none';
        });
    }

    if (warConfirm) {
        warConfirm.addEventListener('click', function() {
            resetForm();
            closeWarContainer.style.display = 'none';
            todoContainer.classList.remove('visible');
        });
    }

    // 5. Создание новой заметки
    if (addTodo) {
        addTodo.addEventListener('click', function() {
            const titleText = todoTitle.value.trim();
            const descText = todoDescription.value.trim();

            if (titleText === "" && descText === "") {
                alert("Заполните поля названия и описания");
                return;
            }

            const smallNote = document.createElement('div');
            smallNote.classList.add('small-note');

            let metaHTML = "";
            if (selectedDate || selectedPriority) {
                metaHTML = `<div class="small-note-meta">`;
                if (selectedDate) {
                    metaHTML += `<span class="note-date-badge">⏱️ ${selectedDate}</span>`;
                }
                if (selectedPriority) {
                    metaHTML += `
                        <span class="note-priority-badge" style="background: ${selectedPriority.color}1a; color: ${selectedPriority.color}; border: 1px solid ${selectedPriority.color}33">
                            ${selectedPriority.text}
                        </span>`;
                }
                metaHTML += `</div>`;
            }

            smallNote.innerHTML = `
                <div class="small-note-header">
                    <input type="checkbox" class="note-checkbox">
                    <div class="small-note-body">
                        <h4 class="small-note-title">${titleText || "Без названия"}</h4>
                        <p class="small-note-desc">${descText || "Нет описания"}</p>
                        ${metaHTML}
                    </div>
                </div>
                <div class="small-note-actions">
                    <button class="note-btn edit-btn">Изменить</button>
                    <button class="note-btn delete-btn">Удалить</button>
                </div>
            `;

            const savedPriority = selectedPriority;
            const savedDate = selectedDate;

            const checkbox = smallNote.querySelector('.note-checkbox');
            const deleteBtn = smallNote.querySelector('.delete-btn');
            const editBtn = smallNote.querySelector('.edit-btn');
            const noteDescriptionEl = smallNote.querySelector('.small-note-desc');

            checkbox.addEventListener('change', function() {
                if (checkbox.checked) {
                    smallNote.classList.add('completed');
                } else {
                    smallNote.classList.remove('completed');
                }
            });

            deleteBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                smallNote.remove();
            });

            editBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                resetForm(); 

                todoTitle.value = titleText;
                todoDescription.value = descText;
                
                if (savedDate) {
                    selectedDate = savedDate;
                    if (dataInput) {
                        dataInput.innerHTML = `
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 16 16" class="data-icon" aria-hidden="true">
                                <path fill="#6194e7" d="M12 2a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm0 1H4a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1m-1.25 7a.75.75 0 1 1 0 1.5.75.75 0 0 1 0-1.5m.75-5a.5.5 0 1 1 0 1h-7a.5.5 0 0 1 0-1z"></path>
                            </svg>
                            ${savedDate}
                        `;
                    }
                }

                if (savedPriority) {
                    selectedPriority = savedPriority;
                    if (priorityInput) {
                        priorityInput.innerHTML = savedPriority.rawHTML;
                        priorityInput.style.color = '#ecf1fb';
                    }
                }
                todoContainer.classList.add('visible');
                smallNote.remove();
            });

            if (noteDescriptionEl) {
                noteDescriptionEl.addEventListener('click', function(e) {
                    e.stopPropagation();
                    const modalOverlay = document.createElement('div');
                    modalOverlay.classList.add('desc-modal-overlay');

                    modalOverlay.innerHTML = `
                        <div class="desc-modal-content">
                            <div class="desc-modal-scroll">${descText || "Описание отсутствует."}</div>
                            <button class="desc-modal-close">Закрыть</button>
                        </div>
                    `;
                    document.body.appendChild(modalOverlay);
                    
                    modalOverlay.querySelector('.desc-modal-close').addEventListener('click', function() {
                        modalOverlay.remove();
                    });
                    
                    modalOverlay.addEventListener('click', function(evt) {
                        if (evt.target === modalOverlay) {
                            modalOverlay.remove();
                        }
                    });
                    fetch('/tasks/create_task' , {
                method: 'POST' , 
                headers: {
                    'Content-Type': 'application/json' , 
                    'accept': 'application/json' , 
                    'Authorization': `Bearer ${token}`
                }, 
                body: JSON.stringify(dataInput , selectPriorityContainer , todoDescription , todoTitle)
            })
                });
            }
            if (notesList) {
                notesList.appendChild(smallNote);
            }
            resetForm();
            todoContainer.classList.remove('visible');
        });
    }
    function getTasks(){
        fetch('/tasks/{tasks_id}' , {
            method: 'GET' , 
            headers: {
            'Content-Type': 'application/json' ,
            'accept': 'application/json' , 
            'Authorization': `Bearer ${token}`
            } , 
            body: JSON.stringify(smallNote , notesList)
        })
    }
    // 6. Логика фильтра (теперь отправляет пустой объект {}, чтобы не вызывать ошибку 422)
    if (filterBtn) {
        filterBtn.addEventListener('click', function() {
            fetch('/tasks', {
                method: 'GET', 
                headers: { 
                'Content-Type': 'application/json' , 
                'accept': 'application/json' ,
                'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(smallNote , notesList , dataInput , todoTitle , todoDescription , selectPriorityContainer)
            })
            .then(res => res.json())
            .then(data => console.log("Фильтр применен:", data))
            .catch(err => console.error("Ошибка фильтрации:", err));
            console.log(res.json())
        });
    }

    // 7. Переключение видимости настроек
    if (settBtn && settCont) {
        settBtn.addEventListener('click', function() {
            settCont.classList.toggle('visible');
        });
    }

    // 8. Отправка формы настроек профиля
    if (settingsForm) {
        settingsForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const msgBox = document.getElementById('message');
            const usernameInput = document.getElementById('username').value.trim();
            const emailInput = document.getElementById('email').value.trim();
            const currentPassword = document.getElementById('currentPassword').value;
            const newPassword = document.getElementById('newPassword').value; 
            const saveBtn = document.querySelector('.save-btn')

            const requestBody = {};
            if (usernameInput !== "") requestBody.new_login = usernameInput;
            if (emailInput !== "") requestBody.new_email = emailInput;
            if (newPassword !== "") requestBody.new_password = newPassword; 

            if (Object.keys(requestBody).length === 0) {
                msgBox.textContent = "Заполните хотя бы одно поле для изменения";
                msgBox.className = "message-box error";
                msgBox.classList.remove('hidden');
                return;
            }

            try {
                msgBox.textContent = "Сохранение изменений...";
                msgBox.className = "message-box";
                msgBox.classList.remove('hidden');

                const response = await fetch("/users/update_profile", {
                    method: "PATCH", 
                    headers: {
                        'Content-Type': 'application/json',
                        'accept': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }, 
                    body: JSON.stringify(usernameInput , emailInput , saveBtn)
                })  
                fetch('/users/update_passwords' , {
                    headers: {
                        'Content-Type': 'application/json' , 
                        'accept': 'application/json' ,
                        'Authorization': `Bearer ${token}`
                    } , 
                    body: JSON.stringify(currentPassword , newPassword , saveBtn)
                })

                if (response.ok) {
                    msgBox.textContent = "Изменения успешно сохранены!";
                    msgBox.className = "message-box success";
                    settingsForm.reset();
                    
                    if (usernameInput) document.getElementById('username').placeholder = `Текущий: ${usernameInput}`;
                    if (emailInput) document.getElementById('email').placeholder = `Текущая: ${emailInput}`;
                } else {
                    msgBox.textContent = result.detail || result.message || "Ошибка при сохранении данных";
                    msgBox.className = "message-box error";
                }
            } catch (error) {
                console.error("Ошибка сети:", error);
                msgBox.textContent = "Не удалось связаться с сервером. Проверьте подключение.";
                msgBox.className = "message-box error";
            }

            setTimeout(() => {
                if(msgBox) msgBox.classList.add('hidden');
            }, 4000);
        });
    }
