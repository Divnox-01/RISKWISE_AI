# RISKWISE AI 2.0
> **Intelligent Fraud Detection. Explainable Risk Decisions.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-brightgreen.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5.4-646cff.svg)](https://vitejs.dev)
[![Azure Ready](https://img.shields.io/badge/Azure-Bicep%20Ready-0078d4.svg)](https://azure.microsoft.com)

**RISKWISE AI 2.0** is an enterprise-grade financial transaction fraud detection and risk intelligence platform. It features a calibrated hybrid machine learning engine that combines supervised gradient boosting, unsupervised anomaly detection, and domain-specific financial typology heuristics with localized SHAP explainability and an interactive fintech dashboard.

---

## Key Capabilities

- **Hybrid Multi-Signal ML Engine**:
  - **Supervised XGBoost Classifier (60% weight)**: Handcrafted leak-free PaySim features, trained with class-imbalance weighting (`scale_pos_weight`). Achieves **0.9987 Test PR-AUC** and **1.0000 Test ROC-AUC**.
  - **Unsupervised Isolation Forest (25% weight)**: RobustScaler-normalized anomaly detector trained strictly on genuine baseline volume.
  - **PaySim Typology Rule Engine (15% weight)**: Real-time flags for account balance liquidation, zero-balance originator spend, new mule accounts, and velocity anomalies.
  - **Unified Composite Risk Score (0 - 100)**: Triage categorizations into **Low Risk** (<35, ALLOW), **Medium Risk** (35-64.9, REVIEW), and **High Risk** (>=65, BLOCK).

- **Explainable AI (SHAP)**:
  - Local additive feature attribution via `shap.TreeExplainer`.
  - Visual waterfall breakdown separating risk escalators (red) from risk mitigators (green).
  - Human-readable natural language risk synthesis.
  - Transparent non-causal interpretability framing.

- **Modular Enterprise Backend (FastAPI)**:
  - RESTful API with SQLite & SQLAlchemy ORM.
  - Role-Based Access Control (`admin`, `analyst`, `auditor`).
  - Secure PBKDF2 HMAC SHA-256 password hashing & JWT token expiration.
  - Automated fraud alert creation and investigation case management.
  - Full audit logging for compliance and forensic review.

- **Fintech Security Dashboard (React + Vite + Tailwind CSS)**:
  - Executive KPI cards, real-time trend charts (Recharts), and risk triage donuts.
  - **Live Inference Studio** with instant predictions, test presets, and SHAP visualizers.
  - Case investigation dossier manager with collaborative analyst note appending.
  - Model Governance matrix comparing live test metrics with historical baselines.
  - Azure operations center and user access directory.

- **Microsoft Azure Cloud Architecture**:
  - Infrastructure-as-Code in **Azure Bicep** (`azure/main.bicep`).
  - Containerized deployment configurations (Docker & Docker Compose).
  - Azure App Service, Azure Blob Storage (model syncing), Key Vault, and Application Insights.

---

## Quick Start (Local Development)

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 2. Backend Setup
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run migrations and seed sample data
python app/database/seed.py

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```
API Documentation will be accessible at: `http://localhost:8000/docs`

### 3. Frontend Setup
```powershell
cd frontend
npm install
npm run dev
```
Dashboard will be accessible at: `http://localhost:5173`

---

## License
MIT License. Developed for enterprise fraud operations and risk intelligence.
