"""Routes for a logged in user to access their data."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.auth import get_current_user
from app.sql.database import get_db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/", response_model=schemas.User)
async def access_self(
    current_user: schemas.User = Depends(get_current_user),
):
    """User can access self their detail."""
    return current_user


@router.patch("/", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def edit_self(
    user_updates: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """User can edit their detail."""
    updated_user = crud.update_user(
        db, user_id=current_user.id, user_updates=user_updates
    )
    return updated_user
