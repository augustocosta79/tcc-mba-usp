from uuid import uuid4
from django.db import models

class CartModel(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    user = models.OneToOneField("users.UserModel", on_delete=models.CASCADE, related_name="cart")

    class Meta:
        db_table="carts"

class CartItemModel(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.ProductModel", on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table="cart_items"
