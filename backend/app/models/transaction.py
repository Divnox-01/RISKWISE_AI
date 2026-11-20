from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.session import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    tx_hash = Column(String(64), unique=True, index=True, nullable=False)
    step = Column(Integer, index=True, nullable=False)
    type = Column(String(30), index=True, nullable=False) # TRANSFER, CASH_OUT, PAYMENT, etc.
    amount = Column(Float, nullable=False)
    nameOrig = Column(String(64), index=True, nullable=False)
    oldbalanceOrg = Column(Float, nullable=False)
    newbalanceOrig = Column(Float, nullable=True)
    nameDest = Column(String(64), index=True, nullable=False)
    oldbalanceDest = Column(Float, nullable=False)
    newbalanceDest = Column(Float, nullable=True)
    is_demo_seed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    prediction = relationship("PredictionResult", back_populates="transaction", uselist=False)
    alerts = relationship("FraudAlert", back_populates="transaction")
