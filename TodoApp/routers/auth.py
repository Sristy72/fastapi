from fastapi import APIRouter
from pydantic import BaseModel
from passlib.context import CryptContext
from models import User

router = APIRouter()

bycrypt_context = CryptContext()

class CreateUserRequest(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
    password: str
    role: str

@router.post("/auth/")
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = User(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.firstName,
        last_name = create_user_request.lastName,
        hashed_password = create_user_request.password,
        role = create_user_request.role
    )
    return create_user_model