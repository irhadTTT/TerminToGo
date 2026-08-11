from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    services = relationship(
        "Service",
        back_populates="business",
        cascade="all, delete",
    )

    appointments = relationship(
        "Appointment",
        back_populates="business",
        cascade="all, delete"
    )