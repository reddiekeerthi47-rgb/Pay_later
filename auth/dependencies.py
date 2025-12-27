from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials #bearer is a type of authentication
from jose import jwt

# SAME secret used while creating token
SECRET_KEY = "f8c1e7a9d4b02f5e6c3a91b7d0e4f2a89c6d5e3b7a90f1e2d4c6a8b5f9e0d7"
ALGORITHM = "HS256"

security = HTTPBearer()


def get_current_customer(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Authentication
    customer_id = payload.get("customer_id")
    role = payload.get("role")

    # Authorization
    if role != "customer":
        raise HTTPException(status_code=403, detail="Customer access only")

    return customer_id
