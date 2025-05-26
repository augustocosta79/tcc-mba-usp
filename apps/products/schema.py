from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from decimal import Decimal

class ProductSchema(BaseModel):
    id: UUID
    title: str
    description: str
    price: str
    stock: int
    owner_id: UUID
    created_at: datetime
    updated_at: datetime



class ProductCreateSchema(BaseModel):
    title: str
    description: str
    price: Decimal
    stock: int
    owner_id: UUID
