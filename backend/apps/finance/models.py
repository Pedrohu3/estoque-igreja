from django.conf import settings
from django.db import models


class CashMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = "in", "Entrada"
        OUT = "out", "Saida"

    movement_type = models.CharField(max_length=10, choices=MovementType.choices)
    category = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
