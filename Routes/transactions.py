from fastapi import APIRouter,Depends ,HTTPException
from pydantic import BaseModel
from Database.database import SessionMaker
from Models.models import CUSTOMER, MERCHANT, TRANSACTIONS
from sqlalchemy.orm import Session
from auth.dependencies import get_current_customer

router = APIRouter()
SessionLocal = SessionMaker().get_session()

class TransactionCreate(BaseModel):
    customer_id: int
    merchant_id: int
    transaction_amount: float

@router.post("/transactions")
def create_transaction(txn: TransactionCreate,customer_id=Depends(get_current_customer)):
    db: Session = SessionLocal()

    customer = db.query(CUSTOMER).filter(CUSTOMER._id == txn.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    merchant = db.query(MERCHANT).filter(MERCHANT.merchant_id == txn.merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    available_credit = customer.credit_limit - customer.current_balance
    if available_credit < txn.transaction_amount:
        raise HTTPException(status_code=400, detail="Insufficient credit limit")

    commission = (txn.transaction_amount * merchant.fee_percentage) / 100

    transaction = TRANSACTIONS(
        customer_id=txn.customer_id,
        merchant_id=txn.merchant_id,
        transaction_amount=txn.transaction_amount,
        commission_amount=commission
    )

    customer.current_balance += txn.transaction_amount

    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.close()

    return {
        "transaction_id": transaction.transaction_id,
        "commission_amount": commission
    }

