from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from services.user_service import UserService
from services.auth_serivce import AuthService
from repositories.user_repo import UserRepository
from core.config import settings
from core.database import get_db
from utils.validators import NotFound
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_repo(db: AsyncSession = Depends(get_db)):
    return UserRepository(db=db)

def get_user_service(user_repo: UserRepository = Depends(get_user_repo)):
    return UserService(user_repo=user_repo)

def get_user_auth_service(user_repo: Annotated[UserRepository, Depends(get_user_repo)]):
    return AuthService(user_repo=user_repo)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_service: Annotated[UserService, Depends(get_user_service)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        login = payload.get("sub")
        user = await user_service.get_user_by_login(login)
    except jwt.PyJWTError: 
        raise HTTPException(401, "Invalid token")
    except NotFound as e:
        raise HTTPException(404, detail=e.detail)
    return user
        