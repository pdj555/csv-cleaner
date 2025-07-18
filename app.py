from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from io import StringIO

app = FastAPI()

@app.post("/clean")
async def clean(file: UploadFile = File(...)):
    # 1. Accept only CSV
    if file.content_type != "text/csv":
        raise HTTPException(400, "Please upload a CSV file.")

    # 2. Read file contents
    data = await file.read()
    if not data.strip(): # empty file -> empty list
        return []

    # 3. Parse CSV safely
    try:
        df = pd.read_csv(StringIO(data.decode('utf-8')))
    except UnicodeDecodeError:
        raise HTTPException(400, "File encoding not supported. Please use UTF-8.")
    except Exception:
        raise HTTPException(400, "Malformed CSV.")

    # 4. Drop any row with a missing value
    cleaned = df.dropna(how="any")

    # 5. Return as JSON list of dicts
    return JSONResponse(cleaned.to_dict(orient="records"))
