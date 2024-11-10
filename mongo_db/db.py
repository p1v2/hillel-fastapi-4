import motor.motor_asyncio
from bson import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient("localhost", 27017)

db = client["db"]

products_collection = db["products"]


async def fetch_all_products():
    products = []
    async for product in products_collection.find():
        products.append(product)

    return products


async def create_product_in_db(product):
   return await products_collection.insert_one(product)


async def update_product_in_db(product_id, product):
    return await products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": product})


def delete_product_in_db(product_id):
    return products_collection.delete_one({"_id": ObjectId(product_id)})


async def fetch_product_by_id(product_id):
    return await products_collection.find_one({"_id": ObjectId(product_id)})
