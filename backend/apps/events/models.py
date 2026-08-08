from django.conf import settings
from django.db import models

from apps.inventory.models import Product


class Event(models.Model):
    name = models.CharField("Nome do evento", max_length=200)
    description = models.TextField("Descrição do evento", blank=True)
    event_date = models.DateField("Data do evento")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Registrado por",
    )

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ["-event_date", "-created_at"]

    def __str__(self):
        return f"{self.name} ({self.event_date.strftime('%d/%m/%Y')})"

    @property
    def total_cost(self):
        return sum(item.subtotal for item in self.items.all())


class EventItem(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Evento",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="Produto",
    )
    quantity = models.PositiveIntegerField("Quantidade")
    purchase_price = models.DecimalField(
        "Preço de compra",
        max_digits=10,
        decimal_places=2,
        help_text="Valor unitario pago na compra para este evento.",
    )

    class Meta:
        verbose_name = "Item do evento"
        verbose_name_plural = "Itens do evento"
        ordering = ["id"]

    @property
    def subtotal(self):
        return self.quantity * self.purchase_price

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) - {self.event.name}"
