# backend/app/models.py
from sqlalchemy import Column, Integer, String
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
