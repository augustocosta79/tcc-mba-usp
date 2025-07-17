from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class CategorySchema(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime


class CategoryCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None