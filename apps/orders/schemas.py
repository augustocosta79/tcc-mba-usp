from datetime import datetime
from typing import Optional, List
from uuid import UUID
from apps.users.schema import UserNestedSchema
from apps.addresses.schema import AddressNestedSchema
from apps.orders.enums import OrderStatus
from apps.products.schema import ProductNestedSchema

from pydantic import BaseModel

class OrderItemSchema(BaseModel):
    id: UUID
    product: ProductNestedSchema
    quantity: int
    price: int

class OrderSchema(BaseModel):
    id: UUID
    user: UserNestedSchema
    address: AddressNestedSchema
    items: List[OrderItemSchema]
    status: OrderStatus