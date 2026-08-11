from sqlalchemy.orm import Session

from repositories.business_repository import (
        create_business,
        get_businesses
    )

from schemas.business import BusinessCreate


def create_new_business(
    db: Session,
    business_data: BusinessCreate,
):
    return create_business(db, business_data)

def get_all_businesses(db: Session):
    return get_businesses(db)