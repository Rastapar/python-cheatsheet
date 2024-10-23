from fastapi import FastAPI

my_app = FastAPI()

# "/docs" path for swagger-ui documentation
# "/redoc" path for redoc (based on swagger-ui) documentation 

@my_app.get("/")
async def root():
    return "Hello API"

@my_app.get("/url")
async def return_some_url():
    return { "mi_url": "www.google.es" }
