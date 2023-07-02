from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
# 自作モジュール
import models.auth as auth_models
import auth.auth as auth_func

router = APIRouter(tags=["auth"])

@router.post("/token", response_model=auth_models.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_func.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_func.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_func.create_access_token(
        data={"sub": user["username"], "roles": user["roles"]}
    )
    return {"access_token": access_token, "token_type": "bearer", "username": user["username"], "roles": user["roles"]}
