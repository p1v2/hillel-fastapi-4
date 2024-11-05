from fastapi import FastAPI, Response

from raw_sql.api import users_router as raw_sql_users_router
from sql_alchemy.api import users_router
from models.product import Product, ProductPartial
from models.user import User

app = FastAPI()
app.include_router(raw_sql_users_router)
app.include_router(users_router)


products = [
    Product(name="Coca-Cola", price=5),
    Product(name="Fanta", price=4),
]


@app.get("/products")
async def read_products():
    return products


@app.post("/products")
async def create_product(product: Product):
    products.append(product)
    return Response(product.json(), status_code=201)


@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    products[product_id] = product
    return product


@app.patch("/products/{product_id}")
async def partial_update_product(product_id: int, product_data: ProductPartial):
    existing_product = products[product_id]

    existing_product.name = product_data.name or existing_product.name
    existing_product.price = product_data.price or existing_product.price

    return existing_product


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    products.pop(product_id)
    return Response(status_code=204)


@app.post("/users")
async def create_user(user: User):
    return user
