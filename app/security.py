from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    raise ValueError("SECRET_KEY environment variable not set")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


def create_access_token(
        *,
        subject: dict[str, Any],
        expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    expires: datetime = datetime.now(timezone.utc) + expires_delta

    to_encode: dict[str, Any] = {
        "sub": subject,
        "exp": expires,
    }

    encoded_jwt: str = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt
    

def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload
    except JWTError as jwt_error:
        raise JWTError("Invalid token") from jwt_error
    
    

