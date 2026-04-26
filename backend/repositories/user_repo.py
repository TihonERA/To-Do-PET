from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import UUID, select, update, delete
from backend.models.user import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, f_login: str, f_hash_pass: str, f_email: str) -> User:
        user = User(login=f_login, hash_pass=f_hash_pass, email=f_email)
        self.db.add(user)
        await self.db.commit()
        return user
    
    async def get_user(self, attribute: str, argument: UUID | str) -> User | None:
        stmt = select(User).where(getattr(User, attribute) == argument)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()
    
    # async def update_user(self, attribute: str, olddata: UUID | str, newdata: str) -> bool:
    #     stmt = (
    #         update(User)
    #         .where(getattr(User, attribute) == olddata)
    #         .values({attribute: newdata})
    #     )
    #     result = await self.db.execute(stmt)
    #     await self.db.commit()
    #     return True if result.rowcount == 1 else False

        
    async def delete_user(self, pk_uuid: UUID) -> bool:
        stmt = (
            delete(User)
            .where(User.user_id == pk_uuid)
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