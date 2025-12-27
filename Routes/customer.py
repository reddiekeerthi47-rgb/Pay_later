from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel, EmailStr
from Database.database import SessionMaker
from sqlalchemy.orm import Session
from Services import customer_services
from auth.dependencies import get_current_customer

router = APIRouter()
Session = SessionMaker().get_session()


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    password:str


@router.post("/create-customer")
def create_customer(customer: CustomerCreate):
    db: Session = Session()
    try:
        new_customer = customer_services.create_customer_service(
            db,
            customer.name,
            customer.email,
            customer.password
        )
        return {
            "message": "User created",
            "user_id": new_customer._id
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@router.get("/profile")
def get_profile(customer_id: int = Depends(get_current_customer)): #depends on functionality
    return {
        "message": "Authorized customer",
        "customer_id": customer_id
    }
    