from uuid import UUID
from pydantic import BaseModel, conint
from apps.products.schema import ProductSchema
from typing import List

class AddToCartSchema(BaseModel):
    product_id: UUID
    quantity: conint(gt=0)

class SubtractCartItemQuantitySchema(AddToCartSchema):
    pass

class CartItemSchema(BaseModel):
    id: UUID
    product: ProductSchema
    quantity: int


class CartSchema(BaseModel):
    id: UUID
    user_id: UUID
    items: List[CartItemSchema]
