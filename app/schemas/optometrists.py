"""Schema for optometrists."""

from pydantic import BaseModel

from .exams import Exam
from .specprescriptions import SpecPrescription


class OptometristBase(BaseModel):
    """Base Pydantic model for Optometrist."""

    registration: str


class OptometristCreate(OptometristBase):
    """Create Pydantic model for Optometrist."""

    pass


class OptometristUpdate(BaseModel):
    """Update Pydantic model for Optometrist."""

    pass


class Optometrist(OptometristBase):
    """Optometrist Pydantic model."""

    id: int
    user_id: int
    is_active: bool
    exams: list[Exam]
    specprescriptions: list[SpecPrescription]

    class Config:
        """Configuration settings for Optometrist Pydantic model."""

        orm_mode = True
