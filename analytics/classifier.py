
SECTORS = {
    "Salud": [
        "hospital", "medicamento", "enfermeria",
        "clinica", "farmaceutico", "laboratorio"
    ],
    "Construcción": [
        "construccion", "obra civil", "infraestructura",
        "pavimentacion", "edificacion"
    ],
    "Tecnología": [
        "software", "sistema de informacion",
        "computador", "telecomunicaciones",
        "tecnologia"
    ],
    "Agroindustria": [
        "agricola", "agroindustrial", "cultivo",
        "ganadero", "riego", "fertilizante"
    ],
    "Energía": [
        "energia electrica", "transformador",
        "panel solar", "fotovoltaico"
    ],
    "Logística": [
        "transporte", "almacenamiento",
        "distribucion", "logistica"
    ],
    "Servicios empresariales": [
        "servicios profesionales", "consultoria",
        "asesoria", "apoyo a la gestion"
    ],
    "Industria": [
        "maquinaria", "manufactura",
        "industrial", "equipos mecanicos"
    ]
}


def classify_sector(text):
    import unicodedata

    if not text:
        return "Sin clasificar"

    normalized = unicodedata.normalize(
        "NFKD", text.lower()
    )
    normalized = "".join(
        c for c in normalized
        if not unicodedata.combining(c)
    )

    scores = {}

    for sector, keywords in SECTORS.items():
        scores[sector] = sum(
            1 for keyword in keywords
            if keyword in normalized
        )

    best = max(scores, key=scores.get)

    return best if scores[best] > 0 else "Sin clasificar"
