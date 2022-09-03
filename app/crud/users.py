"""CRUD operations for users."""

from sqlalchemy.orm import Session

from app import schemas
from app.auth import get_password_hash
from app.sql import models


def create_user(db: Session, user: schemas.UserCreate):
    """Create user."""
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


def get_user_by_username(db: Session, username: str):
    """Get user by username."""
    return db.query(models.User).filter(models.User.username == username).one_or_none()


def get_user_by_id(db: Session, user_id: int):
    """Get user by id."""
    return db.query(models.User).filter(models.User.id == user_id).one_or_none()


def get_users(db: Session):
    """Get user list."""
    return db.query(models.User).all()


def update_user(db: Session, user_id: int, user_updates: schemas.UserUpdate):
    """Edit user."""
    db_user = db.query(models.User).filter(models.User.id == user_id).one()
    user_update_data = user_updates.dict(exclude_unset=True)
    for key, value in user_update_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """Delete user."""
    db_user = db.query(models.User).filter(models.User.id == user_id).one()
    db.delete(db_user)
    db.commit()
