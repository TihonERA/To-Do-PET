from fastapi import APIRouter, Depends, HTTPException, Form
from typing import Annotated
from backend.services.auth_serivce import AuthService
from backend.utils.validators import AlreadyTaken, InvalidCredentialsError
from backend.schemas.user import Token, UserLogin, UserRegister
from backend.api.deps import get_user_auth_service


router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=Token)
async def register(
    data: UserRegister, 
    user_auth: Annotated[AuthService, Depends(get_user_auth_service)]
    ) -> Token:
    try:
        token = await user_auth.register_user(data.login, data.email, data.password)
    except AlreadyTaken as e:
        raise HTTPException(status_code=409, detail=e.detail)
    return token

@router.post("/login", response_model=Token)
async def login(
    data: UserLogin,
    user_auth: Annotated[AuthService, Depends(get_user_auth_service)]
    ) -> Token:
    try:
        token = await user_auth.login_user(data.login_or_email, data.password)
        return token
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
