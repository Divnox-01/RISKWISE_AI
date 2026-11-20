from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.alert import FraudAlert
from app.models.transaction import Transaction
from app.schemas.alert import AlertResponse, AlertUpdate

def list_alerts(
    db: Session,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> List[AlertResponse]:
    query = db.query(FraudAlert, Transaction).join(Transaction, FraudAlert.transaction_id == Transaction.id)
    
    if status:
        query = query.filter(FraudAlert.status == status)
    if severity:
        query = query.filter(FraudAlert.severity == severity)
        
    results = query.order_by(FraudAlert.created_at.desc()).offset(offset).limit(limit).all()
    
    out = []
    for alert, tx in results:
        out.append(AlertResponse(
            id=alert.id,
            alert_code=alert.alert_code,
            transaction_id=alert.transaction_id,
            prediction_id=alert.prediction_id,
            severity=alert.severity,
            risk_score=alert.risk_score,
            status=alert.status,
            assigned_to=alert.assigned_to,
            created_at=alert.created_at,
            updated_at=alert.updated_at,
            tx_hash=tx.tx_hash,
            amount=tx.amount,
            tx_type=tx.type,
            sender=tx.nameOrig,
            recipient=tx.nameDest
        ))
    return out

def update_alert(db: Session, alert_id: int, update_data: AlertUpdate):
    alert = db.query(FraudAlert).filter(FraudAlert.id == alert_id).first()
    if not alert:
        return None
    if update_data.status:
        alert.status = update_data.status
    if update_data.assigned_to is not None:
        alert.assigned_to = update_data.assigned_to
    db.commit()
    db.refresh(alert)
    return alert
