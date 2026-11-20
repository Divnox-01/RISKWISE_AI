from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("", response_model=List[TransactionResponse])
def get_transactions(
    limit: int = 50,
    offset: int = 0,
    type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)
    if type:
        query = query.filter(Transaction.type == type.upper())
    records = query.order_by(Transaction.id.desc()).offset(offset).limit(limit).all()
    
    out = []
    for tx in records:
        pred = tx.prediction
        out.append(TransactionResponse(
            id=tx.id,
            tx_hash=tx.tx_hash,
            step=tx.step,
            type=tx.type,
            amount=tx.amount,
            nameOrig=tx.nameOrig,
            oldbalanceOrg=tx.oldbalanceOrg,
            newbalanceOrig=tx.newbalanceOrig,
            nameDest=tx.nameDest,
            oldbalanceDest=tx.oldbalanceDest,
            newbalanceDest=tx.newbalanceDest,
            is_demo_seed=tx.is_demo_seed,
            created_at=tx.created_at,
            risk_score=pred.risk_score if pred else None,
            risk_category=pred.risk_category if pred else None,
            recommended_action=pred.recommended_action if pred else None
        ))
    return out

@router.get("/{id}", response_model=TransactionResponse)
def get_transaction_by_id(id: int, db: Session = Depends(get_db)):
    tx = db.query(Transaction).filter(Transaction.id == id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    pred = tx.prediction
    return TransactionResponse(
        id=tx.id,
        tx_hash=tx.tx_hash,
        step=tx.step,
        type=tx.type,
        amount=tx.amount,
        nameOrig=tx.nameOrig,
        oldbalanceOrg=tx.oldbalanceOrg,
        newbalanceOrig=tx.newbalanceOrig,
        nameDest=tx.nameDest,
        oldbalanceDest=tx.oldbalanceDest,
        newbalanceDest=tx.newbalanceDest,
        is_demo_seed=tx.is_demo_seed,
        created_at=tx.created_at,
        risk_score=pred.risk_score if pred else None,
        risk_category=pred.risk_category if pred else None,
        recommended_action=pred.recommended_action if pred else None
    )
