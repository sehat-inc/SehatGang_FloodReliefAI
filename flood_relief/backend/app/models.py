# backend/app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from .database import Base

class Resource(Base):
    __tablename__ = 'resources'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    
    def __repr__(self):
        return f"<Resource(id={self.id}, type={self.type}, quantity={self.quantity})>"

class Demand(Base):
    __tablename__ = 'demands'  # Corrected table name
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    priority = Column(Integer, nullable=False)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    
    def __repr__(self):
        return f"<Demand(id={self.id}, type={self.type}, quantity={self.quantity}, priority={self.priority})>"

class Allocation(Base):
    __tablename__ = 'allocations'
    
    id = Column(Integer, primary_key=True)
    demand_id = Column(Integer, ForeignKey('demands.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    quantity_allocated = Column(Integer, nullable=False)

    demand = relationship("Demand")
    resource = relationship("Resource")
    
    def __repr__(self):
        return f"<Allocation(id={self.id}, demand_id={self.demand_id}, resource_id={self.resource_id}, quantity_allocated={self.quantity_allocated})>"