from fastapi import APIRouter, Depends, HTTPException, Form
from models.user import User
from typing import Annotated
from services.user_service import UserService
from services.auth_serivce import AuthService
from repositories.user_repo import UserRepository
from core.config import settings
from core.security import create_access_token
from core.database import get_db
from utils.validators import AlreadyTaken, NotFound, ValidationError, InvalidCredentialsError
from schemas.user import Token
import jwt
from deps import get_user_auth_service
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