# main.py
from fastapi import FastAPI
from db import connect_to_db, close_db
from routes import reports, read, create, update, upload

app = FastAPI()

@app.on_event("startup")
async def startup():
    await connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

app.include_router(reports.router)
app.include_router(read.router)
app.include_router(create.router)
app.include_router(update.router)
app.include_router(upload.router)


