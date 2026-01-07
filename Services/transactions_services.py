from sqlalchemy.orm import Session
from Models.models import CUSTOMER, MERCHANT, TRANSACTIONS
from datetime import datetime

def create_transaction_service(
    db: Session,
    customer_id: int,
    merchant_id: int,
    transaction_amount: float
):
    # Validate customer
    customer = db.query(CUSTOMER).filter(
        CUSTOMER._id == customer_id
    ).first()
    if not customer:
        raise ValueError("Customer not found")

    # Validate merchant
    merchant = db.query(MERCHANT).filter(
        MERCHANT.merchant_id == merchant_id
    ).first()
    if not merchant:
        raise ValueError("Merchant not found")

    # Credit limit check
    if customer.current_balance + transaction_amount > customer.credit_limit:
        raise ValueError("Insufficient credit limit")

    # Calculate commission
    commission_amount = (
        transaction_amount * merchant.fee_percentage
    ) / 100

    # Create transaction record
    transaction = TRANSACTIONS(
        customer_id=customer_id,
        merchant_id=merchant_id,
        transaction_amount=transaction_amount,
        commission_amount=commission_amount,
        transaction_date=datetime.utcnow()
    )

    # Update customer balance
    customer.current_balance += transaction_amount

    # Persist changes safely
    try:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
    except Exception:
        db.rollback()
        raise

    return transaction
