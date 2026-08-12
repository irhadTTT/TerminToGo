from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from core.exception import NotFoundException, UnauthorizedException
from core.security import create_refresh_token
from jwt_handler import create_access_token
from models.refresh_token import RefreshToken
from models.user import User
from repositories import refresh_token_repository


def save_refresh_token(db: Session, user_id: int):
    token = create_refresh_token()

    if token is None:
        raise NotFoundException("User not found")

    db_refresh_token = RefreshToken(
        token=token,
        user_id=user_id,
        expires_at=datetime.now(timezone.utc).replace(tzinfo=None)
        + timedelta(days=30),
    )

    token = refresh_token_repository.create(db, db_refresh_token)

    return token


def get_token(db: Session, token: str):
    token = refresh_token_repository.get_by_token(db, token)

    if token is None:
        raise NotFoundException("Refresh token not found")

    return token


def refresh_access_token(token: str, db: Session):
    refresh_token = get_token(db, token)

    if refresh_token is None:
        raise UnauthorizedException("Invalid refresh token")

    if refresh_token.revoked:
        raise UnauthorizedException("Refresh token has been revoked")

    if refresh_token.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
        raise UnauthorizedException("Refresh token has expired")

    user = db.query(User).filter(User.id == refresh_token.user_id).first()

    if user is None:
        raise NotFoundException("User not found")

    access_token = create_access_token(
        data={"sub": str(refresh_token.user_id), "role": user.role}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }