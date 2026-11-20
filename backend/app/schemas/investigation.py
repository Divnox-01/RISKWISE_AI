from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class AnalystNoteCreate(BaseModel):
    note_text: str

class AnalystNoteResponse(BaseModel):
    id: int
    author_name: str
    author_role: str
    note_text: str
    created_at: datetime

    class Config:
        from_attributes = True

class InvestigationCreate(BaseModel):
    alert_id: int
    title: str
    priority: Optional[str] = "P2"
    assigned_analyst: Optional[str] = None
    findings_summary: Optional[str] = None

class InvestigationUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_analyst: Optional[str] = None
    findings_summary: Optional[str] = None

class InvestigationResponse(BaseModel):
    id: int
    case_number: str
    alert_id: int
    title: str
    status: str
    priority: str
    assigned_analyst: Optional[str] = None
    findings_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    notes: List[AnalystNoteResponse] = []
    
    # Associated alert & tx summary
    alert_code: Optional[str] = None
    risk_score: Optional[float] = None
    amount: Optional[float] = None
    tx_hash: Optional[str] = None

    class Config:
        from_attributes = True
