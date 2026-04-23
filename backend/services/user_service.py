from repositories.user_repo import UserRepository
from models.user import User
from sqlalchemy import UUID
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from email_validator import validate_email
from core.security import password_hash, verify_pass, get_pass_hash, DUMMY_HASH
from utils.validators import AlreadyTaken, NotFound, ValidationError, InternalServerError, validate_pass

class UserService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.MIN_PASSWORD_LENGTH = 8
        self.MAX_PASSWORD_LENGTH = 72

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await self._get_user_or_raise(user_id)
    
    async def get_user_by_login(self, login: str) -> User | None:
        return await self._get_user_or_raise(login, "login")
    
    async def get_user_by_email(self, email: str) -> User | None:
        return await self._get_user_or_raise(email, "email")

    async def update_profile(self, user_id: UUID,  new_login: str | None = None, new_email: str| None = None):
        if new_login is None and new_email is None:
            raise NotFound(detail="Nothing to update")
        
        user = await self._get_user_or_raise(user_id)

        if new_login and user.login != new_login:
            await self._validate_login(new_login)
            user.login = new_login

        if new_email and user.email != new_email:
            email =  await self._validate_email(new_email)
            user.email = email
        
        try:
            await self.user_repo.commit()
            await self.user_repo.refresh(user)
            return user
                
        except IntegrityError:  
            await self.user_repo.rollback()
            raise AlreadyTaken(detail="Login or email already taken")
        
    async def delete_account(self, user_id: UUID, password: str):
        user = await self._get_user_or_raise(user_id)

        if not password_hash.verify(password, user.hash_pass):
            raise ValidationError(detail="Invalid credentials")
        
        if not await self.user_repo.delete_user(user_id):
            raise InternalServerError(detail="Failed to delete account", status_code=500)
        
        return user
        
    async def change_password(self, user_id: UUID, old_password: str, password: str) -> User:
        user = await self._get_user_or_raise(user_id)
        if not verify_pass(old_password, user.hash_pass):
            verify_pass(old_password, DUMMY_HASH)
            raise ValidationError(detail="Invalid credentials")
        self._validate_new_pass(password, old_password)
        new_pass_hash = get_pass_hash(password)
        user.hash_pass = new_pass_hash
        await self.user_repo.commit()
        return user

    async def validate_new_user(self, login: str, email: str) -> str:
        await self._validate_login(login)  
        return await self._validate_email(email)

    def _validate_new_pass(self, password: str, old_password: str) -> None:
        if password == old_password:
            raise ValidationError(detail="New password must be different")
        validate_pass(password)

    async def _get_user_or_raise(self, identifier: UUID, attribute: str = "user_id") -> User:
        user = await self.user_repo.get_user(getattr(User, attribute), identifier)
        if not user:
            raise NotFound(detail="User not found")
        return user
    
    async def _validate_login(self, login: str) -> None:
        if not login.strip():
            raise ValidationError(detail="Login cant be empty")
        if await self.user_repo.get_user("login", login):
            raise AlreadyTaken(detail="Login already taken")
        
    async def _validate_email(self, email: str) -> str:
        validated_email = validate_email(email)
        if await self.user_repo.get_user("email", validated_email.normalized):
            raise AlreadyTaken(detail="Email already taken")
        return validated_email.normalized