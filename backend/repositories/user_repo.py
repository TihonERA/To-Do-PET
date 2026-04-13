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
    
    async def get_user(self, attribute: str, argument: UUID | str) -> User | None:
        stmt = select(User).where(getattr(User, attribute) == argument)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()