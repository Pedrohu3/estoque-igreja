from django.contrib import admin

from .models import Event, EventItem


class EventItemInline(admin.TabularInline):
    model = EventItem
    extra = 1
    fields = ("product", "quantity", "purchase_price")
    autocomplete_fields = ("product",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "event_date", "user", "items_count", "total_cost_display", "updated_at")
    list_filter = ("event_date",)
    search_fields = ("name", "description", "items__product__name")
    date_hierarchy = "event_date"
    inlines = [EventItemInline]
    readonly_fields = ("user", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "event_date", "description")}),
        ("Registro", {"fields": ("user", "created_at", "updated_at")}),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description="Itens")
    def items_count(self, obj):
        return obj.items.count()

    @admin.display(description="Custo total")
    def total_cost_display(self, obj):
        return f"R$ {obj.total_cost:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@admin.register(EventItem)
class EventItemAdmin(admin.ModelAdmin):
    list_display = ("event", "product", "quantity", "purchase_price", "subtotal_display")
    list_filter = ("event__event_date", "event")
    search_fields = ("event__name", "product__name")
    autocomplete_fields = ("event", "product")

    @admin.display(description="Subtotal")
    def subtotal_display(self, obj):
        return f"R$ {obj.subtotal:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
