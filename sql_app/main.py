from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from .auth.auth_bearer import JWTBearer
from .auth.auth_handler import signJWT, decodeJWT

from decouple import config

# Getting superuser
super_user = config("super_user")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to run DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get current user role and primary id
def get_current_user_role(request):
    token = request.headers["authorization"][7:]
    user = decodeJWT(token)
    if user["user_id"] == config("super_user"):
        return True, user["user_id"]
    else:
        return False, user["user_id"]


# Create User account
@app.post("/users/", response_description="Creating Account")
def create_user(user: schemas.UserAccount, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    return crud.create_user(db=db, user=user)


@app.get(
    "/users/",
    dependencies=[Depends(JWTBearer())],
    response_description="Getting User(s) info",
)
def read_users(
    request: Request,
    db: Session = Depends(get_db),
):

    is_super_user, curr_user = get_current_user_role(request)

    if is_super_user:
        users = crud.get_users(db)
    else:
        users = crud.get_user_by_email(db, curr_user)

    return models.ResponseModel(users, "User(s) Info Feteched Successfully")


@app.put("/users/", response_description="Processing Login")
def login_(user: schemas.UserLogin, db: Session = Depends(get_db)):
    users = crud.login_user(db, user)

    if users:
        token = signJWT(user.email)
        return models.ResponseModel(token, "Log in Successful")

    else:
        return models.ErrorResponseModel("", 101, "Wrong Login Details")
