from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from app.database.session import Base

class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True)
    version_tag = Column(String(50), unique=True, index=True, nullable=False)
    algorithm = Column(String(100), nullable=False)
    status = Column(String(30), default="ACTIVE", index=True, nullable=False) # ACTIVE, CANDIDATE, ARCHIVED
    pr_auc = Column(Float, nullable=True)
    roc_auc = Column(Float, nullable=True)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    weights_json = Column(Text, nullable=True)
    training_sample_count = Column(Integer, nullable=True)
    trained_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    deployed_at = Column(DateTime, nullable=True)
