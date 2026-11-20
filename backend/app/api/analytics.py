from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.analytics import OverviewStats, TrendDataPoint, RiskDistributionItem
from app.services.analytics_service import get_overview_stats, get_risk_distribution, get_trend_analytics

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/overview", response_model=OverviewStats)
def overview(db: Session = Depends(get_db)):
    return get_overview_stats(db)

@router.get("/risk-distribution")
def risk_distribution(db: Session = Depends(get_db)):
    return get_risk_distribution(db)

@router.get("/trends")
def trends(db: Session = Depends(get_db)):
    return get_trend_analytics(db)
