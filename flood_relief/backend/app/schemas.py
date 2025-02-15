# schemas.py
from typing import Annotated
from pydantic import BaseModel, Field
from enum import Enum

class ResourceType(str, Enum):
    BOAT = "boat"
    SHELTER = "shelter"
    FOOD = "food"

class DemandBase(BaseModel):
    type: ResourceType
    quantity: Annotated[int, Field(gt=0)]
    priority: Annotated[int, Field(ge=1, le=5)]
    city: str

class DemandCreate(DemandBase):
    pass

class DemandResponse(BaseModel):
    id: int
    type: ResourceType
    quantity: int
    priority: int
    city: str
    location: dict  # This will contain the coordinates

    class Config:
        from_attributes = True
    
    @classmethod
    def from_orm(cls, obj):
        # Get coordinates from the geometry field
        coords = obj.get_coordinates()
        return cls(
            id=obj.id,
            type=obj.type,
            quantity=obj.quantity,
            priority=obj.priority,
            city=obj.city if hasattr(obj, 'city') else "Unknown",  # Fallback for existing records
            location=coords
        )

# Similar updates for Resource schemas
class ResourceBase(BaseModel):
    type: ResourceType
    quantity: Annotated[int, Field(ge=0)]
    city: str

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
            city=obj.city
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