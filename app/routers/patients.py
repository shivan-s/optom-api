"""Routes for patient data."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.auth import get_current_user
from app.sql.database import get_db

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=schemas.Patient, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
):
    """Create a patient."""
    # db_patient = crud.get_patient_by_name_and_dob(
    #     db, patient_name=patient.name, patient_dob=patient.dob
    # )
    # if db_patient is None:
    #     response = crud.create_patient(db=db, patient=patient)
    #     return schemas.PatientCreate(**response.dict())
    #
    # return HTTPException(
    #     status_code=405,
    #     detail="Patient already exists with same name and date of birth.",
    # )
    db_patient = crud.create_patient(db=db, patient=patient)
    return db_patient


@router.get("/", response_model=list[schemas.Patient])
async def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Read patient list."""
    patients = crud.get_patients(db, skip=skip, limit=limit)
    return patients


@router.get("/{patient_id}", response_model=schemas.Patient)
async def read_patient(patient_id: int, db: Session = Depends(get_db)):
    """Read a patient by id."""
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    return db_patient


@router.patch("/{patient_id}", response_model=schemas.Patient)
async def update_patient(
    patient_id: int,
    patient_updates: schemas.PatientUpdate,
    db: Session = Depends(get_db),
):
    """Update a patient by id."""
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    updated_patient = crud.update_patient(
        db, patient_id=patient_id, patient_updates=patient_updates
    )
    return updated_patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """Delete a patient by id."""
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        )
    crud.delete_patient(db, patient_id)
