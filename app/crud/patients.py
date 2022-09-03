"""CRUD operations for patients."""

import datetime

from sqlalchemy.orm import Session

from app import schemas
from app.sql import models


def create_patient(db: Session, patient: schemas.PatientCreate):
    """Create patient on database."""
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_patients(db: Session, skip: int = 0, limit: int = 100):
    """Get patient from database."""
    return db.query(models.Patient).offset(skip).limit(limit).all()


def get_patient(db: Session, patient_id: int):
    """Get patient by id."""
    return (
        db.query(models.Patient).filter(models.Patient.id == patient_id).one_or_none()
    )


def get_patient_by_name(db: Session, patient_name: str):
    """Get a patients by name."""
    return db.query(models.Patient).where(models.Patient.name == patient_name).all()


def get_patient_by_dob(db: Session, patient_dob: datetime.date):
    """Get a patients by date of birth."""
    return db.query(models.Patient).where(models.Patient.dob == patient_dob).all()


def get_patient_by_name_and_dob(
    db: Session, patient_name: str, patient_dob: datetime.date
):
    """Get a patient by both name and date of birth."""
    return (
        db.query(models.Patient)
        .where(models.Patient.name == patient_name)
        .where(models.Patient.dob == patient_dob)
        .all()
    )


def update_patient(
    db: Session, patient_id: int, patient_updates: schemas.PatientUpdate
):
    """Update a patient by id."""
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).one()
    patient_update_data = patient_updates.dict(exclude_unset=True)
    for key, value in patient_update_data.items():
        setattr(db_patient, key, value)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: int):
    """Delete a patient by id."""
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).one()
    db.delete(db_patient)
    db.commit()
