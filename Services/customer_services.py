from sqlalchemy.orm import Session
from Models.models import CUSTOMER
from auth import auth_services

DEFAULT_CREDIT_LIMIT=2000

def create_customer_service(db:Session,name:str,email:str,password:str):
    existing=db.query(CUSTOMER).filter(CUSTOMER.email == email).first()
    print("#"*100)

    if existing:
        raise ValueError("Customer already exists")
    else:
        customer=CUSTOMER(
            name=name,
            email=email,
            password=auth_services.hash_password(password),
            credit_limit=DEFAULT_CREDIT_LIMIT,
            current_balance=0
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

def get_available_credit(customer:CUSTOMER):
    return customer.credit_limit-customer.current_balance

def validate_customer_credit(customer:CUSTOMER,amount:float):
    if amount <=0:
        raise ValueError("Invalid transaction amount")

    available_credit=get_available_credit(customer)

    if available_credit < amount:
        raise ValueError("Insufficient credit limit")

def use_customer_credit(
    db:Session,customer_id:int,amount:float):
    customer=db.query(CUSTOMER).filter(CUSTOMER._id == customer_id).first()

    if not customer:
        raise ValueError("customer not found")

    validate_customer_credit(customer,amount)

    customer.current_balance +=amount
    db.commit()

    return customer

def restore_customer_credit(db:Session,customer_id:int,amount:float):
    customer=db.query(CUSTOMER).filter(CUSTOMER._id==customer_id).first()

    if not customer:
        raise ValueError("customer not found")
    if amount <=0:
        raise ValueError("Invalid payback amount")
    if amount > customer.current_balance:
        raise ValueError("Payback exceeds outstanding balance")
    customer.current_balance -=amount
    db.commit()
    return customer            
    