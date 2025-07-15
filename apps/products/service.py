import logging
from uuid import UUID

from apps.products.product_entity import Product
from apps.products.repository_interface import ProductRepositoryInterface
from apps.products.schema import ProductActivationSchema, ProductUpdateSchema
from apps.shared.exceptions import NotFoundError
from apps.shared.value_objects import Description, Price, Stock, Title


class ProductService:
    def __init__(self, repository:ProductRepositoryInterface, logger: logging.Logger):
        self.repository = repository
        self.logger = logger

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
        self.logger.info(f"Product successfully created: id {saved_product.id} - name {saved_product.title}")
        return saved_product
    
    def get_product_by_id(self, product_id) -> Product:
        if not (product:=self.repository.get_product_by_id(product_id)):
            raise NotFoundError(f"Product with id {product_id} not found")
        return product
    
    def list_products_by_category(self, category: str) -> list[Product]:
        return self.repository.list_products_by_category(category)
    
    def update_product(self, product_id: UUID, payload: ProductUpdateSchema) -> Product:        
        if not (product := self.repository.get_product_by_id(product_id)):
            self.logger.warning(f"Can't update Product with id {product_id}. Product not found")
            raise NotFoundError(f"Can't update Product with id {product_id}. Product not found")
        
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
        self.logger.info(f"Product successfully updated: id {updated_product.id} - name {updated_product.title}")
        return updated_product
    
    def product_activation(self, product_id: UUID, payload: ProductActivationSchema) -> Product:
        product = self.repository.get_product_by_id(product_id)

        if not product:
            self.logger.warning(f"Product not found. ID: {product_id}")
            raise NotFoundError(f"Product with id {product_id} not found")
        
        if payload.status is True:
            self.logger.info(f"Product id {product.id} activated successfully")
            product.activate()
        else:
            self.logger.info(f"Product id {product.id} deactivated successfully")
            product.deactivate()

        return self.repository.update_product(product)
    
    def delete_product(self, product_id: UUID) -> None:
        if not (product:=self.repository.get_product_by_id(product_id)):
            self.logger.warning(f"Not found Product - ID {product_id}")
            raise NotFoundError(f"Product with id {product_id} not found")
        self.logger.info("Product successfully deleted")
        self.repository.delete_product(product)