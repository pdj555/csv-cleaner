from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def post(body: bytes, ct="text/csv"):
    return client.post("/clean", files={"file": ("test.csv", body, ct)})

def test_baseline():
    csv = b"name,age,city\nAlice,30,New York\nBob,,Los Angeles\nCharlie,25,\nDiana,28,Boston"
    r = post(csv)
    assert r.status_code == 200
    assert r.json() == [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Diana", "age": 28, "city": "Boston"},
    ]

def test_empty_file():
    assert post(b"").json() == []

def test_not_csv():
    assert post(b"{}", ct="application/json").status_code == 400

def test_all_rows_missing_values():
    csv = b"name,age,city\nAlice,,New York\nBob,30,\nCharlie,,"
    assert post(csv).json() == []

def test_headers_only():
    csv = b"name,age,city"
    assert post(csv).json() == []

def test_malformed_csv():
    csv = b"name,age,city\nAlice,30,New York\nBob\nCharlie,twenty,Boston,Extra"
    assert post(csv).status_code == 400

def test_large_csv():
    header = b"name,age,city\n"
    rows = []
    for i in range(1000):
        if i % 100 == 0:
            rows.append(f"Person{i},,City{i}\n".encode())
        else:
            rows.append(f"Person{i},{20 + (i % 50)},City{i}\n".encode())
    
    large_csv = header + b"".join(rows)
    r = post(large_csv)
    assert r.status_code == 200
    result = r.json()
    assert len(result) == 990

def test_file_size_limit():
    header = b"name,age,city\n"
    large_row = b"VeryLongName" + b"x" * 10000 + b",25,VeryLongCity" + b"y" * 10000 + b"\n"
    large_csv = header + large_row * 3000
    
    r = post(large_csv)
    assert r.status_code == 413

def test_large_file_within_limit():
    header = b"name,age,city\n"
    large_row = b"Name" + b"x" * 1000 + b",25,City" + b"y" * 1000 + b"\n"
    large_csv = header + large_row * 5000
    
    r = post(large_csv)
    assert r.status_code == 200

def test_no_file():
    response = client.post("/clean")
    assert response.status_code == 422
