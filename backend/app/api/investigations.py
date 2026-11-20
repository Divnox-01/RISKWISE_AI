from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.investigation import Investigation
from app.schemas.investigation import (
    InvestigationCreate, InvestigationResponse, InvestigationUpdate,
    AnalystNoteCreate, AnalystNoteResponse
)
from app.services.investigation_service import list_investigations, create_investigation, add_analyst_note
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/investigations", tags=["Investigations"])

@router.get("", response_model=List[InvestigationResponse])
def get_investigations(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return list_investigations(db, status=status, priority=priority, limit=limit, offset=offset)

@router.post("", response_model=InvestigationResponse)
def start_investigation(
    data: InvestigationCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_investigation(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}", response_model=InvestigationResponse)
def get_investigation_by_id(id: int, db: Session = Depends(get_db)):
    invs = list_investigations(db, limit=1000)
    target = next((x for x in invs if x.id == id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Investigation not found.")
    return target

@router.post("/{id}/notes", response_model=AnalystNoteResponse)
def add_note(
    id: int,
    data: AnalystNoteCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    note = add_analyst_note(db, id, data, user)
    if not note:
        raise HTTPException(status_code=404, detail="Investigation not found.")
    return note
