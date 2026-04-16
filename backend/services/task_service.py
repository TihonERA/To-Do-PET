from repositories.task_repo import TaskRepository
from sqlalchemy import UUID
from models.task import Tasks
from datetime import datetime
from fastapi import HTTPException

class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo
        self.MAX_NAME = 255
        self.MAX_DESC = 500
        self.list_priority = [0, 1, 2]

    # СДЕЛАТЬ КОГДА БУДЕТ ФУНКЦИЯ ПОЛУЧЕНИЯ АКТИВНОГО ПОЛЬЗОВАТЕЛЯ!!!! 
    # def create_task(self, 
    #     name: str, 
    #     user_id: UUID, 
    #     description: str | None = None,
    #     priority: int = 0,
    #     due_data: datetime | None = None
    #     ) -> Tasks:

    async def update_name(self, user_id: UUID, task_id: int, new_name: str) -> Tasks:
        return await self._update_field(
            user_id=user_id,
            task_id=task_id,
            field_name="name",
            value=new_name,
            validator=self._validate_name
        )
    
    async def update_description(self, user_id: UUID, task_id: int, new_desc: str) -> Tasks:
        return await self._update_field(
            user_id=user_id, 
            task_id=task_id, 
            field_name="description", 
            value=new_desc, 
            validator=self._validate_desc
        )

    def _validate_desc(self, description: str) -> None:
        if len(description) > 500:
            raise HTTPException(status_code=400, detail="Description too long")
        
    def _validate_owner(self, task: Tasks | None, user_id: UUID) -> None:
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
    def _validate_name(self, name: str) -> None:
        if not name.strip():
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        if len(name) > 255:
            raise HTTPException(status_code=400, detail="Name too long")
        
    async def _get_task_or_raise(self, task_id: int) -> Tasks:
        task = await self.task_repo.get_task("task_id", task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
        
    async def _validate_priority(self, priority: int) -> None:
        if priority not in self.list_priority:
            raise HTTPException(status_code=400, detail="This type of priority doesn't exist")

    async def _update_field(self, user_id: UUID, task_id: int, field_name: str, value: str, validator: callable | None) -> Tasks:
        if validator:
            validator(value)

        task = await self._get_task_or_raise(task_id)
        
        self._validate_owner(task, user_id)
        
        if getattr(task, field_name) == value:
            return task
        
        setattr(task, field_name, value)
        await self.task_repo.commit()
        return task