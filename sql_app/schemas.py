from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    hashed_password: str
    id: int

    class Config:
        orm_mode = True
