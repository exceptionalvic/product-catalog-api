from django.db import models

from apps.mixins import BaseMixin, TimeStampMixin
from apps.utils import generate_id

class Product(TimeStampMixin, BaseMixin):
    id = models.CharField(max_length=60, primary_key=True, default=generate_id, editable=False)
    name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name