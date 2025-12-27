from fastapi import APIRouter, Depends, HTTPException #responses 200-300 ok responses , 300-400 redirection,400-500 server side access related,500 and above client side
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session 
import bcrypt  #to hash the passwords

from Database.database import SessionMaker  
from Models.models import CUSTOMER
from auth.jwt_service import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

SessionLocal = SessionMaker().get_session()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        pass


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

def hash_password(password: str) -> str: #password encode,
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    customer = db.query(CUSTOMER).filter(
        CUSTOMER.email == data.email
    ).first()

    if not customer:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, customer.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(customer._id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
