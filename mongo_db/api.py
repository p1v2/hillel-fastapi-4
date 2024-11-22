from fastapi import APIRouter, HTTPException, Response

from mongo_db.db import fetch_all_products, create_product_in_db, fetch_product_by_id, update_product_in_db, \
    delete_product_in_db, fetch_discounted_products, fetch_products_report
from mongo_db.serializers import serialize_mongo_data

products_router = APIRouter(prefix="/v2/products")


@products_router.get("/")
async def get_products():
    products = await fetch_all_products()

    return [serialize_mongo_data(product) for product in products]


@products_router.post("/")
async def create_product(product: dict):
    result = await create_product_in_db(product)

    product = await fetch_product_by_id(result.inserted_id)

    return serialize_mongo_data(product)


@products_router.get("/discounted")
async def get_discounted_products():
    products = await fetch_discounted_products()

    return [serialize_mongo_data(product) for product in products]


@products_router.get("/report")
async def report():
    return await fetch_products_report()


@products_router.get("/{product_id}")
async def get_product(product_id: str):
    product = await fetch_product_by_id(product_id)

    if product is None:
        raise HTTPException(status_code=404)

    return serialize_mongo_data(product)


@products_router.put("/{product_id}")
async def update_product(product_id: str, product: dict):
    product = await fetch_product_by_id(product_id)

    if product is None:
        raise HTTPException(status_code=404)

    await update_product_in_db(product_id, product)

    new_product = await fetch_product_by_id(product_id)

    return serialize_mongo_data(new_product)


@products_router.delete("/{product_id}")
async def delete_product(product_id: str):
    product = await fetch_product_by_id(product_id)

    if product is None:
        raise HTTPException(status_code=404)

    await delete_product_in_db(product_id)

    return Response(status_code=204)
