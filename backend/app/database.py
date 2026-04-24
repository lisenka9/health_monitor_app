from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.core.logging import get_logger

logger = get_logger("health-monitor.database")

logger.info("database_initializing", url=settings.DATABASE_URL[:30] + "...")
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
connect_args = {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args=connect_args,
    pool_pre_ping=True,  
    pool_size=5,         
    max_overflow=10      
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Создание таблиц при запуске"""
    Base.metadata.create_all(bind=engine)
    logger.info("database_ready")