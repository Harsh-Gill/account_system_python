from sqlalchemy.orm import Session

from . import models, schemas
from .helper import *


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    # query by email
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session):
    # Get all users
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserAccount):
    # hash password
    hashed_password = get_hashed_password(plain_text_password=user.password)

    # use User Class as model template
    db_user = models.User(
        email=user.email, name=user.name, hashed_password=hashed_password
    )
    # db operations
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(db: Session, user: schemas.UserLogin, verify=False):

    # get account by email
    acc = db.query(models.User).filter(models.User.email == user.email).first()

    # If account exists
    if acc:
        verify = verify_password(user.password, acc.hashed_password)

    # if password verified
    if verify:
        return "JWT"

    # Else not correct login details
    else:
        return
