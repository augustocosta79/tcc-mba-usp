from uuid import uuid4
from django.db import models

class OrderModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.UUIDField()
    address_id = models.UUIDField()
    status = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItemModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(OrderModel, related_name="items", on_delete=models.CASCADE)
    product_id = models.UUIDField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
