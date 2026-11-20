from datetime import datetime, timezone
from fastapi import APIRouter
from app.services.azure_blob import AzureBlobStorageService

router = APIRouter()

@router.get("/health")
def get_health():
    azure_status = AzureBlobStorageService().get_status()
    return {
        "status": "HEALTHY",
        "service": "RISKWISE AI 2.0 API",
        "version": "2.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cloud_storage": azure_status["mode"],
        "database": "CONNECTED",
        "ml_engine": "ACTIVE"
    }
