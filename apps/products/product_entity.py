from uuid import UUID, uuid4
from decimal import Decimal
from typing import Optional
from datetime import datetime
from apps.shared.value_objects import Title, Description, Price, Stock

class Product:
    def __init__(
        self,
        title: Title,
        description: Description,
        price: Price,
        stock: Stock,
        owner_id: UUID,
        category: str,
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
        self._category = category
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
    def category(self) -> str:
        return self._category
    
    @property
    def is_active(self):
        return self._is_active
    
    @property
    def created_at(self):
        return self._created_at
    
    @property
    def updated_at(self):
        return self._updated_at
    

    def change_title(self, new_title: str):
        self._title = Title(new_title)
        return
    
    def change_description(self, new_description: str):
        self._description = Description(new_description)
        return
    
    def change_price(self, new_price: str):
        self._price = Price(new_price)
        return
    
    def change_stock(self, new_stock: int):
        self._stock = Stock(new_stock)
        return
    
    def change_category(self, new_category: str):
        self._category = new_category
        return
