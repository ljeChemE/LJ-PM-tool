from fastapi import FastAPI, HTTPException

from app.db import get_connection

app = FastAPI(title="PM Tool API")


@app.get("/health")
def health() -> dict:
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"database unreachable: {exc}")
    return {"status": "ok"}
