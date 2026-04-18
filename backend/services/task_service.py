from repositories.task_repo import TaskRepository
from sqlalchemy import UUID
from models.task import Tasks
from datetime import datetime, timezone
from fastapi import HTTPException

class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo
        self.MAX_NAME = 255
        self.MAX_DESC = 500
        self.list_priority = [0, 1, 2]
        self.ALLOWED_SORT_FIELDS = {"created", "priority", "due_date", "name", "status", "tasks_id"}
        self.MAX_LIMIT = 500
        self.MIN_LIMIT = 1

    async def create_task(self, 
            name: str, 
            user_id: UUID, # получается из current_user, который будет написан в api
            description: str | None = None,
            priority: int = 0,
            due_date: datetime | None = None
        ) -> Tasks:
        self._validate_name(name)
        self._validate_desc(description)
        self._validate_priority(priority)
        self._validate_due_date(due_date)

        task = await self.task_repo.create_task(f_name=name, 
            f_userid=user_id, 
            f_description=description,
            f_priority=priority,
            f_due_date=due_date
        )

        await self.db.refresh(task)
        return task
    
    async def get_task(self, 
            user_id: UUID, 
            task_id: int
        ) -> Tasks:
        task = await self._get_task_or_raise(task_id)

        self._validate_owner(task, user_id)

        return task
    
    async def get_all_task(self,
            user_id: UUID,
            skip: int = 0,
            limit: int = 100,
            sort_by: str = "created",
            sort_desc: bool = True,
            status: bool | None = None,
            priority: int | None = None                      
        ) -> list[Tasks]:

        if sort_by not in self.ALLOWED_SORT_FIELDS:
            raise HTTPException(
                400, 
                f"Invalid sort field. Allowed: {self.ALLOWED_SORT_FIELDS}"
            )
        self._validate_pagination(skip, limit)
        self._validate_priority(priority)

        return await self.task_repo.get_all_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_desc=sort_desc,
            status=status,
            priority=priority
        )
        
    async def set_completed(self,
            user_id: UUID,
            task_id: int
        ) -> Tasks:
        return await self._set_time(
            user_id,
            task_id
        )

    async def switch_status(self, 
            user_id: UUID,
            task_id: int
        ) -> Tasks:
        return await self._switch_status(
            user_id,
            task_id
        )

    async def update_name(self, 
            user_id: UUID, 
            task_id: int, 
            new_name: str
        ) -> Tasks:
        return await self._update_field(
            user_id=user_id,
            task_id=task_id,
            field_name="name",
            value=new_name,
            validator=self._validate_name
        )
    
    async def update_description(self, 
            user_id: UUID, 
            task_id: int, 
            new_desc: str
        ) -> Tasks:
        return await self._update_field(
            user_id=user_id, 
            task_id=task_id, 
            field_name="description", 
            value=new_desc, 
            validator=self._validate_desc
        )

    async def delete_task(self,
            user_id: UUID,
            task_id: int
        ) -> Tasks:
        task = await self._get_task_or_raise(task_id)

        self._validate_owner(task, user_id)

        await self.task_repo.delete_task("task_id", task_id)
        return task
    
    def _validate_desc(self, description: str | None) -> None:
        if description is None:
            return None
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
    
    def _validate_pagination(self, skip: int, limit: int) -> None:
        if skip < 0:
            raise HTTPException(400, "Skip cannot be negative")
        if limit < self.MIN_LIMIT or limit > self.MAX_LIMIT:
            raise HTTPException(400, f"Limit must be between {self.MIN_LIMIT} and {self.MAX_LIMIT}")
        
    def _validate_priority(self, priority: int) -> None:
        if priority not in self.list_priority:
            raise HTTPException(status_code=400, detail="This type of priority doesn't exist")

    async def _update_field(self, user_id: UUID, task_id: int, field_name: str, value: str, validator: callable | None) -> Tasks:
        validator(value)

        task = await self._get_task_or_raise(task_id)
        
        self._validate_owner(task, user_id)
        
        if getattr(task, field_name) == value:
            return task
        
        setattr(task, field_name, value)
        await self.task_repo.commit()
        return task
    
    async def _switch_status(self, user_id: UUID, task_id: int):
        task = await self._get_task_or_raise(task_id)

        self._validate_owner(task, user_id)

        status = task.status

        task.status = True if status == False else False
        await self.task_repo.commit()
        return task
    
    async def _set_time(self,
            user_id: UUID,
            task_id: int
        ) -> Tasks:
        task = await self._get_task_or_raise(task_id)

        self._validate_owner(task, user_id)

        task.completed = datetime.now(timezone.utc)
        await self.task_repo.commit()
        return task
    
    def _validate_due_date(self, due_date: datetime | str | None) -> datetime | None:
        if due_date is None:
            return None
        
        if isinstance(due_date, str):
            try:
                due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(400, "Invalid date format. Use ISO 8601")
            
        now = datetime.now(timezone.utc)
        if due_date < now:
            raise HTTPException(400, "Due date cannot be in the past")
        
        max_future = now.replace(year=now.year + 1)
        if due_date > max_future:
            raise HTTPException(400, "Due date cannot be more than 1 years in the future")
        
        return due_date