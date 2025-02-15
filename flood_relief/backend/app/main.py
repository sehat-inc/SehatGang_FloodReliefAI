from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from geoalchemy2 import WKTElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from . import models
from . import schemas
from .database import async_session

app = FastAPI(title="Disaster Relief API")

templates = Jinja2Templates(directory="templates")

# Dependency to get an async database session
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# --- Existing API endpoints ---

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
    return [schemas.DemandResponse.from_orm(demand) for demand in demands]

@app.post("/demands/", response_model=schemas.AllocationResponse)
async def create_demand_allocation(
    demand: schemas.DemandCreate,
    db: AsyncSession = Depends(get_db)
):
    # Convert the location data to WKT
    wkt_str = f"POINT({demand.location.longitude} {demand.location.latitude})"
    demand_instance = models.Demand(
        type=demand.type.value,  # convert enum if needed
        quantity=demand.quantity,
        priority=demand.priority,
        location=WKTElement(wkt_str, srid=4326)
    )
    db.add(demand_instance)
    await db.commit()
    await db.refresh(demand_instance)
    
    # Query for a resource at the specified location
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
    
    # Deduct the allocated quantity from the resource
    resource.quantity -= demand.quantity
    
    allocation = models.Allocation(
        resource_id=resource.id,
        demand_id=demand_instance.id,
        quantity=demand.quantity
    )
    db.add(allocation)
    await db.commit()
    await db.refresh(allocation)
    
    return allocation

# --- Frontend Endpoints ---

# Render the demand submission form
@app.get("/demand-form", response_class=HTMLResponse)
async def demand_form(request: Request):
    return templates.TemplateResponse("demand_form.html", {"request": request})

# Process form submission and create an allocation
@app.post("/submit-demand", response_class=HTMLResponse)
async def submit_demand(
    request: Request,
    type: str = Form(...),
    quantity: int = Form(...),
    priority: int = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Convert form data into a WKT string
    wkt_str = f"POINT({longitude} {latitude})"
    # Create a new demand instance
    demand_instance = models.Demand(
        type=type,
        quantity=quantity,
        priority=priority,
        location=WKTElement(wkt_str, srid=4326)
    )
    db.add(demand_instance)
    await db.commit()
    await db.refresh(demand_instance)
    
    # Find a matching resource using ST_Equals
    resource_query = select(models.Resource).where(
        func.ST_Equals(models.Resource.location, WKTElement(wkt_str, srid=4326))
    )
    resource_result = await db.execute(resource_query)
    resource = resource_result.scalars().first()
    
    if resource is None:
        await db.rollback()
        return templates.TemplateResponse("error.html", {"request": request, "error": "No resource available at the specified location"})
    
    if resource.quantity < quantity:
        await db.rollback()
        return templates.TemplateResponse("error.html", {"request": request, "error": "Not enough resources available"})
    
    resource.quantity -= quantity
    
    allocation = models.Allocation(
        resource_id=resource.id,
        demand_id=demand_instance.id,
        quantity=quantity
    )
    db.add(allocation)
    await db.commit()
    await db.refresh(allocation)
    
    return templates.TemplateResponse("allocation_success.html", {"request": request, "allocation": allocation})
