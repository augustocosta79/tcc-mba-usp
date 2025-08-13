from apps.carts.repository_interface import CartRepositoryInterface
from apps.carts.entity import Cart, CartItem
from apps.carts.models import CartModel, CartItemModel
from apps.users.models import UserModel
from apps.products.models import ProductModel

from apps.products.serializers import product_model_to_entity

class CartRepository(CartRepositoryInterface):
    def save(self, cart: Cart) -> Cart:
        user = UserModel.objects.get(id=cart.user_id)
        cart_data = CartModel.objects.create(id=cart.id, user=user)
        items = []

        for cart_item in cart.items:
            product_model = ProductModel.objects.get(id=cart_item.product.id)
            cart_item_model = CartItemModel.objects.create(cart=cart_data, product=product_model, quantity=cart_item.quantity)
            items.append(cart_item_model)

        return Cart(
            user_id=user.id,
            items=[ CartItem(product_model_to_entity(item.product), item.quantity, item.id) for item in items ],
            id=cart_data.id
        )
    
    def update(self, cart: Cart) -> Cart:
        cart_data = CartModel.objects.filter(id=cart.id).first()
        if not cart_data:
            return None
        
        CartItemModel.objects.filter(cart__id=cart.id).delete()
        items = []
        for cart_item in cart.items:
            product_model = ProductModel.objects.get(id=cart_item.product.id)
            cart_item_model = CartItemModel.objects.create(cart=cart_data, product=product_model, quantity=cart_item.quantity)
            items.append(cart_item_model)

        return Cart(
            user_id=cart_data.user.id,
            items=[ CartItem(product_model_to_entity(item.product), item.quantity, item.id) for item in items ],
            id=cart_data.id
        )
    
    def get_cart_by_user(self, user_id) -> Cart:
        cart_data = CartModel.objects.filter(user__id=user_id).first()
        if not cart_data:
            return None
        items = cart_data.items.all()
        return Cart(
            user_id,
            [ CartItem(product_model_to_entity(item.product), item.quantity, item.id) for item in items ],
            cart_data.id
        )