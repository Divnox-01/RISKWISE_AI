from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.session import Base

class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(64), unique=True, index=True, nullable=False)
    alert_id = Column(Integer, ForeignKey("fraud_alerts.id"), index=True, nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(String(50), default="ACTIVE", index=True, nullable=False) # ACTIVE, PENDING_REVIEW, CLOSED_CONFIRMED_FRAUD, CLOSED_FALSE_POSITIVE
    priority = Column(String(20), default="P2", index=True, nullable=False) # P1, P2, P3
    assigned_analyst = Column(String(100), nullable=True)
    findings_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    alert = relationship("FraudAlert", back_populates="investigations")
    notes = relationship("AnalystNote", back_populates="investigation", cascade="all, delete-orphan")
