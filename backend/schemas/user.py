from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserResponse(BaseModel):
    user_id: UUID
    login: str
    email: str
    created: datetime

class Token(BaseModel):
    access_token: str
    token_type: str