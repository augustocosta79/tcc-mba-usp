from apps.orders.entity import Order, OrderItem
from apps.orders.schemas import OrderSchema, OrderItemSchema
from apps.users.schema import UserNestedSchema
from apps.products.schema import ProductNestedSchema
from apps.users.entity import User
from apps.addresses.entity import Address
from apps.products.product_entity import Product
from apps.users.serializers import user_to_nested_schema
from apps.products.serializers import product_to_nested_schema
from apps.addresses.serializers import from_address_entity_to_schema

class OrderDTO:
    @staticmethod
    def build(order: Order, user: User, address: Address, products: list[Product]) -> OrderSchema:
        products_map = {product.id: product for product in products}

        items = []
        for order_item in order.items:
            product = products_map.get(order_item.product_id)
            if not product:
                raise ValueError(f"Produto não encontrado para o ID {order_item.product_id}")

            items.append(
                OrderItemSchema(
                    id=order_item.id,
                    product=product_to_nested_schema(product),
                    quantity=order_item.quantity,
                    price=str(order_item.price.value),
                )
            )

        return OrderSchema(
            id=order.id,
            user=user_to_nested_schema(user),
            address=from_address_entity_to_schema(address),
            items=items,
            status=order.status,
            total_amount=str(order.total_amount.value)
        )