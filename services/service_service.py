from sqlalchemy.orm import Session

from repositories.service_repository import (
    create_service,
    get_services_by_business,
)
from schemas.service import ServiceCreate


def create_new_service(
    db: Session,
    service_data: ServiceCreate,
):
    return create_service(db, service_data)


def get_business_services(
    db: Session,
    business_id: int,
):
    return get_services_by_business(db, business_id)