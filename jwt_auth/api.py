from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from jwt_auth.jwt import create_access_token, verify_token

auth_router = APIRouter(prefix="/auth")


fake_users_db = [
   {"username": "user", "password": "password", "role": "admin"}
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class LoginData(BaseModel):
    username: str
    password: str


@auth_router.post("/token")
async def login(form_data: LoginData):
    username = form_data.username

    user = next((user for user in fake_users_db if user["username"] == username), None)

    if user is None:
        raise HTTPException(status_code=401)

    if user["password"] != form_data.password:
        raise HTTPException(status_code=401)

    # Generate token
    access_token_expires = timedelta(minutes=20)

    access_token = create_access_token(data={"sub": username, "role": user["role"]}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401)

    username = payload.get("sub")

    return {"username": username}

