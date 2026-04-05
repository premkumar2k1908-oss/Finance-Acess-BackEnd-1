from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import Role, Status

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Role = Role.VIEWER

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role
    status: Status

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"