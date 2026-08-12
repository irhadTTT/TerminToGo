import secrets
from datetime import datetime, timedelta, timezone

from jose import jwt

from core.config import settings
from passlib.context import CryptContext


def create_email_token(email: str):

    payload = {"sub": email, "exp": datetime.now(timezone.utc) + timedelta(hours=24)}

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token():
    return secrets.token_urlsafe(64)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
