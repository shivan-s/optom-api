"""Schemas for Spec dispenses."""

from pydantic import BaseModel


class SpecDispenseBase(BaseModel):
    frame: str


class SpecDispenseCreate(SpecDispenseBase):
    pass


class SpecDispenseUpdate(BaseModel):
    pass


class SpecDispense(SpecDispenseBase):
    id: int
    patient_id: int
    spec_prescription_id: int
    user_id: int
    optometrist_id: int

    class Config:
        orm_mode = True
