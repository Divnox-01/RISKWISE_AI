from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class AlertUpdate(BaseModel):
    status: Optional[str] = None # OPEN, UNDER_INVESTIGATION, RESOLVED, DISMISSED
    assigned_to: Optional[str] = None

class AlertResponse(BaseModel):
    id: int
    alert_code: str
    transaction_id: int
    prediction_id: Optional[int] = None
    severity: str
    risk_score: float
    status: str
    assigned_to: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Nested preview
    tx_hash: Optional[str] = None
    amount: Optional[float] = None
    tx_type: Optional[str] = None
    sender: Optional[str] = None
    recipient: Optional[str] = None

    class Config:
        from_attributes = True
