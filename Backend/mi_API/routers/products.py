from fastapi import APIRouter

router = APIRouter(prefix="/products",  # prefix for all paths
                   tags=["products"],   # header for documentation
                   responses={404: {"description": "Not found"}})


products = [
    {"id": 1, "name": "product1", "price": 100},
    {"id": 2, "name": "product2", "price": 200},
    {"id": 3, "name": "product3", "price": 300},
]


@router.get("/", tags=["get all products"])
async def get_products():
    return {"products": products}


@router.get("/{product_id}", tags=["get a product by id"])
async def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return {"error": "Product not found"}