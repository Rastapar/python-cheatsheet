from fastapi import FastAPI, HTTPException, APIRouter, status
from pydantic import BaseModel
from mongodb.models.user import User
from mongodb.client import db_client
from mongodb.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/db-user", tags=["db-user"])


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def _(id: str):
    found = db_client.local.users.delete_one({"_id": ObjectId(id)})
    
    if not found:
        return {"error": "User NOT found"}


# "put" para actualizar usuarios enteros
# "patch" para actualizar usuarios parcialmente
@router.put("/", status_code=status.HTTP_202_ACCEPTED)
async def _(user: User):
    try:
        user_dict = dict(user)
        del user_dict["id"]

        found = db_client.local.users.find_one_and_replace(
            {"_id": ObjectId(user.id)},
            user_dict,
        )

        if not found:
            return {"error": "User NOT found"}
        
    except:
        return {"error": "User doesn't exists"}
    
    return search_user("_id", ObjectId(user.id))


# "post" para crear un usuario
@router.post("/", response_model=User, status_code=201) # status_code=201 para indicar que se ha creado un recurso
async def _(user: User):
    if type( search_user("name", user.name) ) == User:
        raise HTTPException(status_code=404, detail="User already exists")    # send custom status code        
    
    #users.append(user)
    user_dict = dict(user)
    del user_dict["id"]

    print(user_dict)

    id = db_client.local.users.insert_one(user_dict).inserted_id
    
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))

    return User(**new_user)


# query para los parametros opcionales
@router.get("-query/")  # the same as "/user-query/{id}" but with query parameters
async def _(name: str = None):
    return search_user("name", name)


# path para los parametros obligatorios
# @router.get("/{name}")
# async def _(name: str):
#     return search_user("name", name)

@router.get("/{id}")
async def _(id: str):
    return search_user("_id", ObjectId(id))

@router.get("s", response_model=list[User])
async def _():
    return list( users_schema(db_client.local.users.find()) )


@router.get("/base-user")
async def _():
    return User(name = "Tato", surname = "Piña", web = "www.github.com", age = 50)


def search_user(key: str, value):
    try:
        user_dict = user_schema( db_client.local.users.find_one({key: value}) )
        return User(**user_dict)
    except:
        return {"error": "User not found"}
