from django.db import models


class Product(models.Model):
    item_name = models.CharField(max_length=200, verbose_name="Item name")
    brand = models.CharField(max_length=100, verbose_name="Brand")
    category = models.CharField(max_length=100, verbose_name="Category")
    quantity_in_pack = models.IntegerField(verbose_name="Quantity in pack")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price")

    def __str__(self):
        return f"{self.item_name} ({self.brand}) - {self.quantity_in_pack} pcs"