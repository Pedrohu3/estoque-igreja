from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.finance.models import CashMovement
from apps.sales.models import SaleItem


def period_start(period: str):
    now = timezone.now()
    if period == "year":
        return now - timedelta(days=365)
    if period == "quarter":
        return now - timedelta(days=90)
    return now - timedelta(days=30)


class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


class TopProductsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        period = request.query_params.get("period", "month")
        start = period_start(period)
        qs = (
            SaleItem.objects.filter(sale__created_at__gte=start)
            .values("product__name")
            .annotate(total_qty=Sum("quantity"))
            .order_by("-total_qty")[:10]
        )
        return Response({"period": period, "labels": [i["product__name"] for i in qs], "values": [i["total_qty"] for i in qs]})


class CashFlowView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        period = request.query_params.get("period", "month")
        start = period_start(period)
        daily = (
            CashMovement.objects.filter(created_at__gte=start)
            .annotate(day=TruncDay("created_at"))
            .values("day", "movement_type")
            .annotate(total=Sum("amount"))
            .order_by("day")
        )
        cash_in, cash_out = {}, {}
        for row in daily:
            key = row["day"].date().isoformat()
            if row["movement_type"] == "in":
                cash_in[key] = float(row["total"] or 0)
            else:
                cash_out[key] = float(row["total"] or 0)
        labels = sorted(set(cash_in.keys()) | set(cash_out.keys()))
        return Response({"period": period, "labels": labels, "cash_in": [cash_in.get(d, 0) for d in labels], "cash_out": [cash_out.get(d, 0) for d in labels]})
