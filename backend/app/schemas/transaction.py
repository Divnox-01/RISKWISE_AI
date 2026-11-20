from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class TransactionBase(BaseModel):
    step: int = Field(..., ge=1, description="Hourly step indicator (1-744)")
    type: str = Field(..., description="Transaction modality: TRANSFER, CASH_OUT, PAYMENT, CASH_IN, DEBIT")
    amount: float = Field(..., gt=0, description="Transaction financial amount in USD")
    nameOrig: str = Field(..., description="Origin customer identifier (e.g., C123456789)")
    oldbalanceOrg: float = Field(..., ge=0, description="Sender balance prior to transaction")
    nameDest: str = Field(..., description="Recipient identifier (e.g., C987654321 or M123456789)")
    oldbalanceDest: float = Field(..., ge=0, description="Recipient balance prior to transaction")
    newbalanceOrig: Optional[float] = None
    newbalanceDest: Optional[float] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    tx_hash: str
    is_demo_seed: bool
    created_at: datetime
    risk_score: Optional[float] = None
    risk_category: Optional[str] = None
    recommended_action: Optional[str] = None

    class Config:
        from_attributes = True
