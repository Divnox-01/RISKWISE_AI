import os
import sys
import json
import uuid
from datetime import datetime, timedelta, timezone

# Ensure backend root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database.session import SessionLocal, engine, Base
from app.models.user import User
from app.models.transaction import Transaction
from app.models.prediction import PredictionResult
from app.models.alert import FraudAlert
from app.models.investigation import Investigation
from app.models.note import AnalystNote
from app.models.model_version import ModelVersion
from app.models.audit_log import AuditLog
from app.core.security import get_password_hash
from app.services.prediction_service import get_pipeline

def seed_database():
    print("Initializing and seeding database with demo transactions...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 1. Seed Users if not present
    if db.query(User).count() == 0:
        users = [
            User(
                email="admin@riskwise.ai",
                hashed_password=get_password_hash("Admin@123"),
                full_name="Chief Risk Officer (Admin)",
                role="admin",
                is_active=True
            ),
            User(
                email="analyst@riskwise.ai",
                hashed_password=get_password_hash("Analyst@123"),
                full_name="Sarah Chen (Lead Fraud Analyst)",
                role="analyst",
                is_active=True
            ),
            User(
                email="auditor@riskwise.ai",
                hashed_password=get_password_hash("Auditor@123"),
                full_name="Marcus Vance (Compliance Auditor)",
                role="auditor",
                is_active=True
            )
        ]
        db.add_all(users)
        db.commit()
        print("  -> Seeded 3 default users (admin, analyst, auditor).")

    # 2. Seed Model Versions if not present
    if db.query(ModelVersion).count() == 0:
        m1 = ModelVersion(
            version_tag="v2.0.0-prod",
            algorithm="Hybrid Ensemble (XGBoost 60% + Isolation Forest 25% + Rule Engine 15%)",
            status="ACTIVE",
            pr_auc=0.9994,
            roc_auc=1.0000,
            precision=0.9070,
            recall=1.0000,
            f1_score=0.9512,
            weights_json=json.dumps({"xgb": 0.60, "iforest": 0.25, "rules": 0.15}),
            training_sample_count=10500,
            trained_at=datetime.now(timezone.utc) - timedelta(days=2),
            deployed_at=datetime.now(timezone.utc) - timedelta(days=1)
        )
        m2 = ModelVersion(
            version_tag="v1.2.0-legacy",
            algorithm="Random Forest Single Model",
            status="ARCHIVED",
            pr_auc=0.8240,
            roc_auc=0.9610,
            precision=0.6800,
            recall=0.7900,
            f1_score=0.7300,
            weights_json=json.dumps({"rf": 1.0}),
            training_sample_count=8000,
            trained_at=datetime.now(timezone.utc) - timedelta(days=60),
            deployed_at=datetime.now(timezone.utc) - timedelta(days=58)
        )
        db.add_all([m1, m2])
        db.commit()
        print("  -> Seeded model versions.")

    # 3. Seed 60 Demo Transactions across various steps and typologies
    if db.query(Transaction).count() == 0:
        pipeline = get_pipeline()
        
        # Scenarios:
        # A: High Fraud (High amount transfer, sender balance drained, 0 dest balance)
        # B: Medium Risk (Payment/Transfer with moderate anomaly or new recipient)
        # C: Low Risk Routine (Standard payments, deposits, small transfers)
        
        sample_scenarios = [
            # High Risk Frauds
            {"step": 12, "type": "TRANSFER", "amount": 620000.0, "nameOrig": "C104928371", "oldbalanceOrg": 620000.0, "nameDest": "C902817293", "oldbalanceDest": 0.0},
            {"step": 18, "type": "CASH_OUT", "amount": 480000.0, "nameOrig": "C819283019", "oldbalanceOrg": 490000.0, "nameDest": "C192839102", "oldbalanceDest": 0.0},
            {"step": 34, "type": "TRANSFER", "amount": 310000.0, "nameOrig": "C482910394", "oldbalanceOrg": 310000.0, "nameDest": "C392019485", "oldbalanceDest": 0.0},
            {"step": 45, "type": "CASH_OUT", "amount": 250000.0, "nameOrig": "C918293847", "oldbalanceOrg": 255000.0, "nameDest": "C281938475", "oldbalanceDest": 0.0},
            {"step": 56, "type": "TRANSFER", "amount": 780000.0, "nameOrig": "C718293019", "oldbalanceOrg": 800000.0, "nameDest": "C591827364", "oldbalanceDest": 1200.0},
            {"step": 72, "type": "TRANSFER", "amount": 420000.0, "nameOrig": "C518293018", "oldbalanceOrg": 420000.0, "nameDest": "C192847582", "oldbalanceDest": 0.0},

            # Medium Risk Reviews
            {"step": 20, "type": "TRANSFER", "amount": 85000.0, "nameOrig": "C291823746", "oldbalanceOrg": 150000.0, "nameDest": "C748291029", "oldbalanceDest": 0.0},
            {"step": 28, "type": "CASH_OUT", "amount": 95000.0, "nameOrig": "C381928475", "oldbalanceOrg": 120000.0, "nameDest": "C628193847", "oldbalanceDest": 5000.0},
            {"step": 42, "type": "TRANSFER", "amount": 65000.0, "nameOrig": "C582910293", "oldbalanceOrg": 90000.0, "nameDest": "C918273645", "oldbalanceDest": 0.0},
            {"step": 60, "type": "CASH_OUT", "amount": 75000.0, "nameOrig": "C482918273", "oldbalanceOrg": 80000.0, "nameDest": "C192837465", "oldbalanceDest": 12000.0},
            {"step": 80, "type": "TRANSFER", "amount": 90000.0, "nameOrig": "C918273645", "oldbalanceOrg": 100000.0, "nameDest": "C281938475", "oldbalanceDest": 0.0},

            # Low Risk Routine
            {"step": 5, "type": "PAYMENT", "amount": 142.50, "nameOrig": "C981726354", "oldbalanceOrg": 2450.0, "nameDest": "M192837465", "oldbalanceDest": 0.0},
            {"step": 6, "type": "PAYMENT", "amount": 58.20, "nameOrig": "C482910293", "oldbalanceOrg": 1200.0, "nameDest": "M582910293", "oldbalanceDest": 0.0},
            {"step": 8, "type": "CASH_IN", "amount": 1500.0, "nameOrig": "C582910293", "oldbalanceOrg": 3400.0, "nameDest": "C192837465", "oldbalanceDest": 50000.0},
            {"step": 10, "type": "DEBIT", "amount": 25.00, "nameOrig": "C182736452", "oldbalanceOrg": 540.0, "nameDest": "C281938475", "oldbalanceDest": 4200.0},
            {"step": 15, "type": "PAYMENT", "amount": 320.00, "nameOrig": "C381928374", "oldbalanceOrg": 8900.0, "nameDest": "M381928374", "oldbalanceDest": 0.0},
            {"step": 22, "type": "CASH_IN", "amount": 4200.0, "nameOrig": "C819283746", "oldbalanceOrg": 150.0, "nameDest": "C582910293", "oldbalanceDest": 82000.0},
            {"step": 25, "type": "PAYMENT", "amount": 89.99, "nameOrig": "C291827364", "oldbalanceOrg": 3100.0, "nameDest": "M291827364", "oldbalanceDest": 0.0},
            {"step": 30, "type": "TRANSFER", "amount": 1200.0, "nameOrig": "C491827364", "oldbalanceOrg": 25000.0, "nameDest": "C718293019", "oldbalanceDest": 14000.0},
            {"step": 38, "type": "PAYMENT", "amount": 450.00, "nameOrig": "C591827364", "oldbalanceOrg": 18000.0, "nameDest": "M591827364", "oldbalanceDest": 0.0},
            {"step": 50, "type": "CASH_OUT", "amount": 800.0, "nameOrig": "C691827364", "oldbalanceOrg": 4500.0, "nameDest": "C819283019", "oldbalanceDest": 24000.0},
            {"step": 65, "type": "PAYMENT", "amount": 75.40, "nameOrig": "C791827364", "oldbalanceOrg": 980.0, "nameDest": "M791827364", "oldbalanceDest": 0.0},
            {"step": 70, "type": "DEBIT", "amount": 110.00, "nameOrig": "C891827364", "oldbalanceOrg": 2300.0, "nameDest": "C918293847", "oldbalanceDest": 15000.0},
            {"step": 85, "type": "PAYMENT", "amount": 620.00, "nameOrig": "C991827364", "oldbalanceOrg": 14000.0, "nameDest": "M991827364", "oldbalanceDest": 0.0},
            {"step": 90, "type": "CASH_IN", "amount": 8900.0, "nameOrig": "C102938475", "oldbalanceOrg": 400.0, "nameDest": "C482910394", "oldbalanceDest": 120000.0}
        ]

        # Duplicate and vary to create 50 realistic records
        expanded_scenarios = []
        for i in range(2):
            for s in sample_scenarios:
                var_s = s.copy()
                var_s["step"] = s["step"] + (i * 100)
                var_s["amount"] = round(s["amount"] * (1.0 + (i * 0.05)), 2)
                var_s["nameOrig"] = f"C{uuid.uuid4().int % 900000000 + 100000000}"
                var_s["nameDest"] = f"M{uuid.uuid4().int % 900000000 + 100000000}" if s["type"] == "PAYMENT" else f"C{uuid.uuid4().int % 900000000 + 100000000}"
                expanded_scenarios.append(var_s)

        alerts_created = []
        for tx_data in expanded_scenarios:
            tx_hash = "TX-" + uuid.uuid4().hex[:12].upper()
            
            # Predict
            pred_res = pipeline.predict_transaction(tx_data)
            
            tx_row = Transaction(
                tx_hash=tx_hash,
                step=tx_data["step"],
                type=tx_data["type"],
                amount=tx_data["amount"],
                nameOrig=tx_data["nameOrig"],
                oldbalanceOrg=tx_data["oldbalanceOrg"],
                newbalanceOrig=max(0.0, tx_data["oldbalanceOrg"] - tx_data["amount"]),
                nameDest=tx_data["nameDest"],
                oldbalanceDest=tx_data["oldbalanceDest"],
                newbalanceDest=tx_data["oldbalanceDest"] + tx_data["amount"],
                is_demo_seed=True,
                created_at=datetime.now(timezone.utc) - timedelta(hours=(200 - tx_data["step"]))
            )
            db.add(tx_row)
            db.flush()

            pred_row = PredictionResult(
                transaction_id=tx_row.id,
                risk_score=pred_res["risk_score"],
                risk_category=pred_res["risk_category"],
                recommended_action=pred_res["recommended_action"],
                action_description=pred_res["action_description"],
                xgb_fraud_probability=pred_res["score_breakdown"]["xgb_fraud_probability"],
                isolation_forest_anomaly_score=pred_res["score_breakdown"]["isolation_forest_anomaly_score"],
                rule_engine_score=pred_res["score_breakdown"]["rule_engine_score"],
                rules_triggered_json=json.dumps(pred_res["rules"]),
                shap_explanation_json=json.dumps(pred_res["shap_explanation"]),
                is_demo_mode=False,
                created_at=tx_row.created_at
            )
            db.add(pred_row)
            db.flush()

            if pred_res["risk_score"] >= 35.0:
                severity = "CRITICAL" if pred_res["risk_score"] >= 80.0 else ("HIGH" if pred_res["risk_score"] >= 65.0 else "MEDIUM")
                status = "OPEN" if len(alerts_created) % 2 == 0 else "UNDER_INVESTIGATION"
                alert_code = "ALT-" + uuid.uuid4().hex[:8].upper()
                alert_row = FraudAlert(
                    alert_code=alert_code,
                    transaction_id=tx_row.id,
                    prediction_id=pred_row.id,
                    severity=severity,
                    risk_score=pred_res["risk_score"],
                    status=status,
                    assigned_to="analyst@riskwise.ai" if status == "UNDER_INVESTIGATION" else None,
                    created_at=tx_row.created_at
                )
                db.add(alert_row)
                db.flush()
                alerts_created.append(alert_row)

        db.commit()
        print(f"  -> Seeded {len(expanded_scenarios)} transactions and {len(alerts_created)} fraud alerts.")

        # 4. Seed Investigations for some Under Investigation alerts
        active_alerts = [a for a in alerts_created if a.status == "UNDER_INVESTIGATION"]
        for idx, alt in enumerate(active_alerts[:5]):
            case_no = f"CASE-2026-{idx+1:04d}"
            inv = Investigation(
                case_number=case_no,
                alert_id=alt.id,
                title=f"Typology Review: Large Rapid Balance Liquidation ({alt.alert_code})",
                status="ACTIVE",
                priority="P1" if alt.severity == "CRITICAL" else "P2",
                assigned_analyst="Sarah Chen (Lead Fraud Analyst)",
                findings_summary="Account balance liquidated within single transaction step. Destination recipient appears to be freshly created beneficiary node.",
                created_at=alt.created_at + timedelta(minutes=15)
            )
            db.add(inv)
            db.flush()

            # Add analyst notes
            note1 = AnalystNote(
                investigation_id=inv.id,
                author_name="Sarah Chen",
                author_role="analyst",
                note_text="Triggered initial SAR review. Contacted sender bank verification desk to confirm identity legitimacy.",
                created_at=inv.created_at + timedelta(minutes=30)
            )
            note2 = AnalystNote(
                investigation_id=inv.id,
                author_name="Marcus Vance",
                author_role="auditor",
                note_text="Audit review note: Destination wallet matched external high-risk AML watchlist flag. Holding fund settlement pending escalation.",
                created_at=inv.created_at + timedelta(hours=2)
            )
            db.add_all([note1, note2])

        db.commit()
        print(f"  -> Seeded {min(5, len(active_alerts))} active investigations with multi-stage analyst notes.")

    # 5. Audit Log Entry
    audit = AuditLog(
        user_email="system@riskwise.ai",
        action="DATABASE_SEEDED",
        entity_type="Database",
        details_json=json.dumps({"seeded_at": datetime.now(timezone.utc).isoformat()})
    )
    db.add(audit)
    db.commit()
    db.close()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_database()
