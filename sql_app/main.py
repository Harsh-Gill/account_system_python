from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from .auth.auth_bearer import JWTBearer
from .auth.auth_handler import signJWT, decodeJWT


from decouple import config

# Getting superuser
super_user = config("super_user_email")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to run and yield DB
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

    if user["user_id"] == config("super_user_email"):
        return True, user["user_id"]
    else:
        return False, user["user_id"]


@app.on_event("startup")
def startup():
    db = next(get_db())
    # init default super user
    try:
        super_user_init = crud.create_super_user(db)
        print("Super User Intialized")
    except:
        print("Super User exists")


# Create User account
@app.post("/users/", response_description="Creating Account")
def create_user(user: schemas.UserAccount, db: Session = Depends(get_db)):
    """
    Create an account with the information:

    - **name**: Your name associated with the account
    - **email**: Your email for the account
    - **password**: Create a safe password!
    """

    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    new_user = crud.create_user(db=db, user=user)
    return models.ResponseModel("User Account Created")


# Get User information
@app.get(
    "/users/",
    dependencies=[Depends(JWTBearer())],
    response_description="Getting User(s) info",
)
def read_users(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    This API call lets you get user information on the SQL Database.

    - **Requires Authentication with Token **

    - Functionality : **If you are a Super User it returns all users information. Otherwise, it only returns your own user infornation.**
    """

    # Get role of user by decoding JWT Token ; define response based on conditional
    is_super_user, curr_user = get_current_user_role(request)

    if is_super_user:
        users = crud.get_users(db)
    else:
        users = crud.get_user_by_email(db, curr_user)

    return models.ResponseModel(users)


# Login
@app.put("/users/", response_description="Processing Login")
def login_(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Please login with your Credentials:

    - **email**: Your email for the account
    - **password**: The assosciated Password
    """
    users = crud.login_user(db, user)

    if users:
        token = signJWT(user.email)
        return models.LoginResponseModel(token["access_token"], "Log in Successful")

    else:
        return models.ErrorResponseModel("", 101, "Wrong Login Details")
