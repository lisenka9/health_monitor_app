from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, Token, User
from app.services.auth_service import auth_service
from app.services.user_service import user_service
from app.core.logging import get_logger

router = APIRouter(prefix="/auth", tags=["authentication"])
logger = get_logger("health-monitor.auth")

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    logger.info("user_registration_attempted", email=user_create.email)
    try:
        result = user_service.create_user(db, user_create)
        logger.info("user_registration_succeeded", user_id=result.id, email=result.email)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    logger.info("user_login_attempted", email=user_login.email)
    try:
        result = auth_service.login(db, user_login)
        logger.info("user_login_succeeded", email=user_login.email)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )