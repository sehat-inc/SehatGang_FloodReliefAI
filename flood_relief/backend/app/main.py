# main.py
from fastapi import FastAPI, Depends, HTTPException
from geoalchemy2 import WKTElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from . import models, schemas
from .database import async_session
from .utils import get_coordinates

app = FastAPI(title="Disaster Relief API")

async def get_db():
    async with async_session() as session:
        yield session

@app.get("/demands/", response_model=List[schemas.DemandResponse])
async def get_demands(
    resource_type: schemas.ResourceType = None,
    min_priority: int = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all demands with optional filtering"""
    query = select(models.Demand)
    
    if resource_type:
        query = query.where(models.Demand.type == resource_type)
    if min_priority:
        query = query.where(models.Demand.priority <= min_priority)
    
    result = await db.execute(query)
    demands = result.scalars().all()
    
    # Convert the demands to response models
    return [schemas.DemandResponse.from_orm(demand) for demand in demands]

@app.post("/demands/", response_model=schemas.AllocationResponse)
async def create_demand_allocation(demand: schemas.DemandCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Convert city name to coordinates
        longitude, latitude = await get_coordinates(demand.city)
        
        # Create WKT string from coordinates
        wkt_str = f"POINT({longitude} {latitude})"
        demand_instance = models.Demand(
            type=demand.type.value,
            quantity=demand.quantity,
            priority=demand.priority,
            location=WKTElement(wkt_str, srid=4326)
        )
        
        db.add(demand_instance)
        await db.commit()
        await db.refresh(demand_instance)
        
        # Query for a resource within 20km radius and matching type
        resource_query = select(models.Resource).where(
            func.ST_DWithin(
                models.Resource.location,
                WKTElement(wkt_str, srid=4326),
                0.2  # approximately 20km in degrees (0.1 ≈ 10km)
            ),
            models.Resource.type == demand.type.value
        )
        resource_result = await db.execute(resource_query)
        resource = resource_result.scalars().first()
        
        if resource is None:
            await db.rollback()
            raise HTTPException(status_code=404, detail="No resource available at the specified location")
        
        if resource.quantity < demand.quantity:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Not enough resources available")
        
        # Update resource quantity
        resource.quantity -= demand.quantity
        
        # Create allocation record
        allocation = models.Allocation(
            resource_id=resource.id,
            demand_id=demand_instance.id,
            quantity=demand.quantity
        )
        db.add(allocation)
        await db.commit()
        await db.refresh(allocation)
        
        return allocation
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/resources/")
async def get_resources(
    resource_type: schemas.ResourceType = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all resources with optional filtering"""
    query = select(models.Resource)
    
    if resource_type:
        query = query.where(models.Resource.type == resource_type)
    
    result = await db.execute(query)
    resources = result.scalars().all()
    
    # Convert to dictionary with coordinates
    return [{
        "id": resource.id,
        "type": resource.type,
        "quantity": resource.quantity,
        "location": resource.get_coordinates()
    } for resource in resources]