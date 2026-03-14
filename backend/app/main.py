from fastapi import FastAPI
from app.api.middleware import add_cors_middleware
from app.api.routes import auth, users, measurements
from app.api.routes import wellness as wellness_routes
from app.api.routes import analytics as analytics_routes 
from app.database import engine, Base
from app.models import user, measurement, wellness

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Health Monitor API",
    description="API для мониторинга здоровья и ведения медицинских записей",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)