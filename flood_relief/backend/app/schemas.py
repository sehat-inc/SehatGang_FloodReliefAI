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

class AllocationResponse(BaseModel):
    id: int
    quantity: int
    resource_details: dict
    demand_details: dict
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_orm(cls, obj):
        # Ensure relationships are loaded
        if not hasattr(obj, 'resource') or not hasattr(obj, 'demand'):
            raise ValueError("Resource and Demand relationships must be loaded")
            
        return cls(
            id=obj.id,
            quantity=obj.quantity,
            resource_details={
                "id": obj.resource.id,
                "type": obj.resource.type,
                "quantity": obj.resource.quantity,
                "location": obj.resource.get_coordinates()
            },
            demand_details={
                "id": obj.demand.id,
                "type": obj.demand.type,
                "quantity": obj.demand.quantity,
                "priority": obj.demand.priority,
                "location": obj.demand.get_coordinates()
            }
        )