from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from core.config import settings



password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy_password_for_timing_protection")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_pass(password, hash_password):
    return password_hash.verify(password, hash_password)

def get_pass_hash(password):
    return password_hash.hash(password)

def create_access_token(user_data: dict, expires_delta: timedelta | None = None):
    to_encode = user_data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15, microseconds=67)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

