from sqlalchemy.orm import Session
from Models.models import CUSTOMER, PAYBACKS
from datetime import datetime

def create_payback_service(
    db: Session,
    customer_id: int,
    paid_amount: float
):
    customer = db.query(CUSTOMER).filter(CUSTOMER._id == customer_id).first()
    if not customer:
        raise ValueError("Customer not found")

    if paid_amount > customer.current_balance:
        raise ValueError("Payback exceeds due amount")

    before_due = customer.current_balance
    customer.current_balance -= paid_amount

    payback = PAYBACKS(
        customer_id=customer_id,
        due_amount=before_due,
        paid_due_amount=paid_amount,
        remaining_paid=customer.current_balance,
        created_at=datetime.utcnow()
    )

    db.add(payback)
    db.commit()
    db.refresh(payback)

    return {
        "customer_id": customer_id,
        "before_due": before_due,
        "paid_amount": paid_amount,
        "remaining_due": customer.current_balance
    }
