from django.conf import settings
from django.db import models


class Product(models.Model):
    class Category(models.TextChoices):
        CONSUMIVEL = "consumivel", "Consumível"
        SERVICO = "servico", "Serviço"
        ELETRONICO = "eletronico", "Eletrônico"
        MOVEL = "movel", "Móvel"
        LIVRO = "livro", "Livro"

    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.CONSUMIVEL,
        verbose_name="Categoria",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_current = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"


class InventoryMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = "in", "Entrada"
        OUT = "out", "Saida"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movements")
    movement_type = models.CharField(max_length=10, choices=MovementType.choices)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Registrado por",
    )

    def __str__(self):
        tipo = "Entrada" if self.movement_type == self.MovementType.IN else "Saida"
        return f"{tipo}: {self.product.name} (x{self.quantity})"
