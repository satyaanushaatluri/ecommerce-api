from fastapi.testclient import TestClient
from database import Base, engine
from models import Product
import main

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
main.seed(next(main.get_db()))
client = TestClient(main.app)

def test_list_products():
    r = client.get("/products")
    assert r.status_code == 200
    assert len(r.json()) >= 2

def test_create_and_get_product():
    r = client.post("/products", json={"name": "Test Item", "price": 100.0})
    assert r.status_code == 201
    pid = r.json()["id"]
    assert client.get(f"/products/{pid}").json()["name"] == "Test Item"

def test_order_for_missing_product_is_404():
    assert client.post("/orders", json={"product_id": 99999, "quantity": 1}).status_code == 404

