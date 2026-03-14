from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import user_repository
from app.utils.security import verify_password, create_access_token
from app.config import settings
from app.schemas.user import UserLogin, Token

class AuthService:
    def authenticate_user(self, db: Session, user_login: UserLogin) -> Optional[Token]:
        user = user_repository.get_by_email(db, user_login.email)
        if not user:
            return None
        if not verify_password(user_login.password, user.hashed_password):
            return None
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    
    def login(self, db: Session, user_login: UserLogin) -> Token:
        token = self.authenticate_user(db, user_login)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token

auth_service = AuthService()