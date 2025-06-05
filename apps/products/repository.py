from uuid import UUID
from apps.products.repository_interface import ProductRepositoryInterface
from apps.products.product_entity import Product
from apps.products.models import ProductModel
from apps.shared.value_objects import Title, Description, Price, Stock

class ProductRepository(ProductRepositoryInterface):
    def save(self, product: Product) -> Product:
        saved_product = ProductModel.objects.create(
            id=product.id,
            title=product.title.text,
            description=product.description.text,
            price=product.price.value,
            stock=product.stock.value,
            owner_id=product.owner_id,
            category=product.category,
            is_active=product.is_active
        )

        return Product(
            id=saved_product.id,
            title=Title(saved_product.title),
            description=Description(saved_product.description),
            price=Price(saved_product.price),
            stock=Stock(saved_product.stock),
            owner_id=saved_product.owner_id,
            category=saved_product.category,
            is_active=saved_product.is_active,
            created_at=saved_product.created_at,
            updated_at=saved_product.updated_at
        )
    
    def get_product_by_id(self, product_id: UUID):
        if not (product_data:=ProductModel.objects.filter(id=product_id).first()):
            return None
        return Product(
            id=product_data.id,
            title=Title(product_data.title),
            description=Description(product_data.description),
            price=Price(product_data.price),
            stock=Stock(product_data.stock),
            owner_id=product_data.owner_id,
            category=product_data.category,
            is_active=product_data.is_active,
            created_at=product_data.created_at,
            updated_at=product_data.updated_at
        )
    
    def list_products_by_category(self, category: str):
        products_data = ProductModel.objects.filter(category=category)
        return [
            Product(
                id=product_data.id,
                title=Title(product_data.title),
                description=Description(product_data.description),
                price=Price(product_data.price),
                stock=Stock(product_data.stock),
                owner_id=product_data.owner_id,
                category=product_data.category,
                is_active=product_data.is_active,
                created_at=product_data.created_at,
                updated_at=product_data.updated_at
            )

            for product_data in products_data
        ]
    
    def update_product(self, product: Product):
        if not (product_data := ProductModel.objects.filter(id=product.id).first()):
            return None

        product_data.title = product.title.text
        product_data.description = product.description.text
        product_data.price = product.price.value
        product_data.stock = product.stock.value
        product_data.owner_id = product.owner_id
        product_data.category = product.category
        product_data.is_active = product.is_active

        product_data.save()

        return Product(
                id=product_data.id,
                title=Title(product_data.title),
                description=Description(product_data.description),
                price=Price(product_data.price),
                stock=Stock(product_data.stock),
                owner_id=product_data.owner_id,
                category=product_data.category,
                is_active=product_data.is_active,
                created_at=product_data.created_at,
                updated_at=product_data.updated_at
            )
    
    def delete_product(self, product: Product) -> None:
        if not (product_data := ProductModel.objects.filter(id=product.id).first()):
            return None        
        product_data.delete()