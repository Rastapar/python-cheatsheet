from fastapi import FastAPI
from pydantic import BaseModel

my_app = FastAPI()

# BaseModel ayuda a crear una estructura de forma mas sencilla
class User(BaseModel):
    name: str
    surname: str
    web: str
    age: int

users = [
        User(name = "Tomas", surname = "Galapagos", web = "www.google.es", age = 20),
        User(name = "Juan", surname = "Francisco", web = "www.mozilla.es", age = 30),
        User(name = "Fanta", surname = "Naranja", web = "www.amazon.es", age = 40),
    ]

@my_app.get("/users")
async def _():
    return users

@my_app.get("/base-user")
async def _():
    return User(name = "Tato", surname = "Piña", web = "www.github.com", age = 50)