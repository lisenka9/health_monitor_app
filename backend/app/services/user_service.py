from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate, User
from app.utils.security import get_password_hash

class UserService:
    def create_user(self, db: Session, user_create: UserCreate) -> User:
        existing_user = user_repository.get_by_email(db, user_create.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        user = User(
            email=user_create.email,
            hashed_password=get_password_hash(user_create.password),
            full_name=user_create.full_name,
            role="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_user_by_email(self, db: Session, email: str) -> User:
        user = user_repository.get_by_email(db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

user_service = UserService()