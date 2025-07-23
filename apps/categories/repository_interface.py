from abc import ABC, abstractmethod
from uuid import UUID

from apps.categories.entity import Category
from apps.categories.schema import CategoryUpdateSchema

class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def save(self, category: Category) -> Category:
        pass

    @abstractmethod
    def list_categories(self) -> list[Category]:
        pass

    @abstractmethod
    def get_category_by_id(self, category_id:UUID) -> Category:
        pass

    @abstractmethod
    def update_category(self, category: Category) ->  Category:
        pass

    @abstractmethod
    def delete_category(self, category_id: UUID) -> None:
        pass
    