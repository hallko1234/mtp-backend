from fastapi import APIRouter, Response, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import bcrypt
import jwt
import datetime
from config import SECRET_KEY

router_auth = APIRouter(prefix="/auth", tags=["auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_token(user_id: int, role: str, expires_delta):
    expire = datetime.datetime.utcnow() + expires_delta
    return jwt.encode({"user_id": user_id, "role": role, "exp": expire}, SECRET_KEY, algorithm="HS256")

@router_auth.post("/login")
def login(response: Response, username: str, password: str, db: Session = Depends(lambda: SessionLocal())):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.checkpw(password.encode(), user.password.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_token(user.id, user.role, datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token(user.id, user.role, datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="Lax")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="Lax")

    return {"message": "Login erfolgreich"}

@router_auth.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logout erfolgreich"}
