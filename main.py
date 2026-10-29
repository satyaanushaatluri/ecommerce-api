"""E-commerce API - FastAPI + SQLAlchemy.
Database: PostgreSQL via DATABASE_URL, or SQLite (app.db) by default.
Caching: the product list is cached in memory and cleared when a product is added.
Run: pip install -r requirements.txt && uvicorn main:app --reload
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import Product, Order

Base.metadata.create_all(bind=engine)
app = FastAPI(title="E-commerce API")

_product_cache = {}

class ProductIn(BaseModel):
    name: str
    price: float

class ProductOut(ProductIn):
    id: int

class OrderIn(BaseModel):
    product_id: int
    quantity: int = 1

class OrderOut(OrderIn):
    id: int

def seed(db: Session):
    if db.query(Product).count() == 0:
        db.add_all([Product(name="Sample Product", price=999.0),
                    Product(name="Sample Gift Set", price=1499.0)])
        db.commit()

@app.on_event("startup")
def startup():
    seed(next(get_db()))

@app.get("/")
def root():
    return {"message": "E-commerce API is running"}

@app.get("/products", response_model=list[ProductOut])
def list_products(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100),
                  db: Session = Depends(get_db)):
    # Pagination keeps large lists fast; the cache avoids re-querying the same page.
    key = (skip, limit)
    if key in _product_cache:
        return _product_cache[key]
    rows = db.query(Product).offset(skip).limit(limit).all()
    result = [ProductOut(id=r.id, name=r.name, price=r.price) for r in rows]
    _product_cache[key] = result
    return result

@app.post("/products", response_model=ProductOut, status_code=201)
def create_product(data: ProductIn, db: Session = Depends(get_db)):
    row = Product(name=data.name, price=data.price)
    db.add(row); db.commit(); db.refresh(row)
    _product_cache.clear()  # cached lists would otherwise show stale products
    return ProductOut(id=row.id, name=data.name, price=data.price)

@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    row = db.query(Product).filter(Product.id == product_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductOut(id=row.id, name=row.name, price=row.price)

@app.post("/orders", response_model=OrderOut, status_code=201)
def create_order(data: OrderIn, db: Session = Depends(get_db)):
    if not db.query(Product).filter(Product.id == data.product_id).first():
        raise HTTPException(status_code=404, detail="Product not found")
    row = Order(product_id=data.product_id, quantity=data.quantity)
    db.add(row); db.commit(); db.refresh(row)
    return OrderOut(id=row.id, product_id=row.product_id, quantity=row.quantity)

@app.get("/orders", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    rows = db.query(Order).all()
    return [OrderOut(id=r.id, product_id=r.product_id, quantity=r.quantity) for r in rows]

