from fastapi import FastAPI, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status
from routers import auth, todos
import models
from models import Todos
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from typing import Annotated

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)

