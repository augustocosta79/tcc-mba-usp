from apps.products.product_entity import Product
from apps.products.schema import ProductSchema
from apps.categories.serializers import category_to_nested_schema

def product_to_schema(product: Product) -> ProductSchema:
    return ProductSchema(
            id=product.id,
            title=product.title.text,
            description=product.description.text,
            price=str(product.price.value),
            stock=product.stock.value,
            owner_id=product.owner_id,
            categories=[ category_to_nested_schema(category) for category in product.categories ],
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )
