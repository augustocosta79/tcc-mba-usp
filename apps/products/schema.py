from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel

from apps.categories.schema import CategoryNestedSchema

class ProductSchema(BaseModel):
    id: UUID
    title: str
    description: str
    price: str
    stock: int
    owner_id: UUID
    categories: list[CategoryNestedSchema]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ProductNestedSchema(BaseModel):
    id: UUID
    title: str
    description: str
    price: str
    stock: int
    owner_id: UUID
    categories: list[CategoryNestedSchema]



class ProductCreateSchema(BaseModel):
    title: str
    description: str
    price: str
    stock: int
    owner_id: UUID
    categories: list[UUID]


class ProductUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[str] = None
    stock: Optional[int] = None
    owner_id: Optional[UUID] = None
    categories: Optional[list[UUID]] = None
    is_active: Optional[bool] = None

class ProductActivationSchema(BaseModel):
    status: bool