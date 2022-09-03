"""Schemas for spectacle prescriptions."""

import decimal

from pydantic import BaseModel

from .specdispenses import SpecDispense


class SpecPrescriptionBase(BaseModel):
    """Base Pydantic model for SpecPrescription."""

    right_sphere: decimal.Decimal
    right_cylinder: decimal.Decimal
    right_axis: decimal.Decimal
    right_add: decimal.Decimal
    right_inter_add: decimal.Decimal
    left_sphere: decimal.Decimal
    left_cylinder: decimal.Decimal
    left_axis: decimal.Decimal
    left_add: decimal.Decimal
    left_inter_add: decimal.Decimal

    class Config:
        """Configuration for SpecPrescription."""

        orm_mode = True


class SpecPrescriptionCreate(SpecPrescriptionBase):
    """Create Pydantic model for SpecPrescrption."""

    pass


class SpecPrescriptionUpdate(BaseModel):
    """Update Pydantic model for SpecPrescrption."""

    pass


class SpecPrescription(SpecPrescriptionBase):
    """SpecPrescrption Pydantic model."""

    id: int
    exam_id: int
    patient_id: int
    optometrist_id: int
    specdispenses: list[SpecDispense]
