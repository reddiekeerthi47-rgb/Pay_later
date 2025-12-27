from datetime import datetime, timedelta
from jose import jwt

# JWT configuration
SECRET_KEY = "f8c1e7a9d4b02f5e6c3a91b7d0e4f2a89c6d5e3b7a90f1e2d4c6a8b5f9e0d7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(customer_id: int):
    payload = {
        "customer_id": customer_id,   # authentication
        "role": "customer",           # authorization
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
