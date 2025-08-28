from datetime import datetime
from typing import Optional, List
from uuid import UUID
from apps.users.schema import UserNestedSchema
from apps.addresses.schema import AddressSchema
from apps.orders.enums import OrderStatus
from apps.products.schema import ProductNestedSchema

from pydantic import BaseModel

class OrderItemSchema(BaseModel):
    id: UUID
    product: ProductNestedSchema
    quantity: int
    price: str

class OrderSchema(BaseModel):
    id: UUID
    user: UserNestedSchema
    address: AddressSchema
    items: List[OrderItemSchema]
    status: OrderStatus

class OrderCreateSchema(BaseModel):
    address_id: UUID

class OrderStatusChangeSchema(BaseModel):
    new_status: OrderStatus