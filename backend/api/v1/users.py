from fastapi import APIRouter, Depends, HTTPException, Form
from typing import Annotated
from models.user import User
from services.user_service import UserService
from utils.validators import NotFound, AlreadyTaken, ValidationError, InternalServerError
from schemas.user import UserResponse
from deps import get_current_user, get_user_service

router = APIRouter()

@router.get("/users/me", response_model=UserResponse)
async def get_current_user(
        current_user: Annotated[User, Depends(get_current_user)]    
    ) -> User:
    return current_user

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
    
@router.delete("/delete_account")
async def delete_account(
    current_user: Annotated[User, Depends(get_current_user)],
    password: Annotated[str, Form()],
    user_service: Annotated[UserService, Depends(get_user_service)]
    ) -> User:
    try:
        user_service.delete_account(
            user_id=current_user.user_id,
            password=password
        )
        return {"detail": "Account deleted"}
    except NotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except InternalServerError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
