
import os
import httpx

SECOP_DATASET_ID = os.getenv(
    "SECOP_DATASET_ID",
    "p6dx-8zbt"
)

SECOP_URL = (
    "https://www.datos.gov.co/resource/"
    f"{SECOP_DATASET_ID}.json"
)


def fetch_secop(limit=10):
    with httpx.Client(timeout=30) as client:
        response = client.get(
            SECOP_URL,
            params={"$limit": min(limit, 100)}
        )
        response.raise_for_status()
        return response.json()
