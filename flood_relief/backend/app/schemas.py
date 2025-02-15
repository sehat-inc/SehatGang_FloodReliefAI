# schemas.py
from typing import Annotated
from pydantic import BaseModel, Field
from enum import Enum

class ResourceType(str, Enum):
    BOAT = "boat"
    SHELTER = "shelter"
    FOOD = "food"

class LocationBase(BaseModel):
    longitude: Annotated[float, Field(ge=-180, le=180)]
    latitude: Annotated[float, Field(ge=-90, le=90)]

class DemandBase(BaseModel):
    type: ResourceType
    quantity: Annotated[int, Field(gt=0)]
    priority: Annotated[int, Field(ge=1, le=5)]
    location: LocationBase

class DemandCreate(DemandBase):
    pass

class DemandResponse(DemandBase):
    id: int
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            type=obj.type,
            quantity=obj.quantity,
            priority=obj.priority,
            location=obj.get_coordinates()
        )

# Similar updates for Resource schemas
class ResourceBase(BaseModel):
    type: ResourceType
    quantity: Annotated[int, Field(ge=0)]
    location: LocationBase

class ResourceCreate(ResourceBase):
    pass

class ResourceResponse(ResourceBase):
    id: int
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            type=obj.type,
            quantity=obj.quantity,
            location=obj.get_coordinates()
        )

class AllocationBase(BaseModel):
    resource_id: int
    demand_id: int
    quantity: Annotated[int, Field(gt=0)]

class AllocationCreate(AllocationBase):
    pass

class AllocationResponse(AllocationBase):
    id: int
    
    class Config:
        from_attributes = True