"""Starter E-commerce API - FastAPI skeleton.
Run: pip install -r requirements.txt && uvicorn main:app --reload
This is a starter template: products/orders are kept in memory.
Replace the in-memory lists with PostgreSQL + Redis caching for production.
"""
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="E-commerce API (Starter)")

class Product(BaseModel):
    id: int
    name: str
    price: float

class Order(BaseModel):
    id: int
    product_id: int
    quantity: int = 1

products = [
    Product(id=1, name="Sample Product", price=999.0),
    Product(id=2, name="Sample Gift Set", price=1499.0),
]
orders: List[Order] = []

@app.get("/")
def root():
    return {"message": "E-commerce API starter is running"}

@app.get("/products", response_model=List[Product])
def list_products(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    """Paginated product list - pagination keeps large lists fast."""
    return products[skip:skip + limit]

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    for p in products:
        if p.id == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/orders", response_model=Order, status_code=201)
def create_order(order: Order):
    if not any(p.id == order.product_id for p in products):
        raise HTTPException(status_code=404, detail="Product not found")
    orders.append(order)
    return order
