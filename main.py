
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
