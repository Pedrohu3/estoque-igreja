from django.contrib import admin

from .models import InventoryMovement, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("name", "sku", "category")
    list_display = ("name", "sku", "category", "price", "stock_current", "active")
    list_filter = ("category", "active")


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "movement_type", "quantity", "user", "created_at")
    list_filter = ("movement_type", "created_at")
    search_fields = ("product__name", "product__sku")
    autocomplete_fields = ("product",)
    readonly_fields = ("user", "created_at")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)
