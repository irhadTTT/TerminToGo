from sqlalchemy.orm import Session

from models.business import Business
from schemas.business import BusinessCreate


def create_business(db: Session, business_data: BusinessCreate) -> Business:
    business = Business(
        name=business_data.name,
        description=business_data.description
    )

    db.add(business)
    db.commit()
    db.refresh(business)

    return business

def get_businesses(db: Session) -> list[Business]:
    return db.query(Business).all()