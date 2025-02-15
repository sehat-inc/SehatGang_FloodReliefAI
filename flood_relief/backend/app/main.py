# main.py
from fastapi import FastAPI, Depends, HTTPException
from geoalchemy2 import WKTElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from . import models, schemas
from .database import async_session
from .utils import get_coordinates
from ortools.linear_solver import pywraplp
from .utils import haversine


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
        # Convert city to coordinates
        longitude, latitude = await get_coordinates(demand.city)
        wkt_str = f"POINT({longitude} {latitude})"

        # Create demand first
        demand_instance = models.Demand(
            type=demand.type.value,
            quantity=demand.quantity,
            priority=demand.priority,
            location=WKTElement(wkt_str, srid=4326)
        )
        db.add(demand_instance)
        await db.commit()
        await db.refresh(demand_instance)

        # Find all matching resources within 50km (0.45 degrees ≈ 50km)
        resource_query = select(models.Resource).where(
            func.ST_DWithin(
                models.Resource.location,
                WKTElement(wkt_str, srid=4326),
                0.45
            ),
            models.Resource.type == demand.type.value,
            models.Resource.quantity > 0
        )
        result = await db.execute(resource_query)
        resources = result.scalars().all()

        # Check if total resources are sufficient
        total_available = sum(r.quantity for r in resources)
        if total_available < demand.quantity:
            raise HTTPException(
                status_code=400,
                detail="Insufficient resources in the area"
            )

        # Calculate distances using Haversine formula
        distances = [
            haversine(longitude, latitude, 
                      *r.get_coordinates().values())
            for r in resources
        ]

        # Create OR-Tools solver
        solver = pywraplp.Solver.CreateSolver('SCIP')
        allocations = [
            solver.IntVar(0, r.quantity, f'r_{r.id}')
            for r in resources
        ]

        # Add constraints
        solver.Add(sum(allocations) == demand.quantity)
        
        # Minimize total distance-cost
        objective = solver.Objective()
        for i, d in enumerate(distances):
            objective.SetCoefficient(allocations[i], d)
        objective.SetMinimization()

        # Solve
        status = solver.Solve()

        if status != pywraplp.Solver.OPTIMAL:
            raise HTTPException(
                status_code=400,
                detail="Could not find optimal allocation"
            )

        # Create allocations and update resources
        allocations_created = []
        for resource, allocation_var in zip(resources, allocations):
            alloc_qty = int(allocation_var.solution_value())
            if alloc_qty == 0:
                continue

            resource.quantity -= alloc_qty
            allocation = models.Allocation(
                resource_id=resource.id,
                demand_id=demand_instance.id,
                quantity=alloc_qty
            )
            db.add(allocation)
            allocations_created.append(allocation)

        await db.commit()
        return allocations_created[0]  # Return first allocation for response
        
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))