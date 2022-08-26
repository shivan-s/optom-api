"""Schemas for users."""

from pydantic import BaseModel

from .dispensers import Dispenser
from .optometrists import Optometrist
from .specdispenses import SpecDispense


class UserBase(BaseModel):
    username: str
    full_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    pass


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    optometrist: Optometrist | None
    dispenser: Dispenser | None
    specdispenses = list[SpecDispense]

    class Config:
        orm_mode = True
