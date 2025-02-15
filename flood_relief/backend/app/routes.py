# backend/app/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

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
