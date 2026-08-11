from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.business import BusinessCreate, BusinessResponse
from services.business_service import (
    create_new_business,
    get_all_businesses
)

router = APIRouter(
    prefix="/business",
    tags=["Business"],
)


@router.post("/", response_model=BusinessResponse)
def create_business(
    business_data: BusinessCreate,
    db: Session = Depends(get_db)
):
    return create_new_business(db, business_data)

@router.get("/", response_model=list[BusinessResponse])
def get_businesses(db: Session = Depends(get_db)):
    return get_all_businesses(db)