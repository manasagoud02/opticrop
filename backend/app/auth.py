import os
from datetime import datetime, timedelta, timezone
from hashlib import pbkdf2_hmac
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .database import fetch_user_by_id

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
security = HTTPBearer()


def get_password_hash(password: str) -> str:
    salt = b"opticrop-salt"
    digest = pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return digest.hex()


def verify_password(plain_password: str, password_hash: str) -> bool:
    return get_password_hash(plain_password) == password_hash


def create_access_token(subject: str) -> str:
    payload = {
        "sub": subject,
        "exp": datetime.now(timezone.utc) + timedelta(hours=8),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=401, detail="Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = fetch_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
