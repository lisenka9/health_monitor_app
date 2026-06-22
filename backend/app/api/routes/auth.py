from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, Token, User
from app.services.auth_service import auth_service
from app.services.user_service import user_service
from app.core.logging import get_logger

router = APIRouter(prefix="/auth", tags=["authentication"])
logger = get_logger("health-monitor.auth")

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        body = await request.body()
        if not body:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Request body is empty"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid request"
        )
    
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JSON format"
        )
    
    if "email" not in body or "password" not in body or "full_name" not in body:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email, password and full_name are required"
        )
    
    if not body["email"] or not body["password"] or not body["full_name"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email, password and full_name cannot be empty"
        )
    
    if len(body["password"]) < 6:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password must be at least 6 characters long"
        )
    
    try:
        user_create = UserCreate(**body)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Validation error: {str(e)}"
        )
    
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
async def login(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        body_bytes = await request.body()
        if not body_bytes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Request body is empty"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid request"
        )
    
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JSON format"
        )
    
    try:
        user_login = UserLogin(**body)
    except Exception as e:
        logger.error(f"Login parsing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login data"
        )
    
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