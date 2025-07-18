from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
from io import StringIO

app = FastAPI()

@app.post("/clean")
async def clean(file: UploadFile = File(...)):
    if file.content_type != "text/csv":
        raise HTTPException(400, "Please upload a CSV file.")
    
    data = await file.read()
    
    if len(data) > 50 * 1024 * 1024:  # 50MB
        raise HTTPException(413, "File too large. Maximum size allowed is 50MB.")
    
    if not data:
        return []
    
    try:
        df = pd.read_csv(StringIO(data.decode('utf-8')))
        return df.dropna().to_dict(orient="records")
    except Exception:
        raise HTTPException(400, "Invalid CSV format.")
