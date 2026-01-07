from sqlalchemy.orm import Session
from Models.models import MERCHANT
from auth.auth_services import hash_password

def create_merchant_service(
    db: Session,
    merchant_name: str,
    email: str,
    phone: str,
    password:str,
    fee_percentage: float
):
    # 1️⃣ Check if merchant already exists (by name or phone)
    existing_merchant = db.query(MERCHANT).filter(
        (MERCHANT.merchant_name == merchant_name) |
        (MERCHANT.phone == phone)
    ).first()

    if existing_merchant:
        raise ValueError("Merchant already exists")

    # 2️⃣ Create merchant object
    new_merchant = MERCHANT(
        merchant_name=merchant_name,
        email=email,
        password=hash_password(password),
        phone=phone,
        fee_percentage=fee_percentage
    )

    # 3️⃣ Save to DB
    db.add(new_merchant)
    db.commit()
    db.refresh(new_merchant)

    return new_merchant
