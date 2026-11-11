from fastapi import FastAPI, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status

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

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length= 100)
    priority: int = Field(gt=0, lt=6)
    completed: bool

@app.get("/", status_code = status.HTTP_200_OK)
async def read_all(db: db_injection):
    return db.query(Todos).all()

@app.get('/todos/{todo_id}', status_code = status.HTTP_200_OK)
async def read_todo(db: db_injection, todo_id: int = Path(gt=0) ):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo Not Found")

@app.post('/todos', status_code = status.HTTP_201_CREATED)
async def create_todo(db: db_injection, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.dict())
    db.add(todo_model)
    db.commit()