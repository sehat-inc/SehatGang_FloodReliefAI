# main.py
from fastapi import FastAPI, Depends, HTTPException
from geoalchemy2 import WKTElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from . import models
from . import schemas
from .database import async_session

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
    # Convert LocationBase into WKT string and then to a geometry element
    wkt_str = f"POINT({demand.location.longitude} {demand.location.latitude})"
    demand_instance = models.Demand(
        type=demand.type.value,  # enum conversion if needed
        quantity=demand.quantity,
        priority=demand.priority,
        location=WKTElement(wkt_str, srid=4326)
    )
    db.add(demand_instance)
    await db.commit()
    await db.refresh(demand_instance)
    
    # Query for a resource that has the same location using ST_Equals
    resource_query = select(models.Resource).where(
        func.ST_Equals(models.Resource.location, WKTElement(wkt_str, srid=4326))
    )
    resource_result = await db.execute(resource_query)
    resource = resource_result.scalars().first()
    
    if resource is None:
        await db.rollback()
        raise HTTPException(status_code=404, detail="No resource available at the specified location")
    
    if resource.quantity < demand.quantity:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Not enough resources available")
    
    # Update resource quantity (subtract the demanded amount)
    resource.quantity -= demand.quantity
    
    # Create an allocation record linking the demand and resource
    allocation = models.Allocation(
        resource_id=resource.id,
        demand_id=demand_instance.id,
        quantity=demand.quantity
    )
    db.add(allocation)
    await db.commit()
    await db.refresh(allocation)
    
    return allocation