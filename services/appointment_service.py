from sqlalchemy.orm import Session
from datetime import date, datetime, time, timedelta

from repositories.appointment_repository import (
    create_appointment,
    get_appointments_by_business,
    has_overlapping_appointment,
    get_appointments_for_date
)
from schemas.appointment import AppointmentCreate
from core.exception import (
    BadRequestException, 
    ConflictException
)


def create_new_appointment(
    db: Session,
    appointment_data: AppointmentCreate,
):

    if appointment_data.start_time >= appointment_data.end_time:
        raise BadRequestException("End time must be after start time")

    if has_overlapping_appointment(
        db=db,
        business_id=appointment_data.business_id,
        start_time=appointment_data.start_time,
        end_time=appointment_data.end_time,
    ):
        raise ConflictException("Appointment time is already booked")

    return create_appointment(db, appointment_data)

def get_business_appointments(
    db: Session,
    business_id: int,
):
    return get_appointments_by_business(db, business_id)


def get_available_slots(
    db: Session,
    business_id: int,
    service_duration: int,
    appointment_date: date,
) -> list[str]:
    appointments = get_appointments_for_date(
        db,
        business_id,
        appointment_date,
    )

    work_start = datetime.combine(
        appointment_date,
        time(9, 0),
    )

    work_end = datetime.combine(
        appointment_date,
        time(17, 0),
    )

    slots = []
    current = work_start

    while current + timedelta(minutes=service_duration) <= work_end:
        slot_end = current + timedelta(minutes=service_duration)

        overlaps = any(
            appointment.start_time < slot_end
            and appointment.end_time > current
            for appointment in appointments
        )

        if not overlaps:
            slots.append(current.strftime("%H:%M"))

        current += timedelta(minutes=service_duration)

    return slots