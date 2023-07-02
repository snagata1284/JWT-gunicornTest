from fastapi import APIRouter, Depends, HTTPException
# 自作モジュール
import auth.auth as auth_func

router = APIRouter(tags=["test"])

@router.get('/')
def index(user = Depends(auth_func.get_current_user)):
    return {"text": "Hello, " + user["full_name"]}