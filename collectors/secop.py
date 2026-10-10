
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


def fetch_secop(limit=100, offset=0):
    limit = max(1, min(int(limit), 1000))
    offset = max(0, int(offset))

    params = {
        "$where": "fecha_de_publicacion_del IS NOT NULL",
        "$limit": limit,
        "$offset": offset,
        "$order": (
            "fecha_de_publicacion_del DESC, "
            "id_del_proceso ASC"
        )
    }

    with httpx.Client(timeout=60) as client:
        response = client.get(
            SECOP_URL,
            params=params
        )
        response.raise_for_status()
        return response.json()
