from apps.carts.entity import Cart
from apps.carts.schema import CartSchema, CartItemSchema
from apps.products.serializers import product_to_schema


def cart_entity_to_schema(cart: Cart) -> CartSchema:
    return CartSchema(
        id=cart.id,
        user_id=cart.user_id,
        items=[
            CartItemSchema(
                id=item.id,
                product=product_to_schema(item.product),
                quantity=item.quantity
            )
            for item in cart.items
        ]
    )
