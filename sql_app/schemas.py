from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserAccount(UserBase):
    password: str


class User(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str
