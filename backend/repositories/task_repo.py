from sqlalchemy.orm import Session
from sqlalchemy import UUID, select, update, delete
from models.task import Tasks
from datetime import datetime

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_task(self, 
        f_name: str, 
        f_userid: UUID, 
        f_description: str | None = None, 
        f_priority: int = 0, 
        f_due_date: datetime | None = None
        ) -> Tasks:
        task = Tasks(name=f_name, user_id=f_userid, description = f_description, priority = f_priority, due_date = f_due_date) 
        self.db.add(task)
        await self.db.commit()
        return task

    async def get_task(self, attribute: str, identifier: UUID | int) -> Tasks | None:
        stmt = (
            select(Tasks)
            .where(getattr(Tasks, attribute) == identifier)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def update_task(self, 
        task_id: int, 
        attribute: str,
        newvalue: int | str | datetime
        ) -> bool:
        stmt = (
            update(Tasks)
            .where(Tasks.tasks_id == task_id)
            .values({attribute: newvalue})
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return True if result.rowcount == 1 else False
    
    async def delete_task(self, attribute: str, id: int | UUID) -> bool:
        stmt = (
            delete(Tasks)
            .where(getattr(Tasks, attribute) == id)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return True if result.rowcount == 1 else False
    
    async def commit(self) -> None:
        await self.db.commit()
    
    async def refresh(self, instance: object) -> None:
        await self.db.refresh(instance)

    async def rollback(self) -> None:
        await self.db.rollback()