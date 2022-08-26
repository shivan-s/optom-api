"""CRUD operations for users."""

from sqlalchemy.orm import Session

from app import schemas
from app.auth import get_password_hash
from app.sql import models

# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(password=user.password)
    db_user = models.User(
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, username: str):
    """Get User list."""
    return db.query(models.User).filter(models.User.username == username).one_or_none()


def get_users(db: Session):
    """Get User list."""
    return db.query(models.User).all()
