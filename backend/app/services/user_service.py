from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate, User

class UserService:
    def create_user(self, db: Session, user_create: UserCreate) -> User:
        existing_user = user_repository.get_by_email(db, user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        return user_repository.create(db, user_create)
    
    def get_user_by_email(self, db: Session, email: str) -> User:
        user = user_repository.get_by_email(db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

user_service = UserService()