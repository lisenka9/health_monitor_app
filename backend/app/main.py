from fastapi import FastAPI
from app.api.middleware import add_cors_middleware
from app.api.routes import auth, users, measurements
from app.api.routes import wellness as wellness_routes
from app.api.routes import analytics as analytics_routes
from app.database import init_db
import os
import socket
import uuid
import structlog
import asyncio
import signal
from contextlib import asynccontextmanager
from app.core.logging import setup_logging, get_logger
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi

security_scheme = HTTPBearer()
app = FastAPI(
    title="Health Monitor API",
    description="API для мониторинга здоровья и ведения медицинских записей",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            # Пропускаем пути, которые не требуют авторизации
            if not path.startswith("/auth") and path not in ["/", "/health", "/openapi.json", "/docs", "/redoc"]:
                openapi_schema["paths"][path][method]["security"] = [{"Bearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
security = HTTPBearer(auto_error=False)
setup_logging()
logger = get_logger("health-monitor")

shutdown_event = asyncio.Event()

def handle_signal(signum, frame):
    """Обработчик сигналов SIGTERM и SIGINT"""
    logger.info("received_signal", signal=signum, message="Shutting down gracefully...")
    shutdown_event.set()

signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("application_starting")
    
    logger.info("database_initializing")
    init_db()
    logger.info("database_ready")
    
    image_version = os.getenv("IMAGE_VERSION", "unknown")
    commit_hash = os.getenv("COMMIT_HASH", "unknown")
    environment = os.getenv("ENVIRONMENT", "development")
    logger.info("application_started",
                environment=environment,
                image_version=image_version,
                commit_hash=commit_hash)
    
    yield
    
    logger.info("application_shutting_down")
    
    try:
        await asyncio.wait_for(shutdown_event.wait(), timeout=30.0)
    except asyncio.TimeoutError:
        logger.warning("shutdown_timeout", message="Forced shutdown after timeout")
    
    from app.database import engine
    engine.dispose()
    logger.info("database_connections_closed")
    
    logger.info("application_shutdown_complete")


@app.middleware("http")
async def log_requests_middleware(request, call_next):
    if shutdown_event.is_set():
        from fastapi.responses import JSONResponse
        logger.warning("request_rejected", 
                       method=request.method,
                       path=request.url.path,
                       reason="shutting_down")
        return JSONResponse(
            status_code=503,
            content={"detail": "Service is shutting down, please try again later"}
        )
    
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    structlog.contextvars.bind_contextvars(request_id=request_id)
    
    logger.info("request_started", 
                method=request.method,
                path=request.url.path,
                client=request.client.host if request.client else "unknown")
    
    try:
        response = await call_next(request)
        logger.info("request_completed",
                    method=request.method,
                    path=request.url.path,
                    status_code=response.status_code)
        response.headers["X-Request-ID"] = request_id
        return response
    except Exception as e:
        logger.error("request_failed",
                     method=request.method,
                     path=request.url.path,
                     error=str(e))
        raise
    finally:
        structlog.contextvars.clear_contextvars()

add_cors_middleware(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(measurements.router)
app.include_router(wellness_routes.router)
app.include_router(analytics_routes.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is running"}

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

@app.get("/debug/sleep")
async def sleep_test(seconds: int = 10):
    """Тестовый эндпоинт для проверки graceful shutdown"""
    logger.info("sleep_started", seconds=seconds)
    await asyncio.sleep(seconds)
    logger.info("sleep_completed")
    return {"status": "ok", "slept": seconds}