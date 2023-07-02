from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from jose import JWTError, jwt # python-joseをインポート
from passlib.context import CryptContext
from datetime import datetime, timedelta
# 自作モジュール
import models.auth as auth_models

# 各変数
SECRET_KEY = "YOUR-SECRET-KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# テスト用データ
users_db = {
    "user1": {
        "username": "user1",
        "full_name": "User Test",
        "password": pwd_context.hash("password123"),
        "roles": ["user"],
    },
    "admin1": {
        "username": "admin1",
        "full_name": "Admin Test",
        "password": pwd_context.hash("admin123"),
        "roles": ["admin"],
    }
}


def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user:
        return False
    if not pwd_context.verify(password, user["password"]):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        roles: List[str] = payload.get("roles", [])
        if username is None:
            raise credentials_exception
        token_data = auth_models.TokenData(username=username, roles=roles)
    except JWTError:
        raise credentials_exception
    user = users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return user