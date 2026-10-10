

from database import initialize_database
from secop_storage import collect_and_save


def main():
    initialize_database()

    total_received = 0
    total_saved = 0
    total_skipped = 0

    for page in range(10):
        offset = page * 100

        result = collect_and_save(
            limit=100,
            offset=offset
        )

        total_received += result["received"]
        total_saved += result["saved_or_updated"]
        total_skipped += result["skipped"]

        print(
            f"Page {page + 1}: {result}",
            flush=True
        )

        if result["received"] < 100:
            break

    print(
        "SECOP_COLLECTION_RESULT:",
        {
            "received": total_received,
            "saved_or_updated": total_saved,
            "skipped": total_skipped
        },
        flush=True
    )


if __name__ == "__main__":
    main()
