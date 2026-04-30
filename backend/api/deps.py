from fastapi import Depends, HTTPException, Query
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
from backend.schemas.task import TaskFilterParams
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_task_filters(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    sort_by: str = Query("created"),
    sort_desc: bool = Query(True),
    status: Optional[bool] = Query(None),
    priority: Optional[int] = Query(None, ge=0, le=3)
) -> TaskFilterParams:
    return TaskFilterParams(
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_desc=sort_desc,
        status=status,
        priority=priority
    )

def get_user_repo(db: AsyncSession = Depends(get_db)):
    return UserRepository(db=db)

def get_task_repo(db: Annotated[AsyncSession, Depends(get_db)]):
    return TaskRepository(db=db)

def get_user_service(user_repo: UserRepository = Depends(get_user_repo)):
    return UserService(user_repo=user_repo)

def get_task_service(task_repo: Annotated[TaskRepository, Depends(get_task_repo)]):
    return TaskService(task_repo=task_repo)

def get_user_auth_service(user_serv: Annotated[UserService, Depends(get_user_service)]):
    return AuthService(user_serv=user_serv)

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
        