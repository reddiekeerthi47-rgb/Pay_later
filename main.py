from fastapi import FastAPI
from Routes import customer_router, merchant_router, transactions_router, payback_router
from auth.auth_services import router as auth_router

app = FastAPI()

app.include_router(customer_router, prefix="/db", tags=["customer"])
app.include_router(merchant_router, prefix="/db", tags=["merchant"])
app.include_router(transactions_router, prefix="/db", tags=["transactions"])
app.include_router(payback_router, prefix="/db", tags=["payback"])
app.include_router(auth_router)
