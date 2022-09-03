"""Schema for dispensers."""

from pydantic import BaseModel


class DispenserBase(BaseModel):
    """Base Pydantic model for Dispenser."""

    registration: str


class DispenserCreate(DispenserBase):
    """Create Pydantic model for Dispenser."""

    pass


class DispenserUpdate(BaseModel):
    """Update Pydantic model for Dispenser."""

    pass


class Dispenser(DispenserBase):
    """Dispenser Pydantic model."""

    id: int
    user_id: int
    is_active: bool

    class Config:
        """Configuration for Dispenser."""

        orm_mode = True
