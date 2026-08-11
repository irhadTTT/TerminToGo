from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.service import ServiceCreate, ServiceResponse
from services.service_service import (
    create_new_service,
    get_business_services,
)

router = APIRouter(
    prefix="/services",
    tags=["Services"],
)


@router.post("/", response_model=ServiceResponse)
def create_service(
    service_data: ServiceCreate,
    db: Session = Depends(get_db),
):
    return create_new_service(db, service_data)


@router.get(
    "/business/{business_id}",
    response_model=list[ServiceResponse],
)
def get_services(
    business_id: int,
    db: Session = Depends(get_db),
):
    return get_business_services(db, business_id)