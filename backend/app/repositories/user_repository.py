from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash
from .base import BaseRepository

class UserRepository(BaseRepository[User, UserCreate, UserCreate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def create(self, db: Session, obj_in: UserCreate) -> User:
        obj_in_data = obj_in.model_dump()
        obj_in_data["hashed_password"] = get_password_hash(obj_in_data.pop("password"))
        db_obj = User(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

user_repository = UserRepository(User)