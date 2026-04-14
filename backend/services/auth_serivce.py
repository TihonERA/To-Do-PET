from repositories.user_repo import UserRepository, User
from core.security import get_pass_hash, verify_pass, DUMMY_HASH, create_access_token
from fastapi import HTTPException
from core.config import settings
import jwt
from email_validator import validate_email

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, login: str, email: str, password: str) -> User:
        validated_email = validate_email(email)
        if await self.user_repo.get_user("email", validated_email.normalized):
            raise HTTPException(status_code=409, detail="User with this email already exists")
        if await self.user_repo.get_user("login", login):
            raise HTTPException(status_code=409, detail="User with this login already exists")
        hash_pass = get_pass_hash(password)
        return await self.user_repo.create_user(login, hash_pass, validated_email.normalized)
         
    async def login_user(self, login_or_email: str, password: str) -> dict:
        if "@" in login_or_email and "." in login_or_email:
            user = await self.user_repo.get_user("email", login_or_email)
        else:
            user = await self.user_repo.get_user("login", login_or_email)
        if not user:
            verify_pass(password, DUMMY_HASH)
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not verify_pass(password, user.hash_pass):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": user.login})
        return {"access_token": access_token, "token_type": "bearer"}
    
    async def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        login = payload.get("sub")
        if login is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user = await self.user_repo.get_user("login", login)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user


            
