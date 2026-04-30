from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr = Field(description="Почта")
    login: str = Field(min_length=3, max_length=50, description="Логин")
    password: str = Field(min_length=16, max_length=72, description="Пароль")
    class Config:
        schema_extra = {
            "example": {
                "email": "pytest@gmail.com",
                "login": "pytest_user",
                "password": "pytestpassword15"
            }
        }

class UserLogin(BaseModel):
    login_or_email: str | EmailStr = Field(description="Принимает логин или пароль для авторизации пользователя")
    password: str = Field(min_length=16, max_length=72, description="пароль")
    class Config:
        schema_extra = {
            "example": {
                "login_or_email": "pytest_user",
                "password": "pytestpassword15"
            }
        }

class UserUpdateProfile(BaseModel):
    new_login: str | None = Field(
        default=None,
        min_length=3, 
        max_length=50, 
        description="Новый логин"
    )
    new_email: EmailStr | None = Field(default=None, description="Новая почта")

class UserUpdatePassword(BaseModel):
    old_password: str = Field(min_length=16, max_length=72, description="Пользователь должен ввести старый пароль")
    new_password: str = Field(min_length=16, max_length=72, description="Пользователь должен ввести новый пароль")

class UserDeleteAccount(BaseModel):
    password: str = Field(min_length=16, max_length=72, description="Пользователь должен ввести свой пароль чтоб удалить свой аккаунт")

class UserResponse(BaseModel):
    user_id: UUID = Field(description="Уникальный идентификатор пользователя")
    login: str = Field(min_length=3, max_length=50, description="Логин пользователя")
    email: str = Field(description="Электронная почта")
    created: datetime = Field(description="Дата и время регистрации")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "login": "awesome_user",
                "email": "user@example.com",
                "created": "2023-10-27T10:30:00Z"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str