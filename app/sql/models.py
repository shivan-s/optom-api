"""Models."""
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UnicodeText,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    """Users to access the database.

    the Optometrist or Dispenser model.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    optometrists = relationship("Optometrist", back_populates="users", uselist=False)
    dispensers = relationship("Dispenser", back_populates="users", uselist=False)
    specdispenses = relationship("SpecDispense", back_populates="users")


class Dispenser(Base):
    """Dispenser model.

    Dispenser share a one-to-one relationship with the User model.

    Dispensers perform spectacle dispenses.
    """

    __tablename__ = "dispensers"

    id = Column(Integer, primary_key=True, index=True)
    users_id = Column(Integer, ForeignKey("users.id"))
    registration = Column(String, unique=True)
    is_active = Column(Boolean, default=True)

    users = relationship("User", back_populates="dispensers")


class Optometrist(Base):
    """Optometrist model.

    Optometrists share a one-to-one relationship with the User model.

    Optometrist perform eye examination and come up with spectacle
    prescription.
    """

    __tablename__ = "optometrists"

    id = Column(Integer, primary_key=True, index=True)
    users_id = Column(Integer, ForeignKey("users.id"))
    registration = Column(String, unique=True)
    is_active = Column(Boolean, default=True)

    users = relationship("User", back_populates="optometrists")
    exams = relationship("Exam", back_populates="optometrists")
    specprescriptions = relationship("SpecPrescription", back_populates="optometrists")
    specdispenses = relationship("SpecDispense", back_populates="optometrists")


class Patient(Base):
    """Patient model."""

    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    address = Column(String, default=None)
    phonenumber_1 = Column(String, default=None)
    phonenumber_2 = Column(String, default=None)
    phonenumber_3 = Column(String, default=None)
    email = Column(String, default=None)

    exams = relationship("Exam", back_populates="patients")
    specprescriptions = relationship("SpecPrescription", back_populates="patients")
    specdispenses = relationship("SpecDispense", back_populates="patients")


class Exam(Base):
    """Exam model."""

    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    patients_id = Column(Integer, ForeignKey("patients.id"))
    optometrists_id = Column(Integer, ForeignKey("optometrists.id"))
    date_created = Column(DateTime, server_default=func.now())
    date_updated = Column(DateTime, onupdate=func.now())
    history = Column(UnicodeText)
    health = Column(UnicodeText)

    patients = relationship("Patient", back_populates="exams")
    optometrists = relationship("Optometrist", back_populates="exams")
    specprescriptions = relationship("SpecPrescription", back_populates="exams")


class SpecPrescription(Base):
    """Spectacle Prescription model."""

    __tablename__ = "specprescriptions"

    id = Column(Integer, primary_key=True, index=True)
    exams_id = Column(Integer, ForeignKey("exams.id"))
    patients_id = Column(Integer, ForeignKey("patients.id"))
    optometrists_id = Column(Integer, ForeignKey("optometrists.id"))
    right_sphere = Column(Numeric)
    right_cylinder = Column(Numeric)
    right_axis = Column(Numeric)
    right_add = Column(Numeric)
    right_inter_add = Column(Numeric)
    left_sphere = Column(Numeric)
    left_cylinder = Column(Numeric)
    left_axis = Column(Numeric)
    left_add = Column(Numeric)
    left_inter_add = Column(Numeric)

    exams = relationship("Exam", back_populates="specprescriptions")
    patients = relationship("Patient", back_populates="specprescriptions")
    optometrists = relationship("Optometrist", back_populates="specprescriptions")
    specdispenses = relationship(
        "SpecDispense",
        back_populates="specprescriptions",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class SpecDispense(Base):
    """Spectacle Dispense model."""

    __tablename__ = "specdispenses"

    id = Column(Integer, primary_key=True, index=True)
    patients_id = Column(Integer, ForeignKey("patients.id"))
    specprescriptions_id = Column(
        Integer, ForeignKey("specprescriptions.id", ondelete="CASCADE")
    )
    users_id = Column(Integer, ForeignKey("users.id"))
    optometrists_id = Column(Integer, ForeignKey("optometrists.id"))
    frame = Column(String)

    patients = relationship("Patient", back_populates="specdispenses")
    specprescriptions = relationship(
        "SpecPrescription",
        back_populates="specdispenses",
    )
    users = relationship("User", back_populates="specdispenses")
    optometrists = relationship("Optometrist", back_populates="specdispenses")


# class CLPrescription(Base):
#     __tablename__ = "clprescriptions"
