from repositories.user_repo import UserRepository
from sqlalchemy import UUID
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from email_validator import validate_email

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def update_profile(self, uuid: UUID,  new_login: str | None = None, new_email: str| None = None):
        if new_login is None and new_email is None:
            raise HTTPException(status_code=400, detail="Nothing to update")
        user = await self.user_repo.get_user("user_id", uuid)
        if not user:
            raise HTTPException(
                status_code=500,
                detail="User from token not found in database. Data inconsistency detected."
            )
        updated = False

        if new_login and user.login != new_login:
            if await self.user_repo.get_user("login", new_login):
                raise HTTPException(status_code=409, detail="Login already taken")
            user.login = new_login
            updated = True

        if new_email and user.email != new_email:
            email = validate_email(new_email)
            if await self.user_repo.get_user("email", email.normalized):
                raise HTTPException(status_code=409, detail="Email already taken")
            user.email = email.normalized
            updated=True
        
        if not updated:
            raise HTTPException(status_code=400, detail="No changes to apply")
        
        try:
            await self.user_repo.db.commit()
            await self.user_repo.db.refresh(user)
            return user
        except IntegrityError:  
            await self.user_repo.db.rollback()
            raise HTTPException(409, "Login or email already taken")