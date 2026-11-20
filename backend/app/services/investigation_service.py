import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.investigation import Investigation
from app.models.note import AnalystNote
from app.models.alert import FraudAlert
from app.models.transaction import Transaction
from app.schemas.investigation import (
    InvestigationCreate, InvestigationUpdate, InvestigationResponse,
    AnalystNoteCreate, AnalystNoteResponse
)

def list_investigations(
    db: Session,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> List[InvestigationResponse]:
    query = db.query(Investigation).join(FraudAlert, Investigation.alert_id == FraudAlert.id).join(Transaction, FraudAlert.transaction_id == Transaction.id)
    
    if status:
        query = query.filter(Investigation.status == status)
    if priority:
        query = query.filter(Investigation.priority == priority)
        
    records = query.order_by(Investigation.created_at.desc()).offset(offset).limit(limit).all()
    
    out = []
    for inv in records:
        alert = inv.alert
        tx = alert.transaction if alert else None
        notes_res = [
            AnalystNoteResponse(
                id=n.id,
                author_name=n.author_name,
                author_role=n.author_role,
                note_text=n.note_text,
                created_at=n.created_at
            ) for n in inv.notes
        ]
        out.append(InvestigationResponse(
            id=inv.id,
            case_number=inv.case_number,
            alert_id=inv.alert_id,
            title=inv.title,
            status=inv.status,
            priority=inv.priority,
            assigned_analyst=inv.assigned_analyst,
            findings_summary=inv.findings_summary,
            created_at=inv.created_at,
            updated_at=inv.updated_at,
            notes=notes_res,
            alert_code=alert.alert_code if alert else None,
            risk_score=alert.risk_score if alert else None,
            amount=tx.amount if tx else None,
            tx_hash=tx.tx_hash if tx else None
        ))
    return out

def create_investigation(db: Session, inv_in: InvestigationCreate) -> InvestigationResponse:
    alert = db.query(FraudAlert).filter(FraudAlert.id == inv_in.alert_id).first()
    if not alert:
        raise ValueError("Referenced alert does not exist.")
        
    case_number = "CASE-" + uuid.uuid4().hex[:8].upper()
    inv = Investigation(
        case_number=case_number,
        alert_id=inv_in.alert_id,
        title=inv_in.title,
        priority=inv_in.priority or "P2",
        assigned_analyst=inv_in.assigned_analyst,
        findings_summary=inv_in.findings_summary,
        status="ACTIVE"
    )
    db.add(inv)
    # Update alert status to UNDER_INVESTIGATION
    alert.status = "UNDER_INVESTIGATION"
    db.commit()
    db.refresh(inv)
    
    tx = alert.transaction
    return InvestigationResponse(
        id=inv.id,
        case_number=inv.case_number,
        alert_id=inv.alert_id,
        title=inv.title,
        status=inv.status,
        priority=inv.priority,
        assigned_analyst=inv.assigned_analyst,
        findings_summary=inv.findings_summary,
        created_at=inv.created_at,
        updated_at=inv.updated_at,
        notes=[],
        alert_code=alert.alert_code,
        risk_score=alert.risk_score,
        amount=tx.amount if tx else None,
        tx_hash=tx.tx_hash if tx else None
    )

def add_analyst_note(db: Session, inv_id: int, note_in: AnalystNoteCreate, user) -> AnalystNoteResponse:
    inv = db.query(Investigation).filter(Investigation.id == inv_id).first()
    if not inv:
        return None
    note = AnalystNote(
        investigation_id=inv_id,
        author_name=user.full_name,
        author_role=user.role,
        note_text=note_in.note_text
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return AnalystNoteResponse.from_orm(note)
