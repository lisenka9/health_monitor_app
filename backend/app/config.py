from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv
import os
load_dotenv()
class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "healthmonitorsupersecretkey2026courseworkzimina")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    @property
    def CORS_ORIGINS(self) -> List[str]:
        cors_origins = os.getenv("CORS_ORIGINS", "http://localhost,http://localhost:80,http://localhost:3000,http://localhost:8080")
        return [origin.strip() for origin in cors_origins.split(",")]
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:////app/data/health_monitor.db")
    PASSWORD_SALT: str = os.getenv("PASSWORD_SALT", "health_monitor_salt_2026")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "healthuser")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "healthpass")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "healthdb")
    
    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()