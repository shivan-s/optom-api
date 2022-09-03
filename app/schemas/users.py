"""Schemas for users."""

from pydantic import BaseModel

from .dispensers import Dispenser
from .optometrists import Optometrist
from .specdispenses import SpecDispense


class UserBase(BaseModel):
    """Base Pydantic model for User."""

    username: str
    full_name: str


class UserCreate(UserBase):
    """Create Pydantic model for User."""

    password: str


class UserUpdate(BaseModel):
    """Update Pydantic model for User."""

    username: str | None
    full_name: str | None


class User(UserBase):
    """User Pydantic model."""

    id: int
    is_active: bool
    is_admin: bool
    optometrist: Optometrist | None
    dispenser: Dispenser | None
    specdispenses = list[SpecDispense]

    class Config:
        """Configuration for User."""

        orm_mode = True
