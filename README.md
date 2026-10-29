# E-commerce API Platform

FastAPI + SQLAlchemy API for products and orders.

## What it does
- Lists products with pagination and a simple in-memory cache (`GET /products?skip=0&limit=20`)
- Adds products (cache is cleared, so lists never go stale)
- Creates orders only for products that exist

## Database
PostgreSQL: set `DATABASE_URL`, e.g. `postgresql://user:pass@localhost:5432/shop`.
Without it, SQLite file `app.db` is used, so it runs anywhere.

## Run it
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Docs: http://127.0.0.1:8000/docs

## Tests
```bash
pytest
```

