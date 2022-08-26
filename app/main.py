"""Root file."""

import logging

from fastapi import Depends, FastAPI

from app import schemas
from app.auth import get_current_user
from app.routers import auth, patients, users

logging.basicConfig(level=logging.DEBUG, filename="debug.log")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome! OptomAPI"}


@app.get("/me")
async def read_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


# routes
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(users.router)
