"""Routes for user data."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.auth import get_current_user
from app.sql.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.User, status_code=201)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
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
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not sufficient credentials",
        )
    db_users = crud.get_user(username=username, db=db)
    return db_users
