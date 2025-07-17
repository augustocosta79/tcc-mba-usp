from abc import ABC, abstractmethod

from apps.categories.entity import Category


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def save(self, category: Category) -> Category:
        pass

    @abstractmethod
    def list_categories(self) -> list[Category]:
        pass
