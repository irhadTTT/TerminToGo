from sqlalchemy.orm import Session

from models.appointment import Appointment
from schemas.appointment import AppointmentCreate
from datetime import datetime, time


def create_appointment(
    db: Session,
    appointment_data: AppointmentCreate,
) -> Appointment:
    appointment = Appointment(
        customer_name=appointment_data.customer_name,
        start_time=appointment_data.start_time,
        end_time=appointment_data.end_time,
        business_id=appointment_data.business_id,
        service_id=appointment_data.service_id,
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment

def get_appointments_by_business(
    db: Session,
    business_id: int,
) -> list[Appointment]:
    return (
        db.query(Appointment)
        .filter(Appointment.business_id == business_id)
        .all()
    )


def has_overlapping_appointment(
    db: Session,
    business_id: int,
    start_time: datetime,
    end_time: datetime,
) -> bool:
    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.business_id == business_id,
            Appointment.status == "booked",
            Appointment.start_time < end_time,
            Appointment.end_time > start_time,
        )
        .first()
    )

    return appointment is not None


def get_appointments_for_date(
    db: Session,
    business_id: int,
    appointment_date: date,
) -> list[Appointment]:
    start_of_day = datetime.combine(appointment_date, time.min)
    end_of_day = datetime.combine(appointment_date, time.max)

    return (
        db.query(Appointment)
        .filter(
            Appointment.business_id == business_id,
            Appointment.start_time < end_of_day,
            Appointment.end_time > start_of_day,
            Appointment.status == "booked",
        )
        .all()
    )