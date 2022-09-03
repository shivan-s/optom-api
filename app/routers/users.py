"""Routes for user data."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.auth import get_current_user
from app.sql.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """Create user. Admin can only access this endpoint."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not sufficient credentials",
        )
    db_user = crud.create_user(db=db, user=user)
    return db_user


@router.get("/", response_model=list[schemas.User])
async def read_users(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """Read a list of users. Only admin can access this endpoint."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not sufficient credentials",
        )
    db_users = crud.get_users(db=db)
    return db_users


@router.get("/{username}", response_model=schemas.User)
async def read_user(
    username: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """Read a user by username. Admin can only access this endpoint."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not sufficient credentials",
        )
    db_user = crud.get_user_by_username(username=username, db=db)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.patch("/{username}", response_model=schemas.User)
async def update_user(
    username: str,
    user_updates: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """Edit user by username. Only admin level can access this endpoint."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not sufficient credentials",
        )
    db_user = crud.get_user_by_username(username=username, db=db)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    updated_user = crud.update_user(db, user_id=db_user.id, user_updates=user_updates)
    return updated_user


@router.delete(
    "/{username}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    username: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """Delete user by username. Only admin level can access this endpoint."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not sufficient credentials",
        )
    db_user = crud.get_user_by_username(username=username, db=db)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    crud.delete_user(db, user_id=db_user.id)
