from uuid import UUID, uuid4
from decimal import Decimal
from typing import Optional
from datetime import datetime

class Product:
    def __init__(
        self,
        title: str,
        description: str,
        price: Decimal,
        stock: int,
        owner_id: UUID,
        id: Optional[UUID] = None,
        is_active: Optional[bool] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._id = id or uuid4()
        self._title = title
        self._description = description
        self._price = price
        self._stock = stock
        self._owner_id = owner_id
        self._is_active = is_active if is_active is not None else True
        self._created_at = created_at
        self._updated_at = updated_at

    @property
    def id(self):
        return self._id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def price(self) -> Decimal:
        return self._price
    
    @property
    def stock(self) -> int:
        return self._stock
    
    @property
    def owner_id(self) -> UUID:
        return self._owner_id
    
    @property
    def is_active(self):
        return self._is_active
    
    @property
    def created_at(self):
        return self._created_at
    
    @property
    def updated_at(self):
        return self._updated_at
