const CreateToDo = document.querySelector('.create');
        const ContainerToDo = document.querySelector('.create-container');
        const CloseToDo = document.querySelector('.offwind');
        const addButton = document.querySelector('.add');
        const miniContainer = document.querySelector('.mini-container');
        const completedContainer = document.querySelector('.completed-container');
        const nameInput = document.querySelector('.name');
        const descInput = document.querySelector('.description');
        const timeInput = document.querySelector('.time');
        const prioritySelect = document.querySelector('select[name="priority"]');
        const descModal = document.getElementById('descModal');
        const descModalTextarea = document.getElementById('descModalTextarea');
        const saveDescBtn = document.getElementById('saveDescBtn');
        const cancelDescBtn = document.getElementById('cancelDescBtn');
        const settInput = document.querySelector('.sett');
        const settOpen = document.querySelector('.settings-container');
        const closeSett = document.querySelector('.offsett')
        const delAcc = document.querySelector('.delete')

        let notes = [];
        let editId = null;
        let currentDescNoteId = null;   

        function getFormData() {
            return {
                title: nameInput.value.trim(),
                description: descInput.value.trim(),
                deadline: timeInput.value,
                priority: prioritySelect.value === 'pri' ? 'Mid' : prioritySelect.value
            };
        }

        function fillForm(note) {
            nameInput.value = note.title;
            descInput.value = note.description;
            timeInput.value = note.deadline || '';
            prioritySelect.value = note.priority;
        }

        function resetForm() {
            nameInput.value = '';
            descInput.value = '';
            timeInput.value = '';
            prioritySelect.value = 'pri';
            editId = null;
            addButton.textContent = 'Добавить заметку';
            ContainerToDo.classList.remove('active');
        }

        function priorityText(priority) {
            if (priority === 'High') return 'Высокий';
            if (priority === 'Mid') return 'Средний';
            return 'Низкий';
        }

        function escapeHtml(str) {
            if (!str) return '';
            return str.replace(/[&<>]/g, function(m) {
                if (m === '&') return '&amp;';
                if (m === '<') return '&lt;';
                if (m === '>') return '&gt;';
                return m;
            });
        }

        function createNoteCard(note) {
            const card = document.createElement('div');
            card.className = 'note-card';
            card.dataset.id = note.id;
            card.innerHTML = `
                <label class="complete-label">
                    <input type="checkbox" class="complete-checkbox" 
                           ${note.completed ? 'checked' : ''}>
                </label>
                ${escapeHtml(note.title)}
                <strong><div class="note-description" data-desc-id="${note.id}">${escapeHtml(note.description) || ''}</div></strong>
                <small> Срок: ${note.deadline ? new Date(note.deadline).toLocaleString() : 'Без срока'}</small>
                <div><span class="priority ${note.priority}">${priorityText(note.priority)}</span></div>
                <div style="margin-top: 10px;">
                    <button class="edit-note"><svg class="icon-desc" viewBox="0 0 24 24" width="15" height="15" stroke="black" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg> Редактировать</button>
                    <button class="delete-note"><svg class="icon-del" viewBox="0 0 24 24" width="15" height="15" stroke="black" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg> Удалить</button>
                </div>
            `;
            if (note.completed) {
                card.classList.add('completed');
            }
            return card;
        }

        function renderNotes() {
            miniContainer.innerHTML = '';
            completedContainer.innerHTML = '';

            if (notes.length === 0) {
                completedContainer.style.display = 'none';
                return;
            }

            const activeNotes = notes.filter(n => !n.completed);
            const completedNotes = notes.filter(n => n.completed);

            // Активные заметки
            activeNotes.forEach(note => {
                miniContainer.appendChild(createNoteCard(note));
            });

            // Выполненные заметки
            if (completedNotes.length > 0) {
                completedContainer.style.display = 'flex';
                completedNotes.forEach(note => {
                    completedContainer.appendChild(createNoteCard(note));
                });
            } else {
                completedContainer.style.display = 'none';
            }
        }

        function openDescModal(noteId) {
            const note = notes.find(n => n.id === noteId);
            if (!note) return;
            currentDescNoteId = noteId;
            descModalTextarea.value = note.description;
            descModal.style.display = 'flex';
        }

        function closeDescModal() {
            descModal.style.display = 'none';
            currentDescNoteId = null;
        }

        function saveDescFromModal() {
            if (currentDescNoteId === null) return;
            const newDesc = descModalTextarea.value.trim();
            const noteIndex = notes.findIndex(n => n.id === currentDescNoteId);
            if (noteIndex !== -1) {
                notes[noteIndex].description = newDesc;
                renderNotes();
            }
            closeDescModal();
        }

        CreateToDo.addEventListener('click', function(e) {
            e.preventDefault();
            resetForm();
            ContainerToDo.classList.add('active');
        });

        CloseToDo.addEventListener('click', () => {
            resetForm();
        });

        addButton.addEventListener('click', (e) => {
            e.preventDefault();
            const { title, description, deadline, priority } = getFormData();
            
            if (!title) {
                alert('Введите название');
                return;
            }
            if (!deadline) {
                alert('Выберите срок выполнения');
                return;
            }
            if (prioritySelect.value === 'pri') {
                alert('Выберите приоритет');
                return;
            }
            
            if (editId === null) {
                const newNote = {
                    id: Date.now(),
                    title,
                    description,
                    deadline,
                    priority,
                    completed: false
                };
                notes.push(newNote);
            } else {
                const index = notes.findIndex(n => n.id === editId);
                if (index !== -1) {
                    notes[index] = { 
                        ...notes[index], 
                        title, 
                        description, 
                        deadline, 
                        priority,
                        completed: notes[index].completed || false
                    };
                }
            }
            
            renderNotes();
            resetForm();
        });

        // Единый обработчик кликов для обоих контейнеров
        document.addEventListener('click', (e) => {
            // Обработка чекбокса
            if (e.target.classList.contains('complete-checkbox')) {
                const card = e.target.closest('.note-card');
                if (!card) return;
                const id = parseInt(card.dataset.id);
                const note = notes.find(n => n.id === id);
                if (note) {
                    note.completed = e.target.checked;
                    renderNotes();   // задачки переместятся
                }
                return;
            }

            // Клик по описанию
            const descBlock = e.target.closest('.note-description');
            if (descBlock) {
                e.stopPropagation();
                const noteId = parseInt(descBlock.dataset.descId);
                if (!isNaN(noteId)) openDescModal(noteId);
                return;
            }

            const card = e.target.closest('.note-card');
            if (!card) return;
            const id = parseInt(card.dataset.id);
            const note = notes.find(n => n.id === id);
            if (!note) return;

            // Кнопка "Редактировать"
            if (e.target.classList.contains('edit-note') || e.target.closest('.edit-note')) {
                fillForm(note);
                editId = id;
                addButton.textContent = 'Сохранить изменения';
                ContainerToDo.classList.add('active');
            }

            // Кнопка "Удалить"
            if (e.target.classList.contains('delete-note') || e.target.closest('.delete-note')) {
                if (confirm('Удалить заметку?')) {
                    notes = notes.filter(n => n.id !== id);
                    if (editId === id) resetForm();
                    renderNotes();
                }
            }
        });

        saveDescBtn.addEventListener('click', saveDescFromModal);
        cancelDescBtn.addEventListener('click', closeDescModal);
        window.addEventListener('click', (e) => {
            if (e.target === descModal) closeDescModal();
        });

        settInput.addEventListener('click', (e) => {
        e.preventDefault(); 
        resetForm();
        settOpen.classList.add('active');
        });

        closeSett.addEventListener('click' , () => {
            resetForm()
            settOpen.classList.remove('active')
        });
        let alertShown = false;

        delAcc.addEventListener('click', () => {
            if (alertShown)
                return 
            alert('Вы точно хотите удалить аккаунт?')
            alertShown = true;
        })
/*Получаем данные почты с страницы регистрации */
        const url = 'http://localhost:8000/registration/get-email';
        fetch(url)
            .then(response => response.json())  
            .then(data => {
                document.querySelector('.email').innerText = data.email;
            })
/*Получаем данные почты с страницы логина */
        const urlhome = 'http://localhost:8000/login/get-email';
        fetch(urlhome) 
        .then(response => responce.json())
        .then(data =>{
            document.querySelector('.email').innerText =data.email;
        })
        const LogChangeContainer = document.querySelector('.log-change-container') 
        const LogSubmit = document.querySelector('.confirm-log')
        const ChangeLog = document.querySelector('.change-login')
        const offLog = document.querySelector('.offlog')

        ChangeLog.addEventListener('click' , (e) => {
            e.preventDefault(); 
            resetForm(); 
            settOpen.classList.remove('active')
            LogChangeContainer.classList.add('active')
        })
        offLog.addEventListener('click' , () => {
            resetForm() 
            LogChangeContainer.classList.remove('active')
            settOpen.classList.add('active')
        })
        const PassChangeContainer = document.querySelector('.pass-change-container')
        const PassSubmit = document.querySelector('.confirm-pass') 
        const ChangePass = document.querySelector('.change-pass') 
        const offPass = document.querySelector('.offpass') 

        ChangePass.addEventListener('click' , (e) =>{
            e.preventDefault() 
            resetForm() 
            settOpen.classList.remove('active') 
            PassChangeContainer.classList.add('active')
        }) 
        offPass.addEventListener('click' , () =>{
            resetForm() 
            PassChangeContainer.classList.remove('active') 
            settOpen.classList.add('active')
        })
        
        const EmailChangeContainer = document.querySelector('.email-change-container') 
        const EmailSubmit = document.querySelector('.confirm-email') 
        const ChangeEmail = document.querySelector('.change-email') 
        const offEmail = document.querySelector('.offemail') 

        ChangeEmail.addEventListener('click' , (e) =>{
            e.preventDefault() 
            resetForm() 
            settOpen.classList.remove('active') 
            EmailChangeContainer.classList.add('active')
        }) 

        offEmail.addEventListener('click' , () =>{
            resetForm() 
            EmailChangeContainer.classList.remove('active') 
            settOpen.classList.add('active')
        })

        const msgDiv = document.querySelector('.message');

  PassChangeContainer.addEventListener('submit', async (e) => {
    e.preventDefault();

    const oldPass = document.querySelector('.pass-old').value;
    const newPass = document.querySelector('.pass-new').value;
    const confirmPass= document.querySelector('confirm-pass').value;

    // Валидация 
    if (!oldPass || !newPass || !confirmPass) {
      msgDiv.innerText = 'Заполните все поля';
      return;
    }
    if (newPass.length < 6) {
      msgDiv.innerText = 'Новый пароль должен быть не менее 6 символов';
      return;
    }
    if (newPass !== confirmPass) {
      msgDiv.innerText = 'Новый пароль и подтверждение не совпадают';
      return;
    }

    // === Отправка на сервер ===
    try {
      const response = await fetch('/users/update_password', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ oldPass, newPass })
      });

      const result = await response.json();

      if (response.ok) {
        msgDiv.innerText = result.message || 'Пароль успешно изменён'
        form.reset();       // очистить форму
      } else {
        msgDiv.innerText = result.message || 'Ошибка при смене пароля'
      }
    } catch (error) {
      msgDiv.innerText = 'Ошибка сети: ' + error.message;
    }
  })

const msgDivEmail = document.querySelector('.email-message');
  EmailChangeContainer.addEventListener('submit', async (e) => {
    e.preventDefault();

    const oldEmail = document.querySelector('.email-old').value;
    const newEmail = document.querySelector('.email-new').value;
    const confirmEmail= document.querySelector('confirm-email').value;

    if (!oldEmail || !newEmail || !confirmEmail) {
      msgDivEmail.innerText = 'Заполните все поля';
      return;
    }
    
    if (newEmail !== confirmEmail) {
      msgDivEmail.innerText = 'Новая почта и подтверждение не совпадают';
      return;
    }

    try {
      const response = await fetch('/users/update_email', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ oldEmail, newEmail })
      });

      const resultEmail = await response.json();

      if (response.ok) {
        msgDivEmail.innerText = resultEmail.email-message || 'Почта успешно заменена'
        form.reset();       // очистить форму
      } else {
        msgDivEmail.innerText = resultEmail.email-message || 'Ошибка при смене почты'
      }
    } catch (error) {
      msgDivEmail.innerText = 'Ошибка сети: ' + error.email-message;
    }
  })
    const msgDivLog = document.querySelector('.log-message');

    LogChangeContainer.addEventListener('submit', async (e) => {
    e.preventDefault();

    const oldLog = document.querySelector('.log-old').value;
    const newLog = document.querySelector('.log-new').value;
    const confirmLog= document.querySelector('confirm-log').value;

    // Валидация 
    if (!oldLog || !newLog || !confirmLog) {
      msgDivLog.innerText = 'Заполните все поля';
      return;
    }
    if(!newLog.length < 8) {
        msgDivLog.innerText = 'Новый логин должен быть не менее 8 символов'
        return
    }
    if (newLog !== confirmLog) {
      msgDivLog.innerText = 'Новый логин и подтверждение не совпадают';
      return;
    }

    try {
      const response = await fetch('/users/update_login', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ oldLog, newLog })
      });

      const resultLog = await response.json();

      if (response.ok) {
        msgDivLog.innerText = resultLog.log-message || 'Почта успешно заменена'
        form.reset();       // очистить форму
      } else {
        msgDivLog.innerText = resultLog.log-message || 'Ошибка при смене почты'
      }
    } catch (error) {
      msgDivLog.innerText = 'Ошибка сети: ' + error.log-message;
    }
  })
  const filterChooseContainer = document.querySelector('.filter-choose-container') 
  const filterOpen = document.querySelector('.fil')
  
  filterOpen.addEventListener('click', (event) => {
        event.stopPropagation(); // чтобы клик не закрыл меню сразу
        const isVisible = filterChooseContainer.style.display === 'block';
        filterChooseContainer.style.display = isVisible ? 'none' : 'block';
    });
    document.addEventListener('click', () => {
        filterChooseContainer.style.display = 'none';
    });
    filterChooseContainer.addEventListener('click', (event) => {
        event.stopPropagation();
    });
    const originalRenderNotes = renderNotes;


let sortMode = null;

function sortByPriority(arr) {
    const order = { 'High': 1, 'Mid': 2, 'Low': 3 };
    return [...arr].sort((a, b) => (order[a.priority] || 2) - (order[b.priority] || 2));
}

function sortByDeadline(arr) {
    return [...arr].sort((a, b) => {
        if (!a.deadline && !b.deadline) return 0;
        if (!a.deadline) return 1;
        if (!b.deadline) return -1;
        return new Date(a.deadline) - new Date(b.deadline);
    });
}
renderNotes = function() {
    let activeNotes = notes.filter(n => !n.completed);
    let completedNotes = notes.filter(n => n.completed);

    if (sortMode === 'priority') {
        activeNotes = sortByPriority(activeNotes);
        completedNotes = sortByPriority(completedNotes);
    } else if (sortMode === 'deadline') {
        activeNotes = sortByDeadline(activeNotes);
        completedNotes = sortByDeadline(completedNotes);
    }
    
    miniContainer.innerHTML = '';
    completedContainer.innerHTML = '';

    if (notes.length === 0) {
        completedContainer.style.display = 'none';
        return;
    }
    activeNotes.forEach(note => {
        miniContainer.appendChild(createNoteCard(note));
    });
    if (completedNotes.length > 0) {
        completedContainer.style.display = 'flex';
        completedNotes.forEach(note => {
            completedContainer.appendChild(createNoteCard(note));
        });
    } else {
        completedContainer.style.display = 'none';
    }
};

document.querySelector('.filter-priority')?.addEventListener('click', () => {
    sortMode = sortMode === 'priority' ? null : 'priority';
    renderNotes();
    document.querySelector('.filter-choose-container').style.display = 'none';
});

document.querySelector('.filter-time')?.addEventListener('click', () => {
    sortMode = sortMode === 'deadline' ? null : 'deadline';
    renderNotes();
    document.querySelector('.filter-choose-container').style.display = 'none';
});