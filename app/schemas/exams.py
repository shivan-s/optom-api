"""Schemas for exams."""

import datetime

from pydantic import BaseModel

from .specprescriptions import SpecPrescription


class ExamBase(BaseModel):
    """Base Exam Pydantic model."""

    history: str
    health: str
    date_updated: datetime.datetime


class ExamCreate(ExamBase):
    """Create Exam Pydantic model."""

    pass


class ExamUpdate(BaseModel):
    """Update Exam Pydantic model."""

    history: str | None
    health: str | None
    patient_id: int | None
    date_updated: datetime.datetime


class Exam(ExamBase):
    """Exam Pydantic model."""

    id: int
    patient_id: int
    date_created: datetime.datetime
    date_updated: datetime.datetime
    specprescriptions: list[SpecPrescription]

    class Config:
        """Configuration."""

        orm_mode = True
