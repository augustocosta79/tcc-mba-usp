from abc import ABC, abstractmethod
from uuid import UUID

class ProductRepositoryInterface(ABC):
    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def get_product_by_id(self):
        pass

    @abstractmethod
    def list_products_by_category(self):
        pass

    @abstractmethod
    def update_product(self):
        pass

    @abstractmethod
    def delete_product(self):
        pass

    @abstractmethod
    def get_product_for_update(self, product_id: UUID):
        pass