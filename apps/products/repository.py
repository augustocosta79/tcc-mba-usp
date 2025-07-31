from uuid import UUID
from apps.products.repository_interface import ProductRepositoryInterface
from apps.products.product_entity import Product
from apps.products.models import ProductModel
from apps.users.models import UserModel
from apps.products.serializers import product_model_to_entity

class ProductRepository(ProductRepositoryInterface):
    def save(self, product: Product) -> Product:
        saved_product = ProductModel.objects.create(
            id=product.id,
            title=product.title.value,
            description=product.description.value,
            price=product.price.value,
            stock=product.stock.value,
            owner=UserModel.objects.get(id=product.owner_id),
            is_active=product.is_active
        )

        if len(product.categories) > 0:
            saved_product.categories.set([category.id for category in product.categories])

        return product_model_to_entity(saved_product)
    
    def get_product_by_id(self, product_id: UUID):
        if not (product_data:=ProductModel.objects.filter(id=product_id).first()):
            return None
        return product_model_to_entity(product_data)
    
    def list_products_by_category(self, category_id: UUID):
        products_data = ProductModel.objects.filter(categories__id=category_id).prefetch_related("categories").distinct()
        return [
            product_model_to_entity(product_data)
            for product_data in products_data
        ]
    
    def update_product(self, product: Product):
        product_data = ProductModel.objects.prefetch_related("categories").filter(id=product.id).first()
        if not product_data:
            return None

        product_data.title = product.title.value
        product_data.description = product.description.value
        product_data.price = product.price.value
        product_data.stock = product.stock.value
        product_data.is_active = product.is_active
        product_data.categories.set([category.id for category in product.categories])

        product_data.save()

        return product_model_to_entity(product_data)

    
    def delete_product(self, product: Product) -> None:
        if not (product_data := ProductModel.objects.filter(id=product.id).first()):
            return None        
        product_data.delete()