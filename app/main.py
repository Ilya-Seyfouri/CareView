from fastapi import FastAPI
from fastapi.routing import APIRoute

from routes.managers import manager_router
from routes.family import family_router
from routes.carers import carer_router
from routes.patients import patient_router


app = FastAPI()

app.include_router(manager_router)
app.include_router(family_router)
app.include_router(patient_router)
app.include_router(carer_router)


@app.get("/")
async def root():
    return {"Health": "Check"}
