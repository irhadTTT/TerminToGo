from datetime import datetime

from pydantic import BaseModel, field_validator, field_serializer

DATETIME_FORMAT = "%d.%m.%Y %H:%M"

class AppointmentCreate(BaseModel):
    customer_id: int
    start_time: datetime
    end_time: datetime
    business_id: int
    service_id: int

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def parse_datetime(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, DATETIME_FORMAT)

        return value



class AppointmentResponse(BaseModel):
    id: int
    customer_id: int
    start_time: datetime
    end_time: datetime
    status: str
    business_id: int
    service_id: int

    @field_serializer("start_time", "end_time")
    def serialize_datetime(self, value: datetime) -> str:
        return value.strftime("%d-%m-%Y %H:%M:%S")

    class Config:
        from_attributes = True


class AvailableSlotsResponse(BaseModel):
    date: date
    available_slots: list[str]

class AppointmentReschedule(BaseModel):
    start_time: datetime
    end_time: datetime

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def parse_datetime(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, DATETIME_FORMAT)

        return value