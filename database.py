
import os
import psycopg
from contextlib import contextmanager


@contextmanager
def get_db():
    database_url = os.environ["DATABASE_URL"]

    with psycopg.connect(database_url) as conn:
        yield conn


def initialize_database():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS opportunities (
                    id BIGSERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    sector TEXT,
                    description TEXT,
                    source TEXT,
                    source_url TEXT,
                    score NUMERIC(5,2),
                    status TEXT DEFAULT 'candidate',
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
