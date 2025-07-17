from uuid import uuid4
from django.db import models

class CategoryModel(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    name = models.CharField(max_length=120, blank=False, null=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"