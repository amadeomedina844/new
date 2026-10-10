
from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(
    title="Opportunity Radar Colombia",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "platform": "Opportunity Radar",
        "country": "Colombia",
        "status": "online",
        "message": "Motor de inteligencia empresarial iniciado"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

import os
import psycopg
from fastapi import HTTPException

@app.get("/db-health")
def db_health():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL no configurada"
        )

    try:
        with psycopg.connect(
            database_url,
            connect_timeout=5
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                result = cur.fetchone()

        return {
            "database": "connected",
            "test": result[0]
        }

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar a PostgreSQL"
        )
