from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    name = Column(String)
    email = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)


def ResponseModel(message):
    return {
        "success": True,
        "message": message,
        "code": 200,
    }


def LoginResponseModel(token, message):
    return {
        "success": True,
        "token": token,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
