from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.api.dependencies import get_current_user
from app.schemas.user import User
from app.schemas.measurement import (
    BloodPressure, BloodPressureCreate,
    BloodGlucose, BloodGlucoseCreate,
    Weight, WeightCreate
)
from app.repositories.measurement_repository import (
    blood_pressure_repository,
    blood_glucose_repository,
    weight_repository
)

router = APIRouter(prefix="/api", tags=["measurements"])

@router.post("/blood-pressure", response_model=BloodPressure, status_code=status.HTTP_201_CREATED)
def create_blood_pressure(
    bp_data: BloodPressureCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bp_data_dict = bp_data.model_dump()
    bp_data_dict["user_id"] = current_user.id
    return blood_pressure_repository.create(db, bp_data_dict)

@router.get("/blood-pressure", response_model=List[BloodPressure])
def get_blood_pressure_history(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return blood_pressure_repository.get_by_user(db, current_user.id, skip, limit)

@router.put("/blood-pressure/{id}", response_model=BloodPressure)
def update_blood_pressure(
    id: int,
    bp_data: BloodPressureCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bp = blood_pressure_repository.get(db, id)
    if not bp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood pressure measurement not found"
        )
    if bp.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return blood_pressure_repository.update(db, bp, bp_data)

@router.delete("/blood-pressure/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blood_pressure(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bp = blood_pressure_repository.get(db, id)
    if not bp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood pressure measurement not found"
        )
    if bp.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    blood_pressure_repository.delete(db, id)
    return None

@router.post("/blood-glucose", response_model=BloodGlucose, status_code=status.HTTP_201_CREATED)
def create_blood_glucose(
    bg_data: BloodGlucoseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bg_data_dict = bg_data.model_dump()
    bg_data_dict["user_id"] = current_user.id
    return blood_glucose_repository.create(db, bg_data_dict)

@router.get("/blood-glucose", response_model=List[BloodGlucose])
def get_blood_glucose_history(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return blood_glucose_repository.get_by_user(db, current_user.id, skip, limit)

@router.put("/blood-glucose/{id}", response_model=BloodGlucose)
def update_blood_glucose(
    id: int,
    bg_data: BloodGlucoseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bg = blood_glucose_repository.get(db, id)
    if not bg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood glucose measurement not found"
        )
    if bg.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return blood_glucose_repository.update(db, bg, bg_data)

@router.delete("/blood-glucose/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blood_glucose(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bg = blood_glucose_repository.get(db, id)
    if not bg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blood glucose measurement not found"
        )
    if bg.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    blood_glucose_repository.delete(db, id)
    return None

@router.post("/weight", response_model=Weight, status_code=status.HTTP_201_CREATED)
def create_weight(
    weight_data: WeightCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    weight_data_dict = weight_data.model_dump()
    weight_data_dict["user_id"] = current_user.id
    return weight_repository.create(db, weight_data_dict)

@router.get("/weight", response_model=List[Weight])
def get_weight_history(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return weight_repository.get_by_user(db, current_user.id, skip, limit)

@router.put("/weight/{id}", response_model=Weight)
def update_weight(
    id: int,
    weight_data: WeightCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    weight = weight_repository.get(db, id)
    if not weight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weight measurement not found"
        )
    if weight.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return weight_repository.update(db, weight, weight_data)

@router.delete("/weight/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_weight(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    weight = weight_repository.get(db, id)
    if not weight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weight measurement not found"
        )
    if weight.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    weight_repository.delete(db, id)
    return None