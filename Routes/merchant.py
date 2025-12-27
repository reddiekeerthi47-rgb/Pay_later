from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,EmailStr
from Database.database import SessionMaker
from Models.models import MERCHANT
from sqlalchemy.orm import Session
from Services.merchant_services import create_merchant_service

router=APIRouter()
Session=SessionMaker().get_session()

class merchantcreate(BaseModel):
    merchant_name:str
    email:EmailStr
    phone:str
    fee_percentage:float

@router.post("/merchant-create")
def create_merchant(merchant:merchantcreate):
    db: Session=Session()

    new_merchant=MERCHANT(
            merchant_name=merchant.merchant_name,
            email=merchant.email,
            phone=merchant.phone,
            fee_percentage=merchant.fee_percentage
    )
    db.add(new_merchant)
    db.commit()
    db.refresh(new_merchant)
    db.close()
    return{"created the merchant successfully": new_merchant.merchant_id}

# @router.patch("/merchant/{merchant_name}")
# def read_fee(merchant_name:str):
#     db:Session=Session()

#     merchant=db.query(MERCHANT).filter(MERCHANT.merchant_name == merchant_name).first()
#     merchant.fee=fee

#     db.commit()
#     db.refresh(merchant)
#     return {"name": merchant.merchant_name, "fee_percentage": merchant.fee}

@router.get("fee/{merchant_name}")
def read_fee_reports(merchant_name:str):
    db:Session=Session()

    merchant=db.query(MERCHANT).filter(MERCHANT.merchant_name == merchant_name).first()

    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    return{"fee collected":merchant.fee_percentage}    




    




    

    







