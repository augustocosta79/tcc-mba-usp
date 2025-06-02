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
    category: str
    is_active: bool
    created_at: datetime
    updated_at: datetime



class ProductCreateSchema(BaseModel):
    title: str
    description: str
    price: str
    stock: int
    owner_id: UUID
    category: str


class ProductUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[str] = None
    stock: Optional[int] = None
    owner_id: Optional[UUID] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None