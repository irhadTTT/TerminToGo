from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.exception import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
)
from database import get_db
from dependencies import get_current_admin
from enums.sort import UserRole
from models.user import User
from repositories import user_repository
from schemas.auth import PasswordReset
from schemas.user import UserCreate, UserResponse
from core.security import hash_password
from services.user_service import ( 
    get_users as get_users_service,
    create_user as create_user_service,
    delete_user as delete_user_service,
    change_role as change_role_service,
    make_first_admin as make_first_admin_service
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_admin)
):
    return get_users_service(db, current_user)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    return create_user_service(user, db, current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    delete_user_service(user_id, db, current_user)

@router.put("/{user_id}/role")
def change_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    return change_role_service(user_id, role, db, current_user)


@router.post("/make-first-admin")
def make_first_admin(user_id: int, db: Session = Depends(get_db)):
    return make_first_admin_service(user_id, db)