from apps.products.repository_interface import ProductRepositoryInterface
from apps.products.product_entity import Product
from apps.shared.value_objects import Title, Description, Price, Stock
from apps.shared.exceptions import NotFoundError
from uuid import UUID

class ProductService:
    def __init__(self, repository:ProductRepositoryInterface):
        self.repository = repository

    def create_product(
            self,
            title: Title,
            description: Description,
            price: Price,
            stock: Stock,
            owner_id: UUID
    ) -> Product:
        
        product = Product(
            title,
            description,
            price,
            stock,
            owner_id
        )

        saved_product = self.repository.save(product)

        return saved_product
    
    def get_product_by_id(self, product_id) -> Product:
        if not (product:=self.repository.get_product_by_id(product_id)):
            raise NotFoundError(f"Product with id {product_id} not found")
        return product