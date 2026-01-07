from fastapi import APIRouter,Depends ,HTTPException
from pydantic import BaseModel
from Database.database import SessionMaker
from Models.models import CUSTOMER, MERCHANT, TRANSACTIONS
from sqlalchemy.orm import Session
from auth.dependencies import get_current_customer

router = APIRouter()
SessionLocal = SessionMaker().get_session()

class TransactionCreate(BaseModel):
    merchant_id: int
    transaction_amount: float

@router.post("/transactions")
def create_transaction(txn: TransactionCreate,customer_id:int=Depends(get_current_customer)):
    db: Session = SessionLocal()
    try:
        transaction = create_transaction_service(
            db=db,
            customer_id=customer_id,
            merchant_id=txn.merchant_id,
            transaction_amount=txn.transaction_amount
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

    return {
        "message": "Transaction successful",
        "transaction_id": transaction.transaction_id,
        "customer_id": transaction.customer_id,
        "merchant_id": transaction.merchant_id,
        "transaction_amount": transaction.transaction_amount,
        "commission_amount": transaction.commission_amount
    }

@router.get("/transaction/{merchant_id}")
def read_transaction(
    merchant_id: int,
    customer_id: int = Depends(get_current_customer)
):
    db: Session = SessionLocal()

    transaction = (
        db.query(TRANSACTIONS)
        .filter(
            TRANSACTIONS.customer_id == customer_id,
            TRANSACTIONS.merchant_id == merchant_id
        )
        .first()
    )

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return {
        "msg": "authorised customer",
        "customer_id": customer_id,
        "merchant_id": merchant_id,
        "transaction_amount": transaction.transaction_amount
    }


    


