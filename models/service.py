from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False
    )

    business = relationship("Business", back_populates="services")

    appointments = relationship(
        "Appointment",
        back_populates="service",
        cascade="all, delete"
    )