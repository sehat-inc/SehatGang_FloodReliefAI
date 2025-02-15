# models.py
from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .database import Base
from geoalchemy2.shape import to_shape
from shapely.geometry import Point

class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    
    __table_args__ = (
        CheckConstraint("type IN ('boat', 'shelter', 'food')", name='valid_resource_type'),
        CheckConstraint("quantity >= 0", name='valid_quantity'),
    )
    
    allocations = relationship("Allocation", back_populates="resource")

    def get_coordinates(self):
        if self.location is not None:
            point = to_shape(self.location)
            return {"longitude": point.x, "latitude": point.y}
        return None

class Demand(Base):
    __tablename__ = "demands"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    priority = Column(Integer, nullable=False)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    
    __table_args__ = (
        CheckConstraint("type IN ('boat', 'shelter', 'food')", name='valid_demand_type'),
        CheckConstraint("quantity > 0", name='valid_demand_quantity'),
        CheckConstraint("priority BETWEEN 1 AND 5", name='valid_priority'),
    )
    
    allocations = relationship("Allocation", back_populates="demand")

    def get_coordinates(self):
        if self.location is not None:
            point = to_shape(self.location)
            return {"longitude": point.x, "latitude": point.y}
        return None

class Allocation(Base):
    __tablename__ = "allocations"
    
    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey('resources.id', ondelete='CASCADE'), nullable=False)
    demand_id = Column(Integer, ForeignKey('demands.id', ondelete='CASCADE'), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    __table_args__ = (
        CheckConstraint("quantity > 0", name='valid_allocation_quantity'),
    )
    
    resource = relationship("Resource", back_populates="allocations")
    demand = relationship("Demand", back_populates="allocations")