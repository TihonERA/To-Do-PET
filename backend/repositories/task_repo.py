from sqlalchemy.orm import Session
from sqlalchemy import UUID, select, update, delete
from backend.models.task import Tasks
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
    
    async def get_all_by_user(self, 
            user_id: UUID,
            skip: int = 0,
            limit: int = 100,
            sort_by: str = "created",
            sort_desc: bool = True,
            status: bool | None = None,
            priority: int | None = None
        ) -> list[Tasks]:
        stmt = (
            select(Tasks)
            .where(Tasks.user_id == user_id)
        )

        if status is not None:
            stmt = stmt.where(Tasks.status == status)

        if priority is not None:
            stmt = stmt.where(Tasks.priority == priority)

        if sort_desc:
            stmt = stmt.order_by(getattr(Tasks, sort_by).desc())
        else:
            stmt = stmt.order_by(getattr(Tasks, sort_by).asc())

        stmt = stmt.offset(skip).limit(limit)

        result = await self.db.execute(stmt)
        return result.scalars().all()


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