"""Schemas for patient."""

import datetime

from pydantic import BaseModel

from .exams import Exam
from .specdispenses import SpecDispense
from .specprescriptions import SpecPrescription


class PatientBase(BaseModel):
    """Base Pydantic model for Patient."""

    name: str
    dob: datetime.date
    address: str | None
    phonenumber_1: str | None
    phonenumber_2: str | None
    phonenumber_3: str | None
    email: str | None


class PatientCreate(PatientBase):
    """Create Pydantic model for Patient."""

    pass


class PatientUpdate(BaseModel):
    """Update Pydantic model for Patient."""

    name: str | None
    dob: datetime.date | None
    address: str | None
    phonenumber_1: str | None
    phonenumber_2: str | None
    phonenumber_3: str | None
    email: str | None


class Patient(PatientBase):
    """Patient Pydantic model."""

    id: int
    exams: list[Exam] | None
    specprescriptions: list[SpecPrescription] | None
    specdispenses: list[SpecDispense] | None

    class Config:
        """Configuration for Patient model."""

        orm_mode = True
