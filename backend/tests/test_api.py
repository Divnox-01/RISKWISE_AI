import pytest
import os
import sys

# Ensure backend directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app
from app.database.session import SessionLocal
from app.models.user import User

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["service"] == "RISKWISE AI 2.0 API"
    assert data["database"] == "CONNECTED"

def test_auth_flow():
    # Login as seeded admin
    login_res = client.post("/api/auth/login", json={
        "email": "admin@riskwise.ai",
        "password": "Admin@123"
    })
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    token = token_data["access_token"]
    
    # Test /api/auth/me with Bearer token
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["email"] == "admin@riskwise.ai"
    assert me_data["role"] == "admin"

def test_predict_endpoint_high_risk():
    payload = {
        "step": 120,
        "type": "TRANSFER",
        "amount": 750000.0,
        "nameOrig": "C192837465",
        "oldbalanceOrg": 750000.0,
        "nameDest": "C918273645",
        "oldbalanceDest": 0.0,
        "persist": True
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] >= 65.0
    assert data["risk_category"] == "High Risk"
    assert data["recommended_action"] == "BLOCK"
    assert "score_breakdown" in data
    assert "shap_explanation" in data
    assert data["alert_created"] is True

def test_predict_endpoint_low_risk():
    payload = {
        "step": 50,
        "type": "PAYMENT",
        "amount": 45.0,
        "nameOrig": "C819283746",
        "oldbalanceOrg": 5000.0,
        "nameDest": "M192837465",
        "oldbalanceDest": 0.0,
        "persist": False
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] < 35.0
    assert data["risk_category"] == "Low Risk"
    assert data["recommended_action"] == "ALLOW"

def test_transactions_list():
    response = client.get("/api/transactions?limit=10")
    assert response.status_code == 200
    txs = response.json()
    assert len(txs) > 0

def test_alerts_list():
    response = client.get("/api/alerts?limit=10")
    assert response.status_code == 200
    alerts = response.json()
    assert len(alerts) > 0

def test_investigations_list():
    response = client.get("/api/investigations?limit=10")
    assert response.status_code == 200
    invs = response.json()
    assert len(invs) > 0

def test_analytics_endpoints():
    res_ov = client.get("/api/analytics/overview")
    assert res_ov.status_code == 200
    assert res_ov.json()["total_transactions_analyzed"] > 0
    
    res_dist = client.get("/api/analytics/risk-distribution")
    assert res_dist.status_code == 200
    assert len(res_dist.json()) == 3

    res_tr = client.get("/api/analytics/trends")
    assert res_tr.status_code == 200

def test_model_metrics():
    response = client.get("/api/model/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "current_metrics" in data
    assert "historical_reference_metrics" in data
