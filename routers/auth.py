from fastapi import APIRouter, BackgroundTasks, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.exception import BadRequestException, UnauthorizedException
from core.security import create_email_token
from database import get_db
from dependencies import get_current_user
from jwt_handler import create_access_token
from limiter import limiter
from models.user import User
from repositories import user_repository
from schemas.user import UserCreate, UserResponse
from core.security import hash_password, verify_password
from services.auth_service import (
    login as login_service,
    register as register_service,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    summary="User login",
    description="Authenticate user and return JWT access token",
)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return login_service(request, form_data, db)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register user",
    description="Register new user",
)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_service(user, db)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
