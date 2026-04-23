from fastapi import APIRouter, Depends, HTTPException, Form
from models.user import User
from typing import Annotated
from services.user_service import UserService
from services.auth_serivce import AuthService
from repositories.user_repo import UserRepository
from core.config import settings
from core.security import create_access_token
from core.database import get_db
from utils.validators import AlreadyTaken, NotFound, ValidationError, InvalidCredentialsError, InternalServerError
from schemas.user import Token, UserResponse
from sqlalchemy import UUID
from deps import get_current_user
import jwt
from deps import get_user_auth_service, get_user_service
import uvicorn


router = APIRouter()

@router.post("/register", response_model=Token)
async def register(
    email: Annotated[str, Form()], 
    login: Annotated[str, Form()], 
    password: Annotated[str, Form()], 
    user_auth: Annotated[AuthService, Depends(get_user_auth_service)]
    ) -> Token:
    try:
        token = await user_auth.register_user(login, email, password)
    except AlreadyTaken as e:
        raise HTTPException(status_code=409, detail=e.detail)
    return token

@router.post("/login", response_model=Token)
async def login(
    login_or_email: Annotated[str, Form()], 
    password: Annotated[str, Form()],
    user_auth: Annotated[AuthService, Depends(get_user_auth_service)]
    ) -> Token:
    try:
        token = await user_auth.login_user(login_or_email, password)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return token

@router.patch("/update_profile", response_model=UserResponse)
async def update_profile(
    new_login: Annotated[str | None, Form()],
    new_email: Annotated[str | None, Form()],
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)]
    ) -> UserResponse:
    try:
        return await user_service.update_profile(
            user_id=current_user.user_id,
            new_login=new_login,
            new_email=new_email
        )
    except NotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except AlreadyTaken as e:
        raise HTTPException(status_code=409, detail=e.detail)
    
@router.patch("/update_password")
async def update_password(
    old_password: Annotated[str, Form()],
    new_password: Annotated[str, Form()],
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)]
    ) -> dict:
    try:
        await user_service.change_password(
            user_id=current_user.user_id,
            old_password=old_password,
            password=new_password
        )
        return {"detail": "Password successfully changed"}
    except NotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    
@router.post("/delete_account")
async def delete_account(
    current_user: Annotated[User, Depends(get_current_user)],
    password: Annotated[str, Form()],
    user_service: Annotated[UserService, Depends(get_user_service)]
    ) -> User:
    try:
        return user_service.delete_account(
            user_id=current_user.user_id,
            password=password
        )
    except NotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except InternalServerError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)