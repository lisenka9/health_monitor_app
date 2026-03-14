from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.api.dependencies import get_current_user
from app.schemas.user import User
from app.schemas.wellness import WellnessEntry, WellnessEntryCreate, WellnessEntryUpdate
from app.repositories.wellness_repository import wellness_repository

router = APIRouter(prefix="/api", tags=["wellness"])

@router.post("/wellness", response_model=WellnessEntry, status_code=status.HTTP_201_CREATED)
def create_wellness_entry(
    wellness_data: WellnessEntryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    wellness_data_dict = wellness_data.model_dump()
    wellness_data_dict["user_id"] = current_user.id
    return wellness_repository.create(db, wellness_data_dict)

@router.get("/wellness", response_model=List[WellnessEntry])
def get_wellness_history(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return wellness_repository.get_by_user(db, current_user.id, skip, limit)

@router.get("/wellness/{entry_id}", response_model=WellnessEntry)
def get_wellness_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entry = wellness_repository.get(db, entry_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wellness entry not found"
        )
    if entry.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return entry

@router.put("/wellness/{entry_id}", response_model=WellnessEntry)
def update_wellness_entry(
    entry_id: int,
    wellness_data: WellnessEntryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entry = wellness_repository.get(db, entry_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wellness entry not found"
        )
    if entry.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return wellness_repository.update(db, entry, wellness_data)

@router.delete("/wellness/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wellness_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entry = wellness_repository.get(db, entry_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wellness entry not found"
        )
    if entry.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    wellness_repository.delete(db, entry_id)
    return None