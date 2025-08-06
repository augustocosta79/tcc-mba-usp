from uuid import uuid4
from django.db import models

class AddressModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey("users.UserModel", on_delete=models.CASCADE, related_name="address")
    street = models.CharField(max_length=150)
    street_number = models.CharField(max_length=20)
    complement = models.CharField(max_length=20)
    district =  models.CharField(max_length=128)
    city = models.CharField(max_length=255)
    state_code = models.CharField(max_length=3)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=2)
    is_default = models.BooleanField(default=False)