"""CRUD operations for patients."""

import datetime

from sqlalchemy.orm import Session

from app import schemas
from app.sql import models


def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()


def get_patient(db: Session, patient_id: int):
    """Get User list."""
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()


def get_patient_by_name(db: Session, patient_name: str):
    return db.query(models.Patient).where(models.Patient.name == patient_name).all()


def get_patient_by_dob(db: Session, patient_dob: datetime.date):
    return db.query(models.Patient).where(models.Patient.dob == patient_dob).all()


def get_patient_by_name_and_dob(
    db: Session, patient_name: str, patient_dob: datetime.date
):
    return (
        db.query(models.Patient)
        .where(models.Patient.name == patient_name)
        .where(models.Patient.dob == patient_dob)
        .all()
    )


def update_patient(
    db: Session, patient_id: int, patient_updates: schemas.PatientUpdate
):
    db_patient = (
        db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    )
    patient_update_data = patient_updates.dict(exclude_unset=True)
    for key, value in patient_update_data.items():
        setattr(db_patient, key, value)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: int):
    db_patient = (
        db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    )
    db.delete(db_patient)
    db.commit()
