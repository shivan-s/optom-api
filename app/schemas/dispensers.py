"""Schema for dispensers."""

from pydantic import BaseModel


class DispenserBase(BaseModel):
    registration: str


class DispenserCreate(DispenserBase):
    pass


class DispenserUpdate(BaseModel):
    pass


class Dispenser(DispenserBase):
    id: int
    user_id: int
    is_active: bool

    class Config:
        orm_mode = True
