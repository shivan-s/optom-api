"""Database."""
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
SERVER = os.getenv("POSTGRES_SERVER")
DB = os.getenv("POSTGRES_DB")
PORT = 5432

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Connect with database."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
