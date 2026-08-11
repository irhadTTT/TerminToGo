from pydantic import BaseModel


class ServiceCreate(BaseModel):
    name: str
    duration_minutes: int
    price: int
    business_id: int


class ServiceResponse(BaseModel):
    id: int
    name: str
    duration_minutes: int
    price: int
    business_id: int

    class Config:
        from_attributes = True