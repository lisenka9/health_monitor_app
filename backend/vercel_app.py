# vercel_app.py - полная версия для Vercel
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import os
import uuid
import hashlib
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_IcLF8sq2Pban@ep-withered-star-ami4gesr-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = os.getenv("SECRET_KEY", "healthmonitorsupersecretkey2026courseworkzimina")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer(auto_error=False)

def get_password_hash(password: str) -> str:
    salt = os.getenv("PASSWORD_SALT", "vercel-salt-2026")
    return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"})
    
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found", headers={"WWW-Authenticate": "Bearer"})
    return user

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BloodPressure(Base):
    __tablename__ = "blood_pressure"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    systolic = Column(Integer, nullable=False)
    diastolic = Column(Integer, nullable=False)
    pulse = Column(Integer)
    date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)

class BloodGlucose(Base):
    __tablename__ = "blood_glucose"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, default="mg/dL")
    date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)

class Weight(Base):
    __tablename__ = "weight"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, default="kg")
    date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)

class WellnessEntry(Base):
    __tablename__ = "wellness_entries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(Text)
    mood = Column(String)
    symptoms = Column(Text)
    date = Column(DateTime(timezone=True), server_default=func.now())

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class BloodPressureCreate(BaseModel):
    systolic: int
    diastolic: int
    pulse: Optional[int] = None
    notes: Optional[str] = None

class BloodPressureResponse(BloodPressureCreate):
    id: int
    user_id: int
    date: datetime

class BloodGlucoseCreate(BaseModel):
    value: float
    unit: str = "mg/dL"
    notes: Optional[str] = None

class BloodGlucoseResponse(BloodGlucoseCreate):
    id: int
    user_id: int
    date: datetime

class WeightCreate(BaseModel):
    value: float
    unit: str = "kg"
    notes: Optional[str] = None

class WeightResponse(WeightCreate):
    id: int
    user_id: int
    date: datetime

class WellnessEntryCreate(BaseModel):
    description: Optional[str] = None
    mood: Optional[str] = None
    symptoms: Optional[str] = None

class WellnessEntryResponse(WellnessEntryCreate):
    id: int
    user_id: int
    date: datetime

app = FastAPI(
    title="Health Monitor API",
    description="API для управления медицинскими данными",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://health-monitor-frontend-roan.vercel.app",
        "http://localhost:3000",
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Health Monitor API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/auth/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed,
        full_name=user_data.full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/auth/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/api/blood-pressure", response_model=BloodPressureResponse, status_code=201)
def create_bp(data: BloodPressureCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bp = BloodPressure(**data.model_dump(), user_id=current_user.id)
    db.add(bp)
    db.commit()
    db.refresh(bp)
    return bp

@app.get("/api/blood-pressure", response_model=List[BloodPressureResponse])
def get_bp_history(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(BloodPressure).filter(BloodPressure.user_id == current_user.id).offset(skip).limit(limit).all()

@app.delete("/api/blood-pressure/{bp_id}", status_code=204)
def delete_bp(bp_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bp = db.query(BloodPressure).filter(BloodPressure.id == bp_id, BloodPressure.user_id == current_user.id).first()
    if not bp:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(bp)
    db.commit()

@app.post("/api/blood-glucose", response_model=BloodGlucoseResponse, status_code=201)
def create_glucose(data: BloodGlucoseCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = BloodGlucose(**data.model_dump(), user_id=current_user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/api/blood-glucose", response_model=List[BloodGlucoseResponse])
def get_glucose_history(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(BloodGlucose).filter(BloodGlucose.user_id == current_user.id).offset(skip).limit(limit).all()

@app.post("/api/weight", response_model=WeightResponse, status_code=201)
def create_weight(data: WeightCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = Weight(**data.model_dump(), user_id=current_user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/api/weight", response_model=List[WeightResponse])
def get_weight_history(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Weight).filter(Weight.user_id == current_user.id).offset(skip).limit(limit).all()

@app.post("/api/wellness", response_model=WellnessEntryResponse, status_code=201)
def create_wellness(data: WellnessEntryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = WellnessEntry(**data.model_dump(), user_id=current_user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/api/wellness", response_model=List[WellnessEntryResponse])
def get_wellness_history(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(WellnessEntry).filter(WellnessEntry.user_id == current_user.id).offset(skip).limit(limit).all()

@app.put("/api/blood-pressure/{bp_id}", response_model=BloodPressureResponse)
def update_bp(bp_id: int, data: BloodPressureCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bp = db.query(BloodPressure).filter(BloodPressure.id == bp_id, BloodPressure.user_id == current_user.id).first()
    if not bp:
        raise HTTPException(status_code=404, detail="Blood pressure measurement not found")
    
    for key, value in data.model_dump().items():
        setattr(bp, key, value)
    db.commit()
    db.refresh(bp)
    return bp

@app.put("/api/blood-glucose/{glucose_id}", response_model=BloodGlucoseResponse)
def update_glucose(glucose_id: int, data: BloodGlucoseCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(BloodGlucose).filter(BloodGlucose.id == glucose_id, BloodGlucose.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Blood glucose measurement not found")
    
    for key, value in data.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@app.delete("/api/blood-glucose/{glucose_id}", status_code=204)
def delete_glucose(glucose_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(BloodGlucose).filter(BloodGlucose.id == glucose_id, BloodGlucose.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Blood glucose measurement not found")
    db.delete(item)
    db.commit()

@app.put("/api/weight/{weight_id}", response_model=WeightResponse)
def update_weight(weight_id: int, data: WeightCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Weight).filter(Weight.id == weight_id, Weight.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Weight measurement not found")
    
    for key, value in data.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@app.delete("/api/weight/{weight_id}", status_code=204)
def delete_weight(weight_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Weight).filter(Weight.id == weight_id, Weight.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Weight measurement not found")
    db.delete(item)
    db.commit()

@app.put("/api/wellness/{entry_id}", response_model=WellnessEntryResponse)
def update_wellness(entry_id: int, data: WellnessEntryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(WellnessEntry).filter(WellnessEntry.id == entry_id, WellnessEntry.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Wellness entry not found")
    
    for key, value in data.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@app.delete("/api/wellness/{entry_id}", status_code=204)
def delete_wellness(entry_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(WellnessEntry).filter(WellnessEntry.id == entry_id, WellnessEntry.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Wellness entry not found")
    db.delete(item)
    db.commit()

@app.get("/api/analytics/dashboard")
def get_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    latest_bp = db.query(BloodPressure).filter(BloodPressure.user_id == current_user.id).order_by(BloodPressure.date.desc()).first()
    latest_glucose = db.query(BloodGlucose).filter(BloodGlucose.user_id == current_user.id).order_by(BloodGlucose.date.desc()).first()
    latest_weight = db.query(Weight).filter(Weight.user_id == current_user.id).order_by(Weight.date.desc()).first()
    
    return {
        "latest_blood_pressure": latest_bp,
        "latest_blood_glucose": latest_glucose,
        "latest_weight": latest_weight,
        "weekly_stats": {}
    }

@app.get("/api/analytics/measurements")
def get_measurements(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    measurement_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not end_date:
        end_date = datetime.utcnow().isoformat()
    if not start_date:
        start_date = (datetime.utcnow() - timedelta(days=30)).isoformat()
    
    start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
    end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    
    results = []
    
    if not measurement_type or measurement_type == "blood_pressure":
        bp_data = db.query(BloodPressure).filter(
            BloodPressure.user_id == current_user.id,
            BloodPressure.date >= start,
            BloodPressure.date <= end
        ).all()
        for item in bp_data:
            results.append({
                "type": "blood_pressure",
                "date": item.date.isoformat(),
                "systolic": item.systolic,
                "diastolic": item.diastolic,
                "pulse": item.pulse,
                "notes": item.notes
            })
    
    if not measurement_type or measurement_type == "blood_glucose":
        glucose_data = db.query(BloodGlucose).filter(
            BloodGlucose.user_id == current_user.id,
            BloodGlucose.date >= start,
            BloodGlucose.date <= end
        ).all()
        for item in glucose_data:
            results.append({
                "type": "blood_glucose",
                "date": item.date.isoformat(),
                "value": item.value,
                "unit": item.unit,
                "notes": item.notes
            })
    
    if not measurement_type or measurement_type == "weight":
        weight_data = db.query(Weight).filter(
            Weight.user_id == current_user.id,
            Weight.date >= start,
            Weight.date <= end
        ).all()
        for item in weight_data:
            results.append({
                "type": "weight",
                "date": item.date.isoformat(),
                "value": item.value,
                "unit": item.unit,
                "notes": item.notes
            })
    
    results.sort(key=lambda x: x["date"])
    
    return {
        "start_date": start_date,
        "end_date": end_date,
        "measurement_type": measurement_type,
        "count": len(results),
        "data": results
    }

@app.get("/api/analytics/stats")
def get_stats(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    bp_data = db.query(BloodPressure).filter(
        BloodPressure.user_id == current_user.id,
        BloodPressure.date >= start_date,
        BloodPressure.date <= end_date
    ).all()
    
    systolic_values = [b.systolic for b in bp_data if b.systolic]
    diastolic_values = [b.diastolic for b in bp_data if b.diastolic]
    
    glucose_data = db.query(BloodGlucose).filter(
        BloodGlucose.user_id == current_user.id,
        BloodGlucose.date >= start_date,
        BloodGlucose.date <= end_date
    ).all()
    glucose_values = [g.value for g in glucose_data if g.value]
    
    # Вес
    weight_data = db.query(Weight).filter(
        Weight.user_id == current_user.id,
        Weight.date >= start_date,
        Weight.date <= end_date
    ).all()
    weight_values = [w.value for w in weight_data if w.value]
    
    return {
        "period_days": days,
        "stats": {
            "blood_pressure": {
                "avg_systolic": sum(systolic_values) / len(systolic_values) if systolic_values else None,
                "avg_diastolic": sum(diastolic_values) / len(diastolic_values) if diastolic_values else None,
                "min_systolic": min(systolic_values) if systolic_values else None,
                "max_systolic": max(systolic_values) if systolic_values else None
            },
            "blood_glucose": {
                "avg": sum(glucose_values) / len(glucose_values) if glucose_values else None,
                "min": min(glucose_values) if glucose_values else None,
                "max": max(glucose_values) if glucose_values else None
            },
            "weight": {
                "avg": sum(weight_values) / len(weight_values) if weight_values else None,
                "min": min(weight_values) if weight_values else None,
                "max": max(weight_values) if weight_values else None
            },
            "wellness_entries": db.query(WellnessEntry).filter(
                WellnessEntry.user_id == current_user.id,
                WellnessEntry.date >= start_date,
                WellnessEntry.date <= end_date
            ).count()
        }
    }