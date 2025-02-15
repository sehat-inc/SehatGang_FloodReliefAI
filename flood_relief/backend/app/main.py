# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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