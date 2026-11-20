import json
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog

def record_audit(
    db: Session,
    user_email: str,
    action: str,
    entity_type: str,
    entity_id: str = None,
    details: dict = None,
    ip_address: str = "127.0.0.1"
):
    try:
        log = AuditLog(
            user_email=user_email,
            action=action,
            entity_type=entity_type,
            entity_id=str(entity_id) if entity_id else None,
            details_json=json.dumps(details) if details else None,
            ip_address=ip_address
        )
        db.add(log)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Audit log warning: {e}")
