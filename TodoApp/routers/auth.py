from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import User
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

router = APIRouter()
SECRET_KEY = 'ff4308206edc053ef901ae0e38e81ea11c7d1479665ae78cc69065c90f05bef9'
ALGORITHM = 'HS256'

bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bycrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username:str, user_id:int, expires_delta:timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


class CreateUserRequest(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.firstName,
        last_name = create_user_request.lastName,
        hashed_password = bycrypt_context.hash(create_user_request.password),
        role = create_user_request.role
    )
    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db : db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed Authentication'

    token = create_access_token(
        user.username, user.id, expires_delta=timedelta(minutes=20)
    )
    return {'access_token': token, 'token_type': 'bearer'}

