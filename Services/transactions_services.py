from sqlalchemy.orm import Session
from Models.models import CUSTOMER, MERCHANT, TRANSACTIONS
from datetime import datetime

def create_transaction_service(
    db: Session,
    customer_id: int,
    merchant_id: int,
    transaction_amount: float
):
    customer = db.query(CUSTOMER).filter(CUSTOMER._id == customer_id).first()
    if not customer:
        raise ValueError("Customer not found")

    merchant = db.query(MERCHANT).filter(MERCHANT.merchant_id == merchant_id).first()
    if not merchant:
        raise ValueError("Merchant not found")

    if customer.current_balance + transaction_amount > customer.credit_limit:
        return {"status": "rejected", "reason": "credit limit exceeded"}

    commission = (transaction_amount * merchant.fee_percentage) / 100

    transaction = TRANSACTIONS(
        customer_id=customer_id,
        merchant_id=merchant_id,
        transaction_amount=transaction_amount,
        commission_amount=commission,
        transaction_date=datetime.utcnow()
    )

    customer.current_balance += transaction_amount

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return {
        "status": "success",
        "transaction_id": transaction.transaction_id,
        "transaction_amount": transaction.transaction_amount
    }
