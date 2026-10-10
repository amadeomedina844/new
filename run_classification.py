
from database import get_db
from analytics.classifier import classify_sector


def classify_processes():
    updated = 0
    unclassified = 0

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT process_id, process_name, description
                FROM secop_processes
                WHERE sector IS NULL
            """)

            records = cur.fetchall()

            for process_id, name, description in records:
                text = f"{name or ''} {description or ''}"
                sector = classify_sector(text)

                cur.execute("""
                    UPDATE secop_processes
                    SET sector = %s
                    WHERE process_id = %s
                """, (sector, process_id))

                updated += 1

                if sector == "Sin clasificar":
                    unclassified += 1

    return {
        "processed": updated,
        "classified": updated - unclassified,
        "unclassified": unclassified
    }


if __name__ == "__main__":
    result = classify_processes()
    print("CLASSIFICATION_RESULT:", result, flush=True)
