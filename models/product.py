from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float


class ProductPartial(BaseModel):
    name: str = None
    price: float = None
