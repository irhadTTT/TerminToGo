from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime, time
from fastapi import Query

from database import get_db
from schemas.appointment import (
    AppointmentCreate, 
    AppointmentResponse
)
from services.appointment_service import (
    create_new_appointment,
    get_business_appointments,
    get_available_slots
)


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
):
    return create_new_appointment(db, appointment_data)

@router.get(
    "/business/{business_id}",
    response_model=list[AppointmentResponse],
)
def get_appointments(
    business_id: int,
    db: Session = Depends(get_db),
):
    return get_business_appointments(db, business_id)


@router.get(
    "/available"
)
def available_slots(
    business_id: int,
    service_duration: int,
    date: str = Query(...),
    db: Session = Depends(get_db),
):
    appointment_date = datetime.strptime(date, "%d-%m-%Y").date()
    slots = get_available_slots(
        db=db,
        business_id=business_id,
        service_duration=service_duration,
        appointment_date=appointment_date
    )

    return {
        "date": date,
        "available_slots": slots,
    }