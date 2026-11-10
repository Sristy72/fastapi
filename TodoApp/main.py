from fastapi import FastAPI, Depends
import models
from models import Todos
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from typing import Annotated

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_injection = Annotated[Session, Depends(get_db)]
@app.get("/")
async def read_all(db: db_injection):
    return db.query(Todos).all()