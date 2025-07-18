# CSV Cleaner

A FastAPI service that removes rows with missing values from CSV files.

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

## Usage

1. Open http://127.0.0.1:8000/docs in your browser
2. Click on POST `/clean` endpoint
3. Click "Try it out"
4. Upload a CSV file
5. Click "Execute"

Returns clean data as JSON:

```json
[
  {"name": "Alice", "age": 30, "city": "New York"},
  {"name": "Diana", "age": 28, "city": "Boston"}
]
```

## Testing

```bash
pytest test_app.py
```

## What it does

- Accepts CSV files only
- Removes any row containing empty cells
- Returns clean data as JSON
- Handles malformed CSV gracefully
