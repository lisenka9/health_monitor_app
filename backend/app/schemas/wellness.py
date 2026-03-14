from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WellnessEntryBase(BaseModel):
    description: Optional[str] = None
    mood: Optional[str] = None
    symptoms: Optional[str] = None

class WellnessEntryCreate(WellnessEntryBase):
    pass

class WellnessEntryUpdate(WellnessEntryBase):
    pass

class WellnessEntry(WellnessEntryBase):
    id: int
    user_id: int
    date: datetime
    
    class Config:
        from_attributes = True