from sqlalchemy import Column, Integer, String, VARCHAR,ForeignKey,Float,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base=declarative_base()

class CUSTOMER(Base):
    __tablename__="customer_details"
    _id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(VARCHAR(100))
    email=Column(VARCHAR(100),unique=True)
    password=Column(String(100),nullable=False)
    credit_limit=Column(Integer, default=2000)
    current_balance=Column(Float,default=0)  #user already used due
    transaction=relationship("TRANSACTIONS",back_populates="customer")  #one user can do multiple transactions though there is one to many relationship
    payback=relationship("PAYBACKS",back_populates="customer")

class MERCHANT(Base):
    __tablename__="merchant_details"
    merchant_id=Column(Integer,primary_key=True,autoincrement=True)
    merchant_name=Column(VARCHAR(100))
    email=Column(VARCHAR(100))
    password=Column(String(100),unique=True)
    phone=Column(VARCHAR(15),unique=True)
    fee_percentage=Column(Float,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)
    transaction=relationship("TRANSACTIONS",back_populates="merchant")
    

class TRANSACTIONS(Base):
    __tablename__="transaction_details"
    transaction_id=Column(Integer,primary_key=True,autoincrement=True)
    customer_id=Column(Integer,ForeignKey("customer_details._id"))
    merchant_id=Column(Integer,ForeignKey("merchant_details.merchant_id"))
    transaction_amount=Column(Float)
    commission_amount=Column(Float)  #based on mechnt id we should query from mrchnt table and then we get fee per from mrchnt table using that we have to calculate the commission
    transaction_date=Column(DateTime,default=datetime.utcnow)
    customer=relationship("CUSTOMER",back_populates="transaction") # one transaction can use many users
    merchant=relationship("MERCHANT",back_populates="transaction")
    

class PAYBACKS(Base):
    __tablename__="payback_details"
    payback_id=Column(Integer,primary_key=True,autoincrement=True)
    customer_id=Column(Integer,ForeignKey("customer_details._id"))
    due_amount=Column(Float)
    paid_due_amount=Column(Float)
    remaining_paid=Column(Float)
    created_at=Column(DateTime,default=datetime.utcnow)
    customer=relationship("CUSTOMER",back_populates="payback")


