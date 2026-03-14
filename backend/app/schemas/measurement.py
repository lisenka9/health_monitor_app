from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BloodPressureBase(BaseModel):
    systolic: int
    diastolic: int
    pulse: Optional[int] = None
    notes: Optional[str] = None

class BloodPressureCreate(BloodPressureBase):
    pass

class BloodPressureUpdate(BloodPressureBase):
    pass

class BloodPressure(BloodPressureBase):
    id: int
    user_id: int
    date: datetime
    
    class Config:
        from_attributes = True

class BloodGlucoseBase(BaseModel):
    value: float
    unit: str = "mg/dL"
    notes: Optional[str] = None

class BloodGlucoseCreate(BloodGlucoseBase):
    pass

class BloodGlucoseUpdate(BloodGlucoseBase):
    pass

class BloodGlucose(BloodGlucoseBase):
    id: int
    user_id: int
    date: datetime
    
    class Config:
        from_attributes = True

class WeightBase(BaseModel):
    value: float
    unit: str = "kg"
    notes: Optional[str] = None

class WeightCreate(WeightBase):
    pass

class WeightUpdate(WeightBase):
    pass

class Weight(WeightBase):
    id: int
    user_id: int
    date: datetime
    
    class Config:
        from_attributes = True