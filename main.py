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

users = [
    User(id=1, first_name='Maksim', last_name='Buzovskiy', phone_number='+380123456789', 
     email='maksim.buzovskiy@official.com', password='540876545676543'), 
    User(id=2, first_name='Olga', last_name='Ivanova', phone_number='0931234567', 
         email='olga.ivanova@official.com', password='hgfGHIUOIYUTryet8765456'), 
    User(id=3, first_name='Andriy', last_name='Shevchenko', phone_number='+380931234567',
        email='andriy.shevchenko@official.com', password='fguhiu545678765'), 
    User(id=4, first_name='Natalia', last_name='Petrova', phone_number='0977654321', 
         email='natalia.petrova@official.com', password='654567JHGFDFGHJKjhgfdsdf')]


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

@app.delete("/users/{id}") 
async def delete_user(id: int): 
    if id in users: 
        del users[id] 
        return {"message": "User deleted successfully"} 
    else: 
        return Response(status_code=404)
