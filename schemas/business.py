from pydantic import BaseModel


class BusinessCreate(BaseModel):
    name: str
    description: str | None = None


class BusinessResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True