# RISKWISE AI 2.0 — Quality Assurance & Testing Report

## Test Summary

All automated tests executed via `pytest backend/tests/test_api.py -v`:
- Total Test Cases: 9
- Passed: 9
- Failed: 0
- Execution Time: ~19.8 seconds

## Test Cases Breakdown

1. `test_health_endpoint`: Verifies `/api/health` returns status `HEALTHY` and confirms database connectivity.
2. `test_auth_flow`: Verifies login with seeded credentials, JWT token generation, and `/api/auth/me` profile resolution.
3. `test_predict_endpoint_high_risk`: Tests transaction liquidation pattern. Asserts Risk Score >= 65, action == BLOCK, SHAP explanation present, and automated FraudAlert created.
4. `test_predict_endpoint_low_risk`: Tests routine payment. Asserts Risk Score < 35, action == ALLOW.
5. `test_transactions_list`: Verifies transaction retrieval and pagination.
6. `test_alerts_list`: Verifies fraud alert queue retrieval and severity mapping.
7. `test_investigations_list`: Verifies case dossiers and analyst notes.
8. `test_analytics_endpoints`: Validates overview KPIs, risk distributions, and trend data.
9. `test_model_metrics`: Confirms serialized metrics, feature rankings, and historical comparisons.
