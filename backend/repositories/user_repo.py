from sqlalchemy.orm import Session
from sqlalchemy import UUID, select
from models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    async def create_user(self, f_login: str, f_hash_pass: str, f_email: str) -> User:
        user = User(login=f_login, hash_pass=f_hash_pass, email=f_email)
        self.db.add(user)
        await self.db.commit()
        await self.db.close()
        return user
    
    async def _get_user(self, column: str, argument: UUID | str) -> User | None:
        stmt = select(User).where(getattr(User, column) == argument)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()
    
    async def get_user_byid(self, uuid: UUID) -> User | None:
        return await self._get_user(column="user_id", argument=uuid)
    
    async def get_user_bylogin(self, f_login: str) -> User | None:
        return await self._get_user(column="login", argument=f_login)
    
    async def get_user_byemail(self, f_email: str) -> User | None:
        return await(self._get_user(column="email", argument=f_email))