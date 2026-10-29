# E-commerce API Platform (Starter)

A starter FastAPI project for a simple e-commerce API.

## What it does
- Lists products with pagination (`GET /products?skip=0&limit=20`)
- Gets one product by id
- Creates an order for an existing product

## Run it
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Then open http://127.0.0.1:8000/docs

## Next steps
Replace the in-memory lists with PostgreSQL, add Redis caching for repeated product data, and add tests for order and payment flows.
