from django.db import models
from uuid import uuid4

class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    owner = models.ForeignKey("users.UserModel", on_delete=models.CASCADE, related_name="products")
    categories = models.ManyToManyField("categories.CategoryModel")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
