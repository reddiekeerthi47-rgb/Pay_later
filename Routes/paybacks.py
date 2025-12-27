from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Database.database import SessionMaker
from sqlalchemy.orm import Session
from Services.paybacks_services import create_payback_service

router = APIRouter()
SessionLocal = SessionMaker().get_session()

class CreatePayback(BaseModel):
    customer_id: int
    paid_due_amount: float

@router.post("/paybacks")
def create_payback(payback: CreatePayback):
    db: Session = SessionLocal()
    try:
        result = create_payback_service(
            db=db,
            customer_id=payback.customer_id,
            paid_amount=payback.paid_due_amount
        )
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        db.close()
