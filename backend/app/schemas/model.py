from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ModelMetricsResponse(BaseModel):
    model_version: str
    training_timestamp: str
    dataset_rows: int
    train_rows: int
    test_rows: int
    current_metrics: Dict[str, Any]
    historical_reference_metrics: Dict[str, Any]
    feature_importances: List[Any]
    hybrid_weights: Dict[str, float]
    thresholds: Dict[str, float]

class ModelInfoResponse(BaseModel):
    name: str = "RiskWise AI 2.0 Hybrid Fraud Engine"
    version: str = "v2.0.0-prod"
    status: str = "ACTIVE_PRODUCTION"
    algorithms: List[str] = [
        "XGBoost Supervised Gradient Boosted Trees (Imbalanced weighted)",
        "Isolation Forest Unsupervised Anomaly Detection (Robust Scaler)",
        "Behavioural PaySim Typology Rule Heuristics Engine",
        "SHAP TreeExplainer Localized Additive Feature Attribution"
    ]
    artifact_status: str
