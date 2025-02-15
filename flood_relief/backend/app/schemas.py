# backend/app/schemas.py
from pydantic import BaseModel, Field
from typing import Literal

class ResourceBase(BaseModel):
    type: Literal["boats", "food", "shelter"]
    quantity: int
    latitude: float
    longitude: float

class ResourceCreate(ResourceBase):
    pass

class Resource(ResourceBase):
    id: int

    class Config:
        orm_mode = True

class DemandBase(BaseModel):
    type: Literal["boats", "food", "shelter"]
    quantity: int
    priority: int = Field(..., ge=1, le=5) 
    latitude: float
    longitude: float

class DemandCreate(DemandBase):
    pass

class Demand(DemandBase):
    id: int

    class Config:
        orm_mode = True

class AllocationBase(BaseModel):
    demand_id: int
    resource_id: int
    quantity_allocated: int

class AllocationCreate(AllocationBase):
    pass

class Allocation(AllocationBase):
    id: int

    class Config:
        orm_mode = True