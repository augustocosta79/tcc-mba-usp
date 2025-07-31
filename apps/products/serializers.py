from apps.products.product_entity import Product
from apps.products.schema import ProductSchema
from apps.products.models import ProductModel
from apps.categories.serializers import category_to_nested_schema
from apps.shared.value_objects import Title, Description, Price, Stock
from apps.categories.serializers import category_model_to_entity

def product_to_schema(product: Product) -> ProductSchema:
    return ProductSchema(
            id=product.id,
            title=product.title.value,
            description=product.description.value,
            price=str(product.price.value),
            stock=product.stock.value,
            owner_id=product.owner_id,
            categories=[ category_to_nested_schema(category) for category in product.categories ],
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )

def product_model_to_entity(product_model: ProductModel) -> Product:
    return Product(
            id=product_model.id,
            title=Title(product_model.title),
            description=Description(product_model.description),
            price=Price(product_model.price),
            stock=Stock(product_model.stock),
            owner_id=product_model.owner.id,
            categories=[ category_model_to_entity(c) for c in product_model.categories.all() ],
            is_active=product_model.is_active,
            created_at=product_model.created_at,
            updated_at=product_model.updated_at
        )
