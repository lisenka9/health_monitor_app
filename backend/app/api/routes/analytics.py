from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.api.dependencies import get_current_user
from app.schemas.user import User
from app.services.analytics_service import analytics_service
from app.utils.validators import medical_validator

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/measurements")
def get_measurements_for_period(
    start_date: Optional[datetime] = Query(None, description="Start date for filtering"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering"),
    measurement_type: Optional[str] = Query(None, description="Type of measurement: blood_pressure, blood_glucose, weight"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not end_date:
        end_date = datetime.now()
    if not start_date:
        start_date = end_date - timedelta(days=30)
    date_validation = medical_validator.validate_date_range(start_date, end_date)
    if not date_validation["is_valid"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=date_validation["errors"]
        )
    
    measurements = analytics_service.get_measurements_by_date_range(
        db, current_user.id, start_date, end_date, measurement_type
    )
    
    return {
        "start_date": start_date,
        "end_date": end_date,
        "measurement_type": measurement_type,
        "count": len(measurements),
        "data": measurements
    }

@router.get("/stats")
def get_measurements_stats(
    days: int = Query(30, ge=1, le=365, description="Number of days for statistics"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stats = analytics_service.get_measurements_stats(db, current_user.id, days)
    
    return {
        "period_days": days,
        "stats": stats
    }

@router.get("/dashboard")
def get_dashboard_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение данных для главной страницы (дашборда)"""
    latest_bp = analytics_service.get_measurements_by_date_range(
        db, current_user.id, 
        datetime.now() - timedelta(days=1), 
        datetime.now(),
        'blood_pressure'
    )
    
    latest_glucose = analytics_service.get_measurements_by_date_range(
        db, current_user.id,
        datetime.now() - timedelta(days=1),
        datetime.now(), 
        'blood_glucose'
    )
    
    latest_weight = analytics_service.get_measurements_by_date_range(
        db, current_user.id,
        datetime.now() - timedelta(days=7),
        datetime.now(),
        'weight'
    )
    weekly_stats = analytics_service.get_measurements_stats(db, current_user.id, 7)
    
    return {
        "latest_blood_pressure": latest_bp[-1] if latest_bp else None,
        "latest_blood_glucose": latest_glucose[-1] if latest_glucose else None,
        "latest_weight": latest_weight[-1] if latest_weight else None,
        "weekly_stats": weekly_stats
    }