const modal = document.getElementById('modal');
const openModalBtn = document.getElementById('openModalBtn');
const cancelBtn = document.getElementById('cancelBtn');
const addNoteBtn = document.getElementById('addNoteBtn');
const noteTextarea = document.getElementById('noteText');
const notesContainer = document.getElementById('notesContainer');

// Открыть модальное окно
openModalBtn.addEventListener('click', () => {
  modal.style.display = 'flex';
  noteTextarea.value = ''; // очистить поле при открытии
});

// Закрыть по кнопке "Отмена"
cancelBtn.addEventListener('click', () => {
  modal.style.display = 'none';
});

// Добавить заметку
addNoteBtn.addEventListener('click', () => {
  const text = noteTextarea.value.trim();
  if (text === '') {
    alert('Введите текст заметки');
    return;
  }

  // Создаём элемент мини-заметки
  const noteItem = document.createElement('div');
  noteItem.className = 'note-item';
  noteItem.textContent = text; // текст из textarea

  // (Опционально) добавить кнопку удаления
  const deleteBtn = document.createElement('button');
  deleteBtn.textContent = '✖';
  deleteBtn.onclick = () => noteItem.remove();
  noteItem.appendChild(deleteBtn);

  // Добавляем в контейнер
  notesContainer.appendChild(noteItem);

  // Закрываем модальное окно
  modal.style.display = 'none';
});

// Закрыть модальное окно при клике вне его содержимого
window.addEventListener('click', (e) => {
  if (e.target === modal) modal.style.display = 'none';
});