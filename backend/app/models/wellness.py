from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class WellnessEntry(Base):
    __tablename__ = "wellness_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(Text)
    mood = Column(String)  
    symptoms = Column(Text)  
    date = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")