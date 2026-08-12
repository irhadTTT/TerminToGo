from sqlalchemy.orm import Session
from datetime import date, datetime, time, timedelta

from repositories.appointment_repository import (
    create_appointment,
    get_appointments_by_business,
    has_overlapping_appointment,
    get_appointments_for_date,
    has_conflict,
    get_by_id
)
from schemas.appointment import AppointmentCreate
from core.exception import (
    NotFoundException,
    BadRequestException, 
    ConflictException,
    ForbiddenException
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


def cancel_appointment(
    appointment_id: int,
    current_user: User,
    db: Session,
):
    appointment = get_by_id(
        db,
        appointment_id
    )

    if appointment is None:
        raise NotFoundException("Appointment not found")

    if appointment.customer_id != current_user.id:
        raise ForbiddenException(
            "You cannot cancel this appointment"
        )

    if appointment.status == "cancelled":
        raise BadRequestException(
            "Appointment is already cancelled"
        )

    appointment.status = "cancelled"

    db.commit()
    db.refresh(appointment)

    return appointment


def reschedule_appointment(
    appointment_id: int,
    data: AppointmentReschedule,
    current_user: User,
    db: Session,
):
    appointment = get_by_id(
        db,
        appointment_id
    )

    if appointment is None:
        raise NotFoundException("Appointment not found")

    if appointment.customer_id != current_user.id:
        raise ForbiddenException(
            "You cannot reschedule this appointment"
        )

    if appointment.status != "booked":
        raise BadRequestException(
            "Only booked appointments can be rescheduled"
        )

    if data.start_time <= datetime.now():
        raise BadRequestException(
            "Appointment cannot be scheduled in the past"
        )

    if data.start_time >= data.end_time:
        raise BadRequestException(
            "Start time must be before end time"
        )

    conflict = has_conflict(
        db=db,
        business_id=appointment.business_id,
        start_time=data.start_time,
        end_time=data.end_time,
        appointment_id=appointment.id,
    )

    if conflict:
        raise BadRequestException(
            "The selected time slot is already booked"
        )

    appointment.start_time = data.start_time
    appointment.end_time = data.end_time

    db.commit()
    db.refresh(appointment)

    return appointment