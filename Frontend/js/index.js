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