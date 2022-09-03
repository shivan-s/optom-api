"""Verifying user."""

from typing import Literal

from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.auth.user import get_user
from app.sql.database import get_db
from app.sql.models import User


def get_pwd_context():
    """Get password cryptopgraphy context."""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password.

    Args:
        plain_password (str): Password provided by user.
        hashed_password (str): Hashed password.

    Returns:
        bool: Determine if the password is correct or not.
    """
    pwd_context = get_pwd_context()
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(
    username: str, password: str, db: Session = Depends(get_db)
) -> User | Literal[False]:
    """Authenticate user.

    Args:
        username (str): Username.
        password (str): Plain password.
        db (Session): Database session.

    Returns:
        bool | User : False if the username does not exist of the password is \
                incorrect. Or the user details if the user is confirmed.
    """
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
