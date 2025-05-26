from abc import ABC, abstractmethod

class ProductRepositoryInterface(ABC):
    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def get_product_by_id(self):
        pass