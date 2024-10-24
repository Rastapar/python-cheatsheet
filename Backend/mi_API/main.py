from fastapi import FastAPI
from routers import users, products
from fastapi.staticfiles import StaticFiles

# "/docs" path for swagger-ui documentation
# "/redoc" path for redoc (based on swagger-ui) documentation 

my_app = FastAPI()

my_app.include_router(users.router)
my_app.include_router(products.router)
# to show static files (like images)
# 'address'/static/images/image.png
my_app.mount("/static", StaticFiles(directory="static"), name="static")


@my_app.get("/")
async def root():
    return "Hello API"


@my_app.get("/url")
async def return_some_url():
    return { "mi_url": "www.google.es" }


