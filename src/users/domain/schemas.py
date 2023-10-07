import hashlib

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
