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