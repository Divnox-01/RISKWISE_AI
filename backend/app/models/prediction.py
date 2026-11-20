from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.session import Base

class PredictionResult(Base):
    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), index=True, nullable=False)
    risk_score = Column(Float, nullable=False, index=True)
    risk_category = Column(String(30), nullable=False, index=True) # Low Risk, Medium Risk, High Risk
    recommended_action = Column(String(30), nullable=False) # ALLOW, REVIEW, BLOCK
    action_description = Column(String(255), nullable=True)
    xgb_fraud_probability = Column(Float, nullable=False)
    isolation_forest_anomaly_score = Column(Float, nullable=False)
    rule_engine_score = Column(Float, nullable=False)
    rules_triggered_json = Column(Text, nullable=True) # JSON array of triggered rules
    shap_explanation_json = Column(Text, nullable=True) # JSON payload of SHAP drivers
    is_demo_mode = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    transaction = relationship("Transaction", back_populates="prediction")
    alert = relationship("FraudAlert", back_populates="prediction", uselist=False)
