from uuid import UUID, uuid4
from apps.shared.value_objects import Name, Description
from datetime import datetime
from typing import Optional


class Category:
    def __init__(
        self,
        name: Name,
        description: Description,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._name = name
        self._description = description
        self._id = id or uuid4()
        self._created_at = created_at
        self._updated_at = updated_at

    @property
    def name(self) -> Name:
        return self._name

    @property
    def description(self) -> Description:
        return self._description
    
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def rename(self, new_name: str) -> None:
        name = Name(new_name)
        self._name = name
        return
    
    def update_description(self, new_description: str) -> None:
        description = Description(new_description)
        self._description = description
        return
