from pathlib import Path


FILES = {
    "README.md": """# Estoque Igreja - Skeleton (Django + Next.js)

Aplicacao web para controle de estoque, vendas e caixa com dashboard BI.
""",
    "RUNNING.md": """# Como rodar no Cursor (primeira vez)

## 1) Requisitos

- Python 3.11+
- Node.js 20+
- npm

## 2) Backend (Django)

No terminal do Cursor:

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend em: `http://127.0.0.1:8000`

## 3) Frontend (Next.js)

Abra outro terminal no Cursor:

```bash
cd frontend
npm install
npm run dev
```

Frontend em: `http://localhost:3000`
""",
    "backend/requirements.txt": """Django>=5.0
djangorestframework>=3.15
django-cors-headers>=4.4
plotly>=5.22
""",
    "backend/manage.py": """#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
""",
    "backend/core/__init__.py": "",
    "backend/core/asgi.py": """import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
application = get_asgi_application()
""",
    "backend/core/wsgi.py": """import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
application = get_wsgi_application()
""",
    "backend/core/settings.py": """from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "dev-secret-key-change-me"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "apps.accounts",
    "apps.inventory",
    "apps.sales",
    "apps.finance",
    "apps.analytics",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True, "OPTIONS": {"context_processors": ["django.template.context_processors.request", "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOW_CREDENTIALS = True
REST_FRAMEWORK = {"DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"]}
""",
    "backend/core/urls.py": """from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.analytics.urls")),
]
""",
    "backend/apps/__init__.py": "",
    "backend/apps/accounts/__init__.py": "",
    "backend/apps/accounts/apps.py": """from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    label = "accounts"
""",
    "backend/apps/accounts/models.py": """from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrador"
        USER = "user", "Usuario"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
""",
    "backend/apps/accounts/admin.py": """from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
""",
    "backend/apps/inventory/__init__.py": "",
    "backend/apps/inventory/apps.py": """from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.inventory"
""",
    "backend/apps/inventory/models.py": """from django.conf import settings
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_current = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)


class InventoryMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = "in", "Entrada"
        OUT = "out", "Saida"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movements")
    movement_type = models.CharField(max_length=10, choices=MovementType.choices)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
""",
    "backend/apps/inventory/admin.py": """from django.contrib import admin
from .models import Product, InventoryMovement

admin.site.register(Product)
admin.site.register(InventoryMovement)
""",
    "backend/apps/sales/__init__.py": "",
    "backend/apps/sales/apps.py": """from django.apps import AppConfig


class SalesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.sales"
""",
    "backend/apps/sales/models.py": """from django.conf import settings
from django.db import models
from apps.inventory.models import Product


class Sale(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
""",
    "backend/apps/sales/admin.py": """from django.contrib import admin
from .models import Sale, SaleItem

admin.site.register(Sale)
admin.site.register(SaleItem)
""",
    "backend/apps/finance/__init__.py": "",
    "backend/apps/finance/apps.py": """from django.apps import AppConfig


class FinanceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.finance"
""",
    "backend/apps/finance/models.py": """from django.conf import settings
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
""",
    "backend/apps/finance/admin.py": """from django.contrib import admin
from .models import CashMovement

admin.site.register(CashMovement)
""",
    "backend/apps/analytics/__init__.py": "",
    "backend/apps/analytics/apps.py": """from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.analytics"
""",
    "backend/apps/analytics/urls.py": """from django.urls import path
from .views import HealthView, TopProductsView, CashFlowView

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("bi/top-products/", TopProductsView.as_view(), name="bi-top-products"),
    path("bi/cash-flow/", CashFlowView.as_view(), name="bi-cash-flow"),
]
""",
    "backend/apps/analytics/views.py": """from datetime import timedelta
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
""",
    "frontend/package.json": """{
  "name": "estoque-igreja-frontend",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "14.2.5",
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "react-plotly.js": "2.6.0",
    "plotly.js": "2.34.0"
  }
}
""",
    "frontend/next.config.js": """/** @type {import('next').NextConfig} */
const nextConfig = {};

module.exports = nextConfig;
""",
    "frontend/app/layout.js": """export const metadata = {
  title: "Estoque Igreja",
  description: "Dashboard de estoque",
};

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body style={{ fontFamily: "Arial, sans-serif", margin: 0, padding: 24 }}>
        {children}
      </body>
    </html>
  );
}
""",
    "frontend/app/page.js": """"use client";
import { useEffect, useState } from "react";
import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });
const API_BASE = "http://127.0.0.1:8000/api";

export default function HomePage() {
  const [topProducts, setTopProducts] = useState({ labels: [], values: [] });
  const [cashFlow, setCashFlow] = useState({ labels: [], cash_in: [], cash_out: [] });

  useEffect(() => {
    async function loadData() {
      const [topRes, cashRes] = await Promise.all([
        fetch(`${API_BASE}/bi/top-products/?period=month`, { credentials: "include" }),
        fetch(`${API_BASE}/bi/cash-flow/?period=month`, { credentials: "include" }),
      ]);
      if (!topRes.ok) {
        throw new Error(`Falha ao carregar top-products: HTTP ${topRes.status}`);
      }
      if (!cashRes.ok) {
        throw new Error(`Falha ao carregar cash-flow: HTTP ${cashRes.status}`);
      }
      setTopProducts(await topRes.json());
      setCashFlow(await cashRes.json());
    }
    loadData().catch(console.error);
  }, []);

  return (
    <main>
      <h1>Painel BI - Estoque da Igreja</h1>
      <p>Esqueleto inicial com dados vindos da API Django.</p>
      <h2>Produtos mais vendidos (mes)</h2>
      <Plot
        data={[{ x: topProducts.labels, y: topProducts.values, type: "bar" }]}
        layout={{ width: 850, height: 400, title: "Top 10 produtos" }}
      />
      <h2>Fluxo de caixa (entrou x saiu)</h2>
      <Plot
        data={[
          { x: cashFlow.labels, y: cashFlow.cash_in, type: "scatter", mode: "lines+markers", name: "Entradas" },
          { x: cashFlow.labels, y: cashFlow.cash_out, type: "scatter", mode: "lines+markers", name: "Saidas" },
        ]}
        layout={{ width: 850, height: 400, title: "Fluxo de caixa" }}
      />
    </main>
  );
}
""",
}


def main() -> None:
    root = Path(__file__).resolve().parent
    for relative_path, content in FILES.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(f"Created {len(FILES)} files.")


if __name__ == "__main__":
    main()
