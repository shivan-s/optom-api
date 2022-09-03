"""Fixture for tests."""

import pytest
from faker import Faker
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth import get_current_user, get_password_hash
from app.main import app
from app.sql import models
from app.sql.database import SQLALCHEMY_DATABASE_URL, get_db


@pytest.fixture(scope="session")
def db_engine():
    """Engine for database."""
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, echo_pool="debug")
    yield engine


@pytest.fixture(scope="session")
def db(db_engine):
    """Database."""
    connection = db_engine.connect()
    connection.begin()
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    db = TestSessionLocal()
    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="session", autouse=True)
def faker():
    """Faker initialised."""
    return Faker()


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    """Set the locale for faker."""
    return ["en_NZ"]


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    """Random seed for faker generating information."""
    return 42


@pytest.fixture(scope="function")
def fake_user(faker):
    """Create fake user."""
    user = {
        "username": faker.user_name(),
        "full_name": faker.name(),
        "password": faker.password(),
    }
    return user


@pytest.fixture(scope="session")
def user_normal(faker, db):
    """Ordinary-level staff."""
    user = {
        "username": faker.user_name(),
        "full_name": faker.name(),
        "hashed_password": get_password_hash(faker.password()),
    }
    db_user = models.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@pytest.fixture(scope="session")
def user_admin(faker, db):
    """Admin-level staff."""
    user = {
        "username": faker.user_name(),
        "full_name": faker.name(),
        "hashed_password": get_password_hash(faker.password()),
        "is_admin": True,
    }
    db_user = models.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@pytest.fixture(scope="session")
def user_optom(faker, db):
    """Optometry-level staff."""
    user = {
        "username": faker.user_name(),
        "full_name": faker.name(),
        "hashed_password": get_password_hash(faker.password()),
    }
    db_user = models.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    registration = faker.ean8()  # similar to registration numbers
    db_optometrist = models.Optometrist(registration=registration, users_id=db_user.id)
    db.add(db_optometrist)
    db.commit()
    db.refresh(db_optometrist)
    return db_optometrist


@pytest.fixture(scope="session")
def user_dispenser(faker, db):
    """Dispenser-level staff."""
    user = {
        "username": faker.user_name(),
        "full_name": faker.name(),
        "hashed_password": get_password_hash(faker.password()),
    }
    db_user = models.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    registration = faker.ean8()  # similar to regristration numbers
    db_dispenser = models.Dispenser(registration=registration, users_id=db_user.id)
    db.add(db_dispenser)
    db.commit()
    db.refresh(db_dispenser)
    return db_dispenser


@pytest.fixture(scope="function")
def anon_client(db):
    """Client."""
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def client(db, user_normal):
    """Client."""
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: user_normal
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def admin_client(db, user_admin):
    """Admin client."""
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: user_admin
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def fake_patient(faker):
    """Fake patient."""
    patient = {
        "name": faker.name(),
        "dob": faker.date_of_birth(),
        "address": faker.address(),
        "phonenumber_1": faker.phone_number(),
        "email": faker.email(),
    }
    return jsonable_encoder(patient)


@pytest.fixture(scope="function")
def mock_patient(faker, db):
    """Mock patient."""
    patient = {
        "name": faker.name(),
        "dob": faker.date_of_birth(),
        "address": faker.address(),
        "phonenumber_1": faker.phone_number(),
        "email": faker.email(),
    }
    db_patient = models.Patient(**patient)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@pytest.fixture(scope="function")
def patient_update(faker) -> dict[str, str]:
    """Update patient."""
    patient = {
        "name": faker.name(),
        "dob": faker.date_of_birth(),
    }
    return jsonable_encoder(patient)


@pytest.fixture(scope="function")
def mock_user(fake_user, db):
    """Mock user."""
    fake_user["hashed_password"] = get_password_hash(fake_user["password"])
    fake_user.pop("password")
    db_user = models.User(**fake_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@pytest.fixture(scope="function")
def user_update(faker) -> dict[str, str]:
    """Update user."""
    user = {
        "username": faker.user_name(),
        "full_name": faker.name(),
    }
    return jsonable_encoder(user)
