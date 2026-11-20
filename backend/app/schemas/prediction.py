from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from .transaction import TransactionBase

class PredictRequest(TransactionBase):
    persist: Optional[bool] = Field(default=True, description="Whether to persist the transaction and prediction result to database")

class RuleFlag(BaseModel):
    rule_id: str
    name: str
    severity: str
    description: str
    score_impact: float

class RuleEvaluation(BaseModel):
    rule_score: float
    rules_triggered_count: int
    flags: List[RuleFlag]
    has_high_severity: bool

class SHAPDriver(BaseModel):
    feature: str
    label: str
    shap_value: float
    feature_value: Any

class SHAPExplanation(BaseModel):
    top_risk_drivers: List[SHAPDriver]
    top_mitigating_factors: List[SHAPDriver]
    all_contributions: Optional[List[SHAPDriver]] = None
    summary_insights: List[str]
    disclaimer: str

class ScoreBreakdown(BaseModel):
    xgb_fraud_probability: float
    xgb_weighted_contribution: float
    isolation_forest_anomaly_score: float
    isolation_forest_weighted_contribution: float
    rule_engine_score: float
    rule_engine_weighted_contribution: float

class PredictResponse(BaseModel):
    tx_hash: Optional[str] = None
    transaction_id: Optional[int] = None
    transaction_data: Dict[str, Any]
    risk_score: float
    risk_category: str # Low Risk, Medium Risk, High Risk
    recommended_action: str # ALLOW, REVIEW, BLOCK
    action_description: str
    score_breakdown: ScoreBreakdown
    rules: RuleEvaluation
    shap_explanation: SHAPExplanation
    engine_mode: str
    alert_created: bool = False
    alert_code: Optional[str] = None
