"""Schemas for Spec dispenses."""

from pydantic import BaseModel


class SpecDispenseBase(BaseModel):
    """Base Pydantic model for SpecDipense."""

    frame: str


class SpecDispenseCreate(SpecDispenseBase):
    """Create Pydantic model for SpecDispense."""

    pass


class SpecDispenseUpdate(BaseModel):
    """Update Pydantic model for SpecDispense."""

    pass


class SpecDispense(SpecDispenseBase):
    """SpecDispense Pydantic model."""

    id: int
    patient_id: int
    spec_prescription_id: int
    user_id: int
    optometrist_id: int

    class Config:
        """Configuration for SpecDispense."""

        orm_mode = True
