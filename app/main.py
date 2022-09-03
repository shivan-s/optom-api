"""Root file."""

import logging

from fastapi import FastAPI

from app.routers import auth, dashboard, patients, users

logging.basicConfig(level=logging.DEBUG, filename="debug.log")

app = FastAPI()


@app.get("/")
async def root():
    """Root."""
    return {"message": "Welcome! OptomAPI"}


# routes
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(users.router)
app.include_router(dashboard.router)
