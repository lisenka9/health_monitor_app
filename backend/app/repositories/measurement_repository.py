from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.measurement import BloodPressure, BloodGlucose, Weight
from app.schemas.measurement import BloodPressureCreate, BloodPressureUpdate, BloodGlucoseCreate, BloodGlucoseUpdate, WeightCreate, WeightUpdate
from .base import BaseRepository

class BloodPressureRepository(BaseRepository[BloodPressure, BloodPressureCreate, BloodPressureUpdate]):
    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[BloodPressure]:
        return db.query(BloodPressure).filter(
            BloodPressure.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_by_user_and_date_range(self, db: Session, user_id: int, 
                              start_date: datetime, end_date: datetime) -> List[BloodPressure]:
        if start_date.tzinfo is not None:
            start_date = start_date.replace(tzinfo=None)
        if end_date.tzinfo is not None:
            end_date = end_date.replace(tzinfo=None)
        
        return db.query(BloodPressure).filter(
            BloodPressure.user_id == user_id,
            BloodPressure.date >= start_date,
            BloodPressure.date <= end_date
        ).all()

blood_pressure_repository = BloodPressureRepository(BloodPressure)

class BloodGlucoseRepository(BaseRepository[BloodGlucose, BloodGlucoseCreate, BloodGlucoseUpdate]):
    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[BloodGlucose]:
        return db.query(BloodGlucose).filter(
            BloodGlucose.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_by_user_and_date_range(self, db: Session, user_id: int, start_date: datetime, end_date: datetime) -> List[BloodGlucose]:
        if start_date.tzinfo is not None:
            start_date = start_date.replace(tzinfo=None)
        if end_date.tzinfo is not None:
            end_date = end_date.replace(tzinfo=None)
        
        return db.query(BloodGlucose).filter(
            BloodGlucose.user_id == user_id,
            BloodGlucose.date >= start_date,
            BloodGlucose.date <= end_date
        ).all()

blood_glucose_repository = BloodGlucoseRepository(BloodGlucose)

class WeightRepository(BaseRepository[Weight, WeightCreate, WeightUpdate]):
    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Weight]:
        return db.query(Weight).filter(
            Weight.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_by_user_and_date_range(self, db: Session, user_id: int, start_date: datetime, end_date: datetime) -> List[Weight]:
        if start_date.tzinfo is not None:
            start_date = start_date.replace(tzinfo=None)
        if end_date.tzinfo is not None:
            end_date = end_date.replace(tzinfo=None)

        return db.query(Weight).filter(
            Weight.user_id == user_id,
            Weight.date >= start_date,
            Weight.date <= end_date
        ).all()

weight_repository = WeightRepository(Weight)