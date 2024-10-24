from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel

router = APIRouter()

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


@router.delete("/user/{id}")
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
@router.put("/user/")
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
@router.post("/user/", response_model=User, status_code=201) # status_code=201 para indicar que se ha creado un recurso
async def _(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="User already exists")    # send custom status code        
    
    users.append(user)
    return user # defined the typo in response_model


# query para los parametros opcionales
@router.get("/user-query/")  # the same as "/user-query/{id}" but with query parameters
async def _(id: int):
    return search_user(id)


# path para los parametros obligatorios
@router.get("/user/{id}")
async def _(id: int):
    return search_user(id)


@router.get("/users")
async def _():
    return users


@router.get("/base-user")
async def _():
    return User(name = "Tato", surname = "Piña", web = "www.github.com", age = 50)


def search_user(id: int):
    users_byid = list( filter(lambda user: user.id == id, users) )
    return users_byid[0] if users_byid else {"error": "User not found"}
