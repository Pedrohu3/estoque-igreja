from django.conf import settings
from django.db import models
from django.utils import timezone
from apps.inventory.models import Product


class Sale(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        local_created_at = timezone.localtime(self.created_at)
        return f"Venda de {local_created_at.strftime('%d/%m/%Y - %H:%M')}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Item: {self.product.name} (x{self.quantity}) - {self.sale}"
