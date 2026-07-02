from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.dependencies import get_current_admin
from app.models.user import User
from app.schemas.user import User as UserSchema

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get(
    "/users",
    response_model=list[UserSchema],
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Admin access required"}
    }
)
def get_all_users(
    admin_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return users

@router.get(
    "/users/{user_id}",
    response_model=UserSchema,
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Admin access required"},
        404: {"description": "User not found"}
    }
)
def get_user_by_id(
    user_id: int,
    admin_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put(
    "/users/{user_id}/role",
    responses={
        400: {"description": "Invalid role"},
        401: {"description": "Not authenticated"},
        403: {"description": "Admin access required"},
        404: {"description": "User not found"}
    }
)
def change_user_role(
    user_id: int,
    new_role: str,
    admin_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    if new_role not in ["user", "admin"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role. Must be 'user' or 'admin'")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.role = new_role
    db.commit()
    db.refresh(user)
    return {"message": f"User {user.email} role changed to {new_role}"}