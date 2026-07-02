from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.measurement import BloodPressure, BloodGlucose, Weight
from app.models.wellness import WellnessEntry
from app.utils.security import get_password_hash
from datetime import datetime, timedelta
import random

def seed_database():
    db = SessionLocal()
    test_user = db.query(User).filter(User.email == "test@mail.ru").first()
    if not test_user:
        test_user = User(
            email="test@mail.ru",
            hashed_password=get_password_hash("test123"),
            full_name="Test User",
            role="user"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
    
    admin_user = db.query(User).filter(User.email == "admin@mail.ru").first()
    if not admin_user:
        admin_user = User(
            email="admin@mail.ru",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
    
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        bp = BloodPressure(
            user_id=test_user.id,
            systolic=random.randint(110, 140),
            diastolic=random.randint(70, 90),
            pulse=random.randint(60, 80),
            date=date,
            notes=f"Test measurement {i+1}"
        )
        db.add(bp)
    
    for i in range(20):
        date = datetime.now() - timedelta(days=i)
        glucose = BloodGlucose(
            user_id=test_user.id,
            value=random.randint(70, 120),
            unit="mg/dL",
            date=date,
            notes=f"Test glucose {i+1}"
        )
        db.add(glucose)
    
    for i in range(15):
        date = datetime.now() - timedelta(days=i)
        weight = Weight(
            user_id=test_user.id,
            value=random.randint(65, 80),
            unit="kg",
            date=date,
            notes=f"Test weight {i+1}"
        )
        db.add(weight)
    
    moods = ["good", "normal", "bad"]
    for i in range(10):
        date = datetime.now() - timedelta(days=i)
        wellness = WellnessEntry(
            user_id=test_user.id,
            description=f"Test wellness entry {i+1}",
            mood=random.choice(moods),
            symptoms="None",
            date=date
        )
        db.add(wellness)
    
    db.commit()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()