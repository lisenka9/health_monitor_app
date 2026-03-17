from fastapi import FastAPI
from app.api.middleware import add_cors_middleware
from app.api.routes import auth, users, measurements
from app.api.routes import wellness as wellness_routes
from app.api.routes import analytics as analytics_routes
from app.database import engine, Base, init_db
from app.models import user, measurement, wellness
import logging
import subprocess
import os
import socket


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Инициализация базы данных...")
init_db()
logger.info("База данных готова")

app = FastAPI(
    title="Health Monitor API",
    description="API для мониторинга здоровья и ведения медицинских записей",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def log_version():
    image_version = os.getenv("IMAGE_VERSION", "unknown")
    commit_hash = os.getenv("COMMIT_HASH", "unknown")
    environment = os.getenv("ENVIRONMENT", "development")
    
    logger.info(f"Starting application - Environment: {environment}, Image: {image_version}, Commit: {commit_hash}")
    
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

add_cors_middleware(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(measurements.router)
app.include_router(wellness_routes.router)
app.include_router(analytics_routes.router)

@app.get("/")
def read_root():
    return {"message": "Health Monitor API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/debug/config")
def debug_config():
    from app.config import settings
    return {
        "secret_key_preview": settings.SECRET_KEY[:10] + "...",  
        "algorithm": settings.ALGORITHM,
        "expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "cors_origins": settings.CORS_ORIGINS,
        "database_url": settings.DATABASE_URL,
        "password_salt_preview": settings.PASSWORD_SALT[:10] + "..."
    }

@app.get("/debug/instance")
def get_instance():
    return {
        "hostname": socket.gethostname(),
        "container_id": socket.gethostname()
    }