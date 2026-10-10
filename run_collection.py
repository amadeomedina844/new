
from database import initialize_database
from secop_storage import collect_and_save


def main():
    initialize_database()
    result = collect_and_save(limit=100)
    print("SECOP_COLLECTION_RESULT:", result)


if __name__ == "__main__":
    main()
