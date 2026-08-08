# Como rodar no Cursor (primeira vez)

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
.\.venv\Scripts\Activate.ps1
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
