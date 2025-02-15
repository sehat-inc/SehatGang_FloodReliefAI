# backend/app/schemas.py
from pydantic import BaseModel

class ResourceBase(BaseModel):
    type: str
    quantity: int
    latitude: float
    longitude: float

class ResourceCreate(ResourceBase):
    pass

class Resource(ResourceBase):
    id: int

    class Config:
        orm_mode = True
