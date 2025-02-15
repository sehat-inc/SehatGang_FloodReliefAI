# backend/app/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
import traceback

from . import models, schemas
from .database import async_session

router = APIRouter()

@router.post("/resources/", response_model=schemas.Resource)
async def create_resource(resource: schemas.ResourceCreate, db: AsyncSession = Depends(async_session)):
    point = Point(resource.longitude, resource.latitude)
    location = from_shape(point, srid=4326)
    db_resource = models.Resource(
        type=resource.type,
        quantity=resource.quantity,
        location=location
    )
    db.add(db_resource)
    await db.commit()
    await db.refresh(db_resource)
    return db_resource

@router.get("/resources/", response_model=list[schemas.Resource])
async def read_resources(db: AsyncSession = Depends(async_session)):
    stmt = select(models.Resource)
    result = await db.execute(stmt)
    resources = result.scalars().all()
    return resources

@router.post("/demands", response_model=schemas.Demand)
async def create_demand(demand: schemas.DemandCreate, db: AsyncSession = Depends(async_session)):
    try:
        print('tom')
        # Debug log the parsed demand
        print("Received demand:", demand.dict())
        point = Point(demand.longitude, demand.latitude)
        location = from_shape(point, srid=4326)
        db_demand = models.Demand(
            type=demand.type,
            quantity=demand.quantity,
            priority=demand.priority,
            location=location
        )
        db.add(db_demand)
        await db.commit()
        await db.refresh(db_demand)
        return db_demand
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail="Error creating demand")

@router.get("/demands", response_model=list[schemas.Demand])
async def read_demands(db: AsyncSession = Depends(async_session)):
    stmt = select(models.Demand)
    result = await db.execute(stmt)
    demands = result.scalars().all()
    return demands
