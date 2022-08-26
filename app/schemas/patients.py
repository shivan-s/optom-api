"""Schemas for patient."""

import datetime

from pydantic import BaseModel

from .exams import Exam
from .specdispenses import SpecDispense
from .specprescriptions import SpecPrescription


class PatientBase(BaseModel):
    name: str
    dob: datetime.date
    address: str | None
    phonenumber_1: str | None
    phonenumber_2: str | None
    phonenumber_3: str | None
    email: str | None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: str | None
    dob: datetime.date | None
    address: str | None
    phonenumber_1: str | None
    phonenumber_2: str | None
    phonenumber_3: str | None
    email: str | None


class Patient(PatientBase):
    id: int
    exams: list[Exam] | None
    specprescriptions: list[SpecPrescription] | None
    specdispenses: list[SpecDispense] | None

    class Config:
        orm_mode = True
