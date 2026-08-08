# Estoque Igreja (Django + Next.js)

Este repositorio contem um backend em **Django** (com DRF) e um frontend em **Next.js** para montar um dashboard BI sobre estoque/vendas/caixa.

## Backend (Django): resumo do que foi feito

### Estrutura / Arquitetura (MVC na prática)
- **Model (M)**: entidades do banco em `backend/apps/*/models.py`.
- **Controller (C)**: endpoints de API em `backend/apps/analytics/views.py` (consultam o banco via ORM).
- **View (V)**: respostas JSON da API para o BI.

### Apps do backend
- `apps.accounts`
  - Modelo customizado `User` via `AbstractUser`, com campo `role` (`admin`/`user`).
- `apps.inventory`
  - `Product` (sku, categoria, preco, estoque atual, ativo).
  - `InventoryMovement` (historico de entrada/saida no estoque).
- `apps.sales`
  - `Sale` (data de criacao, usuario, total).
  - `SaleItem` (item de venda: produto, quantidade, preco unitario, subtotal).
- `apps.finance`
  - `CashMovement` (entrada/saida, categoria, valor, descricao).
- `apps.analytics`
  - Endpoints de BI (consultas agregadas no banco e retorno JSON).

### Ajuste de legibilidade no Admin (sem "Sale Object (1)")
Para evitar que o Django Admin mostre apenas `Sale Object (1)` / IDs "crus", adicionamos `__str__()`:
- `Sale`: mostra `Venda de DD/MM/YYYY - HH:MM`
- `SaleItem`: mostra `Item: <produto> (x<quantidade>) - <venda>`

Isso melhora a identificação das vendas ao cadastrar/visualizar registros no admin.

## Rodar o backend

### Pre-requisitos
- Python 3.11+
- ambiente virtual (recomendado)

### Comandos (Windows / PowerShell)
No terminal:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend em: `http://127.0.0.1:8000`

## Admin

- Admin em: `http://127.0.0.1:8000/admin`
- Voce encontra os modelos registrados:
  - `User`
  - `Product`, `InventoryMovement`
  - `Sale`, `SaleItem`
  - `CashMovement`

## Banco de dados

- SQLite local: `backend/db.sqlite3`

## Rotas da API (DRF)

Base da API: `http://127.0.0.1:8000/api/`

O `core/settings.py` esta com:
- `REST_FRAMEWORK.DEFAULT_PERMISSION_CLASSES = IsAuthenticated`
- Porem as rotas de BI em `apps.analytics` usam `permission_classes = [AllowAny]` (liberadas para o dashboard durante desenvolvimento).

### Health
- `GET /api/health/`
  - Retorna: `{"status":"ok"}`

### BI: produtos mais vendidos
- `GET /api/bi/top-products/?period=<month|quarter|year>`
- Padrao: `period=month`
- Consulta: soma a `quantity` por `product__name` nos `SaleItem` da janela de tempo, retornando Top 10.

Resposta (exemplo de formato):
- `{
    "period": "month",
    "labels": ["Produto A", "Produto B", ...],
    "values": [12, 9, ...]
  }`

### BI: fluxo de caixa (entradas x saídas)
- `GET /api/bi/cash-flow/?period=<month|quarter|year>`
- Padrao: `period=month`
- Consulta:
  - agrupa `CashMovement` por dia (`TruncDay(created_at)`)
  - separa por `movement_type` (`in` / `out`)

Resposta (formato):
- `{
    "period": "month",
    "labels": ["2026-04-01", "2026-04-02", ...],
    "cash_in": [100.00, 0, ...],
    "cash_out": [0, 50.00, ...]
  }`

## CORS (frontend local)

No backend (`core/settings.py`):
- `CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]`
- `CORS_ALLOW_CREDENTIALS = True`

Isso permite o frontend local buscar os endpoints do backend sem bloqueio de CORS.