# RISKWISE AI 2.0 — API Reference

Base URL: `http://localhost:8000/api`

### Health
- `GET /health`: System health check, database status, and cloud storage connection status.

### Authentication
- `POST /auth/register`: Register a new user (`email`, `password`, `full_name`, `role`).
- `POST /auth/login`: Authenticate and receive JWT Bearer token.
- `GET /auth/me`: Retrieve current authenticated profile.

### Prediction & Inference
- `POST /predict`: Execute real-time multi-signal inference with SHAP explanation.

### Transactions
- `GET /transactions`: Retrieve paginated transactions ledger.
- `GET /transactions/{id}`: Retrieve detailed transaction by ID.

### Alerts
- `GET /alerts`: Retrieve fraud alerts filtered by `status` and `severity`.
- `PATCH /alerts/{id}`: Update alert status (`OPEN`, `UNDER_INVESTIGATION`, `RESOLVED`, `DISMISSED`).

### Investigations
- `GET /investigations`: List formal investigation cases.
- `POST /investigations`: Open a new investigation dossier.
- `POST /investigations/{id}/notes`: Append analyst findings note.

### Analytics
- `GET /analytics/overview`: Aggregate KPI metrics.
- `GET /analytics/risk-distribution`: Risk tier breakdown.
- `GET /analytics/trends`: Hourly fraud volume trends.

### Model Governance
- `GET /model/metrics`: Performance metrics and feature importances.
- `GET /model/info`: Model metadata and pipeline state.

### Users
- `GET /users`: List registered users (Admin only).
- `PATCH /users/{id}/role`: Update user permissions (Admin only).
