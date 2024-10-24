from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="token") # tokenUrl is the path to get the token

class User(BaseModel):
    id: int
    username: str
    email: str
    disabled: bool


class UserInDB(User):
    password: str


users_db = {
    "user1": {
        "id": 1,
        "username": "user1",
        "email": "first_user@gmail.com",
        "disabled": False,
        "password": "1password1"
    },
    "user2": {
        "id": 2,
        "username": "user1",
        "email": "second_user@gmail.com",
        "disabled": True,
        "password": "2password2"
    },
    "user3": {
        "id": 3,
        "username": "user3",
        "email": "third_user@gmail.com",
        "disabled": False,
        "password": "3password3"
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


async def current_user(token: str = Depends(oauth2)):
    user = search_userDB(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},)
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user")

    user = User(**user.dict())

    return user


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = search_userDB(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    if form_data.password != user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    return {"access_token": user.username, "token_type": "bearer"}
    

@app.get("/users/me")
async def read_users_me(user: str = Depends(current_user)):
    return user