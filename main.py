
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

from collectors.secop import fetch_secop

@app.get("/secop-test", include_in_schema=False)
def secop_test():
    try:
        records = fetch_secop(limit=5)
        return {
            "source": "SECOP II",
            "count": len(records),
            "records": records
        }
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="No se pudo consultar SECOP II"
        )

@app.get("/secop-processes")
def get_secop_processes(limit: int = 20):
    from fastapi import Query
    from database import get_db
    from psycopg.rows import dict_row

    limit = max(1, min(limit, 100))

    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT
                    process_id,
                    entity_name,
                    process_name,
                    sector,
                    estimated_value,
                    publication_date,
                    source_url
                FROM secop_processes
                ORDER BY collected_at DESC, process_id
                LIMIT %s
            """, (limit,))

            records = cur.fetchall()

    return {
        "source": "SECOP II",
        "count": len(records),
        "processes": records
    }

@app.get("/sector-analysis")
def sector_analysis():
    from database import get_db
    from psycopg.rows import dict_row

    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT
                    COALESCE(sector, 'Sin clasificar') AS sector,
                    COUNT(*) AS total_processes,
                    SUM(estimated_value) AS total_value,
                    ROUND(AVG(estimated_value), 2) AS average_value
                FROM secop_processes
                GROUP BY COALESCE(sector, 'Sin clasificar')
                ORDER BY total_processes DESC
            """)

            results = cur.fetchall()

    return {
        "source": "SECOP II",
        "analysis": "Demanda por sector",
        "sectors": results,
        "note": (
            "Muestra exploratoria, no representativa "
            "del mercado colombiano."
        )
    }

@app.get("/data-summary")
def data_summary():
    from database import get_db
    from psycopg.rows import dict_row

    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT
                    COUNT(*) AS total_unique_processes,
                    COUNT(*) FILTER (
                        WHERE sector IS NOT NULL
                        AND sector <> 'Sin clasificar'
                    ) AS classified,
                    COUNT(*) FILTER (
                        WHERE sector IS NULL
                        OR sector = 'Sin clasificar'
                    ) AS unclassified,
                    MIN(publication_date) AS earliest_date,
                    MAX(publication_date) AS latest_date
                FROM secop_processes
            """)
            result = cur.fetchone()

    return result

