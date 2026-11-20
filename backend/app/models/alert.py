from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class FraudAlert(Base):
    __tablename__ = "fraud_alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_code = Column(String(64), unique=True, index=True, nullable=False)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), index=True, nullable=False)
    prediction_id = Column(Integer, ForeignKey("prediction_results.id"), nullable=True)
    severity = Column(String(30), index=True, nullable=False) # CRITICAL, HIGH, MEDIUM, LOW
    risk_score = Column(Float, nullable=False)
    status = Column(String(30), default="OPEN", index=True, nullable=False) # OPEN, UNDER_INVESTIGATION, RESOLVED, DISMISSED
    assigned_to = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    transaction = relationship("Transaction", back_populates="alerts")
    prediction = relationship("PredictionResult", back_populates="alert")
    investigations = relationship("Investigation", back_populates="alert")
