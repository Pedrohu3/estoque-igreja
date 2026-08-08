from django.urls import path
from .views import HealthView, TopProductsView, CashFlowView

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("bi/top-products/", TopProductsView.as_view(), name="bi-top-products"),
    path("bi/cash-flow/", CashFlowView.as_view(), name="bi-cash-flow"),
]
