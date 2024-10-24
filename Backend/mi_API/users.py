from fastapi import FastAPI
from pydantic import BaseModel

my_app = FastAPI()

# BaseModel ayuda a crear una estructura de forma mas sencilla
class User(BaseModel):
    id: int
    name: str
    surname: str
    web: str
    age: int

users = [
        User(id = 1, name = "Tomas", surname = "Galapagos", web = "www.google.es", age = 20),
        User(id = 2, name = "Juan", surname = "Francisco", web = "www.mozilla.es", age = 30),
        User(id = 3, name = "Fanta", surname = "Naranja", web = "www.amazon.es", age = 40),
    ]

@my_app.delete("/user/{id}")
async def _(id: int):
    found : bool = False
    for index, user in enumerate(users):
        if user.id == id:
            found = True
            del users[index]
    
    if not found:
        return {"error": "User doesn't exists"}
    
    return {"message": "User deleted"}

# "put" para actualizar usuarios enteros
# "patch" para actualizar usuarios parcialmente
@my_app.put("/user/")
async def _(user: User):
    found : bool = False
    for index, saved_user in enumerate(users):
        if saved_user.id == user.id:
            found = True
            users[index] = user
    
    if not found:
        return {"error": "User doesn't exists"}
    
    return {"message": "User updated"}

# "post" para crear un usuario
@my_app.post("/user/")
async def _(user: User):
    if type(search_user(user.id)) == User:
        return {"error": "User already exists"}
    users.append(user)
    return {"message": "User created"}

# query para los parametros opcionales
@my_app.get("/user-query/")  # the same as "/user-query/{id}" but with query parameters
async def _(id: int):
    return search_user(id)

# path para los parametros obligatorios
@my_app.get("/user/{id}")
async def _(id: int):
    return search_user(id)

@my_app.get("/users")
async def _():
    return users

@my_app.get("/base-user")
async def _():
    return User(name = "Tato", surname = "Piña", web = "www.github.com", age = 50)

def search_user(id: int):
    users_byid = list( filter(lambda user: user.id == id, users) )
    return users_byid[0] if users_byid else {"error": "User not found"}
