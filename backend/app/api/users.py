from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserRoleUpdate
from app.services.auth_service import require_role

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    admin = Depends(require_role(["admin"]))
):
    return db.query(User).all()

@router.patch("/{id}/role")
def update_user_role(
    id: int,
    data: UserRoleUpdate,
    db: Session = Depends(get_db),
    admin = Depends(require_role(["admin"]))
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user.role = data.role
    db.commit()
    return {"message": f"Updated user {user.email} to role {user.role}"}
