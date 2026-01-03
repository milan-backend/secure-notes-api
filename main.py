from fastapi import FastAPI
from database import create_db_and_tables
from routers import auth,notes


app = FastAPI()

@app.on_event("startup")
def on_event():
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(notes.router)