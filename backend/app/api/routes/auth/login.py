# Routes for login, token refresh, logout

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

# Security
from fastapi.security import OAuth2PasswordRequestForm

from app.api.services.user_services import authenticate_user
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.api.schemas.token import Token
from app.core.deps import fake_users_db


router = APIRouter(prefix="", tags=["auth"])


@router.post("/token")
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
