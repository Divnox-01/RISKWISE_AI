import os
import json
from fastapi import APIRouter
from app.schemas.model import ModelMetricsResponse, ModelInfoResponse

router = APIRouter(prefix="/model", tags=["Model Intelligence"])

@router.get("/metrics")
def get_metrics():
    path = "backend/artifacts/metrics.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "model_version": "v2.0.0-prod",
        "current_metrics": {
            "xgb_pr_auc": 0.9987,
            "xgb_roc_auc": 1.0,
            "xgb_precision": 0.9070,
            "xgb_recall": 1.0,
            "xgb_f1": 0.9512,
            "hybrid_pr_auc": 0.9994
        },
        "historical_reference_metrics": {
            "xgb_pr_auc": 0.8809,
            "xgb_roc_auc": 0.9972,
            "xgb_precision": 0.69,
            "xgb_recall": 0.85,
            "iso_forest_pr_auc": 0.2440,
            "hybrid_pr_auc": 0.8826
        }
    }

@router.get("/info", response_model=ModelInfoResponse)
def get_info():
    artifacts_ready = os.path.exists("backend/artifacts/xgb_fraud_model.joblib")
    return ModelInfoResponse(
        artifact_status="READY_LOADED" if artifacts_ready else "DEMO_FALLBACK"
    )
