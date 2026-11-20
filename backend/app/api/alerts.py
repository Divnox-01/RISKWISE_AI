from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.alert import AlertResponse, AlertUpdate
from app.services.alert_service import list_alerts, update_alert

router = APIRouter(prefix="/alerts", tags=["Fraud Alerts"])

@router.get("", response_model=List[AlertResponse])
def get_alerts(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return list_alerts(db, status=status, severity=severity, limit=limit, offset=offset)

@router.patch("/{id}")
def modify_alert(
    id: int,
    data: AlertUpdate,
    db: Session = Depends(get_db)
):
    alert = update_alert(db, id, data)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found.")
    return {"message": "Alert updated successfully", "alert_id": alert.id, "status": alert.status}
