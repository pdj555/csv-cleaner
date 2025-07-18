from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def post(body: bytes, ct="text/csv"):
    return client.post("/clean", files={"file": ("f.csv", body, ct)})

def test_baseline():
    csv = b"name,age,city\nAlice,30,New York\nBob,,Los Angeles\nCharlie,25,\nDiana,28,Boston"
    r = post(csv)
    assert r.status_code == 200
    assert r.json() == [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Diana", "age": 28, "city": "Boston"},
    ]

def test_empty_file():
    assert post(b"\n").json() == []

def test_not_csv():
    assert post(b"{}", ct="application/json").status_code == 400

def test_all_blank_rows():
    csv = b"name,age,city\n,,\n,,"
    assert post(csv).json() == []
