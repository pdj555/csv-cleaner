# CSV Cleaner

Clean CSV files by removing rows with missing values.

## Setup

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

## Usage

POST `/clean` with CSV file → JSON response

Docs: `http://127.0.0.1:8000/docs`

## Example

Input:
```csv
name,age,city
Alice,30,New York
Bob,,Los Angeles
Diana,28,Boston
```

Output:
```json
[
  {"name": "Alice", "age": 30, "city": "New York"},
  {"name": "Diana", "age": 28, "city": "Boston"}
]
```
