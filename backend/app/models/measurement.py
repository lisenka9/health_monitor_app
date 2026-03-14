from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class BloodPressure(Base):
    __tablename__ = "blood_pressure"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    systolic = Column(Integer, nullable=False)  
    diastolic = Column(Integer, nullable=False) 
    pulse = Column(Integer) 
    date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)
    
    user = relationship("User")

class BloodGlucose(Base):
    __tablename__ = "blood_glucose"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, default="mg/dL")
    date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)
    
    user = relationship("User")

class Weight(Base):
    __tablename__ = "weight"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, default="kg")
    date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)
    
    user = relationship("User")