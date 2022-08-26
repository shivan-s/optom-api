"""Access database."""

from sqlalchemy.orm import Session

from app.sql import models


def get_user(db: Session, username: str):
    """Get User."""
    return db.query(models.User).filter(models.User.username == username).one_or_none()
