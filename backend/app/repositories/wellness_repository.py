from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.wellness import WellnessEntry
from app.schemas.wellness import WellnessEntryCreate, WellnessEntryUpdate
from .base import BaseRepository

class WellnessRepository(BaseRepository[WellnessEntry, WellnessEntryCreate, WellnessEntryUpdate]):
    def get_by_user_and_date_range(
        self, 
        db: Session, 
        user_id: int, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[WellnessEntry]:
        return db.query(WellnessEntry).filter(
            WellnessEntry.user_id == user_id,
            WellnessEntry.date >= start_date,
            WellnessEntry.date <= end_date
        ).all()
    
    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[WellnessEntry]:
        return db.query(WellnessEntry).filter(
            WellnessEntry.user_id == user_id
        ).offset(skip).limit(limit).all()

wellness_repository = WellnessRepository(WellnessEntry)