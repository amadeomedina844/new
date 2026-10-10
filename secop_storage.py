
from datetime import datetime
from psycopg.types.json import Jsonb

from database import get_db
from collectors.secop import fetch_secop


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
    except (ValueError, TypeError):
        return None


def collect_and_save(limit=100):
    records = fetch_secop(limit=limit)
    saved = 0
    skipped = 0

    with get_db() as conn:
        with conn.cursor() as cur:
            for record in records:
                process_id = record.get("id_del_proceso")

                if not process_id:
                    skipped += 1
                    continue

                cur.execute("""
                    INSERT INTO secop_processes (
                        process_id,
                        entity_name,
                        process_name,
                        description,
                        estimated_value,
                        publication_date,
                        source_url,
                        raw_data
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (process_id)
                    DO UPDATE SET
                        entity_name = EXCLUDED.entity_name,
                        process_name = EXCLUDED.process_name,
                        description = EXCLUDED.description,
                        estimated_value = EXCLUDED.estimated_value,
                        publication_date = EXCLUDED.publication_date,
                        source_url = EXCLUDED.source_url,
                        raw_data = EXCLUDED.raw_data
                """, (
                    process_id,
                    record.get("entidad"),
                    record.get("nombre_del_procedimiento"),
                    record.get("descripci_n_del_procedimiento"),
                    record.get("precio_base"),
                    parse_date(
                        record.get("fecha_de_publicacion_del")
                    ),
                    record.get("urlproceso", {}).get("url")
                    if isinstance(record.get("urlproceso"), dict)
                    else None,
                    Jsonb(record)
                ))

                saved += 1

    return {
        "received": len(records),
        "saved_or_updated": saved,
        "skipped": skipped
    }
