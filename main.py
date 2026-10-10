
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

from database import initialize_database


def setup_database():
    try:
        initialize_database()
        return {
            "status": "success",
            "message": "Tabla de oportunidades creada correctamente"
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al inicializar la base de datos"
        )
        
from contextlib import asynccontextmanager
from database import initialize_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app.router.lifespan_context = lifespan

@app.get("/database-status")
def database_status():
    database_url = os.environ["DATABASE_URL"]

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT to_regclass('public.opportunities')"
            )
            result = cur.fetchone()

    return {
        "database": "connected",
        "opportunities_table": (
            "created" if result[0] is not None
            else "missing"
        )
    }

