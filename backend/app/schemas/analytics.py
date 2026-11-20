from typing import List, Dict, Any
from pydantic import BaseModel

class OverviewStats(BaseModel):
    total_transactions_analyzed: int
    fraud_transactions_detected: int
    high_risk_transactions: int
    medium_risk_transactions: int
    low_risk_transactions: int
    fraud_detection_rate: float
    average_risk_score: float
    open_alerts_count: int
    active_investigations_count: int

class TrendDataPoint(BaseModel):
    step_window: str
    transaction_count: int
    fraud_count: int
    high_risk_count: int
    avg_risk_score: float

class RiskDistributionItem(BaseModel):
    category: str
    count: int
    percentage: float
