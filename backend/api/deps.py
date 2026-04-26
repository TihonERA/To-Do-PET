from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from backend.services.user_service import UserService
from backend.services.auth_serivce import AuthService
from backend.services.task_service import TaskService
from backend.repositories.task_repo import TaskRepository
from backend.repositories.user_repo import UserRepository
from backend.core.config import settings
from backend.core.database import get_db
from backend.utils.validators import NotFound
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_repo(db: AsyncSession = Depends(get_db)):
    return UserRepository(db=db)

def get_task_repo(db: Annotated[AsyncSession, Depends(get_db)]):
    return TaskRepository(db=db)

def get_user_service(user_repo: UserRepository = Depends(get_user_repo)):
    return UserService(user_repo=user_repo)

def get_task_service(task_repo: Annotated[TaskRepository, Depends(get_task_repo)]):
    return TaskService(task_repo=task_repo)

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
        