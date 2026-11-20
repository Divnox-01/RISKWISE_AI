from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.prediction import PredictRequest, PredictResponse
from app.services.prediction_service import process_prediction
from app.services.audit_service import record_audit

router = APIRouter(tags=["ML Prediction"])

@router.post("/predict", response_model=PredictResponse)
def predict_transaction_endpoint(
    request: PredictRequest,
    db: Session = Depends(get_db)
):
    result = process_prediction(db, request)
    record_audit(
        db,
        user_email="system@riskwise.ai",
        action="TRANSACTION_EVALUATED",
        entity_type="Transaction",
        entity_id=result.tx_hash,
        details={"risk_score": result.risk_score, "category": result.risk_category}
    )
    return result
