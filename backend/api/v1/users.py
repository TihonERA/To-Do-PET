from fastapi import APIRouter, Depends, HTTPException, Form
from typing import Annotated
from backend.models.user import User
from backend.services.user_service import UserService
from backend.utils.validators import NotFound, AlreadyTaken, ValidationError, InternalServerError
from backend.schemas.user import UserResponse, UserUpdateProfile, UserUpdatePassword, UserDeleteAccount
from backend.api.deps import get_current_user, get_user_service

router = APIRouter(tags=["User"])

@router.get("/users/me", response_model=UserResponse)
async def get_current_user(
        current_user: Annotated[User, Depends(get_current_user)]    
    ):
    return current_user

@router.patch("/users/update_profile", response_model=UserResponse)
async def update_profile(
    data: UserUpdateProfile,
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)]
    ) -> UserResponse:
    try:
        return await user_service.update_profile(
            user_id=current_user.user_id,
            new_login=data.new_login,
            new_email=data.new_email
        )
    except NotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except AlreadyTaken as e:
        raise HTTPException(status_code=409, detail=e.detail)
    
@router.patch("/users/update_password")
async def update_password(
    data: UserUpdatePassword,
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)]
    ) -> dict:
    try:
        await user_service.change_password(
            user_id=current_user.user_id,
            old_password=data.old_password,
            password=data.new_password
        )
        return {"detail": "Password successfully changed"}
    except NotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    
@router.delete("/users/delete_account")
async def delete_account(
    data: UserDeleteAccount,
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)]
    ):
    try:
        user_service.delete_account(
            user_id=current_user.user_id,
            password=data.password
        )
        return {"detail": "Account deleted"}
    except NotFound as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except InternalServerError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
