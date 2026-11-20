from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.transaction import Transaction
from app.models.prediction import PredictionResult
from app.models.alert import FraudAlert
from app.models.investigation import Investigation
from app.schemas.analytics import OverviewStats, TrendDataPoint, RiskDistributionItem

def get_overview_stats(db: Session) -> OverviewStats:
    total_tx = db.query(Transaction).count()
    if total_tx == 0:
        return OverviewStats(
            total_transactions_analyzed=0,
            fraud_transactions_detected=0,
            high_risk_transactions=0,
            medium_risk_transactions=0,
            low_risk_transactions=0,
            fraud_detection_rate=0.0,
            average_risk_score=0.0,
            open_alerts_count=0,
            active_investigations_count=0
        )
        
    high_count = db.query(PredictionResult).filter(PredictionResult.risk_category == "High Risk").count()
    med_count = db.query(PredictionResult).filter(PredictionResult.risk_category == "Medium Risk").count()
    low_count = db.query(PredictionResult).filter(PredictionResult.risk_category == "Low Risk").count()
    avg_score = db.query(func.avg(PredictionResult.risk_score)).scalar() or 0.0
    
    open_alerts = db.query(FraudAlert).filter(FraudAlert.status == "OPEN").count()
    active_inv = db.query(Investigation).filter(Investigation.status == "ACTIVE").count()
    
    return OverviewStats(
        total_transactions_analyzed=total_tx,
        fraud_transactions_detected=high_count,
        high_risk_transactions=high_count,
        medium_risk_transactions=med_count,
        low_risk_transactions=low_count,
        fraud_detection_rate=round((high_count / total_tx) * 100, 2),
        average_risk_score=round(float(avg_score), 2),
        open_alerts_count=open_alerts,
        active_investigations_count=active_inv
    )

def get_risk_distribution(db: Session):
    total = db.query(PredictionResult).count()
    if total == 0:
        return [
            {"category": "Low Risk (<35)", "count": 0, "percentage": 0.0},
            {"category": "Medium Risk (35-65)", "count": 0, "percentage": 0.0},
            {"category": "High Risk (>=65)", "count": 0, "percentage": 0.0}
        ]
    high = db.query(PredictionResult).filter(PredictionResult.risk_category == "High Risk").count()
    med = db.query(PredictionResult).filter(PredictionResult.risk_category == "Medium Risk").count()
    low = db.query(PredictionResult).filter(PredictionResult.risk_category == "Low Risk").count()

    return [
        {"category": "Low Risk (<35)", "count": low, "percentage": round((low / total) * 100, 1)},
        {"category": "Medium Risk (35-65)", "count": med, "percentage": round((med / total) * 100, 1)},
        {"category": "High Risk (>=65)", "count": high, "percentage": round((high / total) * 100, 1)}
    ]

def get_trend_analytics(db: Session):
    # Group transactions by hour windows
    txs = db.query(Transaction, PredictionResult).join(
        PredictionResult, Transaction.id == PredictionResult.transaction_id
    ).order_by(Transaction.step.asc()).limit(300).all()
    
    if not txs:
        return []
        
    buckets = {}
    for tx, pred in txs:
        bucket_key = f"Hour {(tx.step % 24):02d}:00"
        if bucket_key not in buckets:
            buckets[bucket_key] = {"tx_count": 0, "high_risk": 0, "scores": []}
        buckets[bucket_key]["tx_count"] += 1
        if pred.risk_category == "High Risk":
            buckets[bucket_key]["high_risk"] += 1
        buckets[bucket_key]["scores"].append(pred.risk_score)
        
    out = []
    for k, v in list(buckets.items())[:12]:
        avg_s = sum(v["scores"]) / len(v["scores"]) if v["scores"] else 0.0
        out.append({
            "step_window": k,
            "transaction_count": v["tx_count"],
            "fraud_count": v["high_risk"],
            "high_risk_count": v["high_risk"],
            "avg_risk_score": round(avg_s, 1)
        })
    return out
