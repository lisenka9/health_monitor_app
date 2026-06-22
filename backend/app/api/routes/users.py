from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app.schemas.user import User
from app.api.dependencies import get_current_user
from app.models.user import User as UserModel

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=User)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

class ProfileUpdate(BaseModel):
    full_name: str
    email: EmailStr

@router.put("/me", response_model=User)
def update_profile(
    profile_data: ProfileUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if profile_data.email != current_user.email:
        existing_user = db.query(UserModel).filter(UserModel.email == profile_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        current_user.email = profile_data.email
    
    current_user.full_name = profile_data.full_name
    
    db.commit()
    db.refresh(current_user)
    
    return current_user