from apps.products.repository_interface import ProductRepositoryInterface
from apps.products.product_entity import Product
from apps.products.schema import ProductUpdateSchema, ProductActivationSchema
from apps.shared.value_objects import Title, Description, Price, Stock
from apps.shared.exceptions import NotFoundError
from uuid import UUID

class ProductService:
    def __init__(self, repository:ProductRepositoryInterface):
        self.repository = repository

    def create_product(
            self,
            title: str,
            description: str,
            price: str,
            stock: int,
            owner_id: UUID,
            category: str
    ) -> Product:
        
        title = Title(title)
        description = Description(description)
        price = Price(price)
        stock = Stock(stock)
        owner_id = owner_id
        category = category
        
        product = Product(
            title,
            description,
            price,
            stock,
            owner_id,
            category
        )

        saved_product = self.repository.save(product)

        return saved_product
    
    def get_product_by_id(self, product_id) -> Product:
        if not (product:=self.repository.get_product_by_id(product_id)):
            raise NotFoundError(f"Product with id {product_id} not found")
        return product
    
    def list_products_by_category(self, category: str) -> list[Product]:
        return self.repository.list_products_by_category(category)
    
    def update_product(self, product_id: UUID, payload: ProductUpdateSchema) -> Product:        
        if not (product := self.repository.get_product_by_id(product_id)):
            raise NotFoundError(f"Product with id {product_id} not found")
        
        operations = {
            "title": product.change_title,
            "description": product.change_description,
            "price": product.change_price,
            "stock": product.change_stock,
            "category": product.change_category
        }
        
        for attr, value in payload.model_dump(exclude_none=True).items():
            operations[attr](value)

        updated_product = self.repository.update_product(product)

        return updated_product
    
    def product_activation(self, product_id: UUID, payload: ProductActivationSchema):
        product = self.repository.get_product_by_id(product_id)

        if not product:
            raise NotFoundError(f"Product with id {product_id} not found")
        
        if payload.status is True:
            product.activate()
        else:
            product.deactivate()

        return self.repository.update_product(product)