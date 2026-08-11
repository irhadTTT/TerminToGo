from sqlalchemy.orm import Session

from models.service import Service
from schemas.service import ServiceCreate


def create_service(
    db: Session,
    service_data: ServiceCreate,
) -> Service:
    service = Service(
        name=service_data.name,
        duration_minutes=service_data.duration_minutes,
        price=service_data.price,
        business_id=service_data.business_id,
    )

    db.add(service)
    db.commit()
    db.refresh(service)

    return service


def get_services_by_business(
    db: Session,
    business_id: int,
) -> list[Service]:
    return (
        db.query(Service)
        .filter(Service.business_id == business_id)
        .all()
    )