import json
import uuid
from sqlalchemy.orm import Session
from app.ml_engine.pipeline import FraudInferencePipeline
from app.models.transaction import Transaction
from app.models.prediction import PredictionResult
from app.models.alert import FraudAlert
from app.schemas.prediction import PredictRequest, PredictResponse

# Singleton pipeline instance
_inference_pipeline = None

def get_pipeline() -> FraudInferencePipeline:
    global _inference_pipeline
    if _inference_pipeline is None:
        _inference_pipeline = FraudInferencePipeline(artifacts_dir="backend/artifacts")
    return _inference_pipeline

def process_prediction(db: Session, request: PredictRequest) -> PredictResponse:
    pipeline = get_pipeline()
    
    tx_data = {
        "step": request.step,
        "type": request.type.upper(),
        "amount": request.amount,
        "nameOrig": request.nameOrig,
        "oldbalanceOrg": request.oldbalanceOrg,
        "nameDest": request.nameDest,
        "oldbalanceDest": request.oldbalanceDest
    }
    
    # Run ML Inference
    result = pipeline.predict_transaction(tx_data)
    
    tx_hash = "TX-" + uuid.uuid4().hex[:12].upper()
    db_tx_id = None
    alert_created = False
    alert_code = None

    if request.persist:
        # Create Transaction
        tx_row = Transaction(
            tx_hash=tx_hash,
            step=request.step,
            type=request.type.upper(),
            amount=request.amount,
            nameOrig=request.nameOrig,
            oldbalanceOrg=request.oldbalanceOrg,
            newbalanceOrig=request.newbalanceOrig,
            nameDest=request.nameDest,
            oldbalanceDest=request.oldbalanceDest,
            newbalanceDest=request.newbalanceDest,
            is_demo_seed=False
        )
        db.add(tx_row)
        db.flush() # obtain tx_row.id
        db_tx_id = tx_row.id

        # Create PredictionResult
        pred_row = PredictionResult(
            transaction_id=tx_row.id,
            risk_score=result["risk_score"],
            risk_category=result["risk_category"],
            recommended_action=result["recommended_action"],
            action_description=result["action_description"],
            xgb_fraud_probability=result["score_breakdown"]["xgb_fraud_probability"],
            isolation_forest_anomaly_score=result["score_breakdown"]["isolation_forest_anomaly_score"],
            rule_engine_score=result["score_breakdown"]["rule_engine_score"],
            rules_triggered_json=json.dumps(result["rules"]),
            shap_explanation_json=json.dumps(result["shap_explanation"]),
            is_demo_mode=(result["engine_mode"] == "DEMO_SYNTHETIC_MODE")
        )
        db.add(pred_row)
        db.flush()

        # If High Risk (>= 65) or Medium Risk (>= 40), generate automatic FraudAlert
        if result["risk_score"] >= 35.0:
            severity = "CRITICAL" if result["risk_score"] >= 80.0 else ("HIGH" if result["risk_score"] >= 65.0 else "MEDIUM")
            alert_code = "ALT-" + uuid.uuid4().hex[:8].upper()
            alert_row = FraudAlert(
                alert_code=alert_code,
                transaction_id=tx_row.id,
                prediction_id=pred_row.id,
                severity=severity,
                risk_score=result["risk_score"],
                status="OPEN",
                assigned_to=None
            )
            db.add(alert_row)
            alert_created = True

        db.commit()

    return PredictResponse(
        tx_hash=tx_hash,
        transaction_id=db_tx_id,
        transaction_data=result["transaction_data"],
        risk_score=result["risk_score"],
        risk_category=result["risk_category"],
        recommended_action=result["recommended_action"],
        action_description=result["action_description"],
        score_breakdown=result["score_breakdown"],
        rules=result["rules"],
        shap_explanation=result["shap_explanation"],
        engine_mode=result["engine_mode"],
        alert_created=alert_created,
        alert_code=alert_code
    )
