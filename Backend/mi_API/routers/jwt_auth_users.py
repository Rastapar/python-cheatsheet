from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
# SECRET KEY generated with openssl rand -hex 32
SECRET = "a8fcf7bcbda63d58d64a8dba3ab8b5a92358393aac3d660184f7605e4cd0afa7"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="token") # tokenUrl is the path to get the token

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    id: int
    username: str
    email: str
    disabled: bool


class UserInDB(User):
    password: str


# password encrypted with bcrypt
users_db = {
    "user1": {
        "id": 1,
        "username": "user1",
        "email": "first_user@gmail.com",
        "disabled": False,
        "password": "$2a$12$Dw4EfhJZrwpRTG2O12VGeOmh.6Sp.5D4IhZM0Dlb8FlR5F7y9gPQC"
    },
    "user2": {
        "id": 2,
        "username": "user2",
        "email": "second_user@gmail.com",
        "disabled": True,
        "password": "$2a$12$euuSXzwnLO.ryqo5fACcLud3RWVlsLyimaG0X7txo5vg8PQKqsqPe"
    },
    "user3": {
        "id": 3,
        "username": "user3",
        "email": "third_user@gmail.com",
        "disabled": False,
        "password": "$2a$12$fNqIlF1vf..XXcP9jK3CwevvunosR.dCEqK6RuZ/R8EvweZI3ugI6"
    }
}


def search_userDB(user_key: str):
    if user_key in users_db:
        return UserInDB(**users_db[user_key])
    return None


def search_user(user_key: str):
    if user_key in users_db:
        return User(**users_db[user_key])
    return None


async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},)

    try:
        user = jwt.decode(token, key=SECRET, algorithms=[ALGORITHM])
        username = user.get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    return search_user(username)


async def current_user(user: str = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user")

    user = User(**user.model_dump())

    return user


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = search_userDB(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")

    if not crypt.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    # token expiration
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = {
        "sub": user.username,
        "exp": expire
    }

    return {
        "access_token": jwt.encode(access_token, key=SECRET, algorithm=ALGORITHM), 
        "token_type": "bearer",
        }
    

@router.get("/users/me")
async def read_users_me(user: str = Depends(current_user)):
    return user