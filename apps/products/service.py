import logging
from uuid import UUID

from apps.products.product_entity import Product
from apps.products.repository_interface import ProductRepositoryInterface
from apps.products.schema import ProductActivationSchema, ProductUpdateSchema
from apps.shared.exceptions import NotFoundError
from apps.shared.value_objects import Description, Price, Stock, Title
from apps.categories.service import CategoryService
from apps.categories.repository import CategoryRepository
from apps.users.service import UserService
from apps.users.repository import UserRepository
from utils.logger import configure_logger

logger = configure_logger(__name__)

class ProductService:
    def __init__(self, repository:ProductRepositoryInterface, logger: logging.Logger, category_service: CategoryService = None, user_service: UserService = None):
        self.repository = repository
        self.logger = logger
        self.category_service = category_service or CategoryService(CategoryRepository(), logger)
        self.user_service = user_service or UserService(UserRepository(), logger)

    def create_product(
            self,
            title: str,
            description: str,
            price: str,
            stock: int,
            owner_id: UUID,
            categories_ids: list[UUID]
    ) -> Product:
        user = self.user_service.get_user_by_id(owner_id)        
        title = Title(title)
        description = Description(description)
        price = Price(price)
        stock = Stock(stock)
        owner_id = user.id
        categories = [self.category_service.get_category_by_id(uuid) for uuid in categories_ids]
        
        product = Product(
            title,
            description,
            price,
            stock,
            owner_id,
            categories
        )

        saved_product = self.repository.save(product)
        self.logger.info(f"Product successfully created: id {saved_product.id} - name {saved_product.title}")
        return saved_product
    
    def get_product_by_id(self, product_id) -> Product:
        if not (product:=self.repository.get_product_by_id(product_id)):
            self.logger.warning(f"Product with id {product_id} not found")
            raise NotFoundError(f"Product with id {product_id} not found")
        return product
    
    def list_products_by_category(self, category_id: UUID) -> list[Product]:
        return self.repository.list_products_by_category(category_id)
    
    def update_product(self, product_id: UUID, payload: ProductUpdateSchema) -> Product:        
        if not (product := self.repository.get_product_by_id(product_id)):
            self.logger.warning(f"Can't update Product with id {product_id}. Product not found")
            raise NotFoundError(f"Can't update Product with id {product_id}. Product not found")

        payload_data = payload.model_dump(exclude_none=True)

        if "categories" in payload_data:
            category_ids = payload_data.pop("categories")
            categories = [self.category_service.get_category_by_id(cid) for cid in category_ids]
            product.change_categories(categories)

        operations = {
            "title": product.change_title,
            "description": product.change_description,
            "price": product.change_price,
        }

        for attr, value in payload_data.items():
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

    def reserve_stock(self, product_id: UUID, reserved_quantity: int):
        if not (product:=self.repository.get_product_for_update(product_id)):
            self.logger.warning("Product not found. Stock reservation aborted.")
            raise NotFoundError("Product not found")        
        product.reserve_stock(reserved_quantity)
        self.repository.update_product(product)
        return product
    
    
    def release_stock(self, product_id: UUID, released_quantity: int):
        if not (product:=self.repository.get_product_for_update(product_id)):
            self.logger.warning("Product not found. Stock reservation aborted.")
            raise NotFoundError("Product not found")        
        product.release_stock(released_quantity)
        self.repository.update_product(product)
        return product
