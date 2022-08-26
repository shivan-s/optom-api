"""Schemas for exams."""

import datetime

from pydantic import BaseModel

from .specprescriptions import SpecPrescription


class ExamBase(BaseModel):
    history: str
    health: str
    date_updated: datetime.datetime


class ExamCreate(ExamBase):
    pass


class ExamUpdate(BaseModel):
    history: str | None
    health: str | None
    patient_id: int | None
    date_updated: datetime.datetime


class Exam(ExamBase):
    id: int
    patient_id: int
    date_created: datetime.datetime
    date_updated: datetime.datetime
    specprescriptions: list[SpecPrescription]

    class Config:
        orm_mode = True
