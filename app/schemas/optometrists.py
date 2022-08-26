"""Schema for optometrists."""

from pydantic import BaseModel

from .exams import Exam
from .specprescriptions import SpecPrescription


class OptometristBase(BaseModel):
    registration: str


class OptometristCreate(OptometristBase):
    pass


class OptometristUpdate(BaseModel):
    pass


class Optometrist(OptometristBase):
    id: int
    user_id: int
    is_active: bool
    exams: list[Exam]
    specprescriptions: list[SpecPrescription]

    class Config:
        orm_mode = True
