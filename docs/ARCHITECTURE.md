# RISKWISE AI 2.0 — System Architecture

## Architectural Overview

RISKWISE AI 2.0 is designed as a decoupled, microservices-ready multi-modal fraud detection architecture.

```
[ Financial Ingestion / Payment Gateway ]
                  │
                  ▼
         [ FastAPI REST Gateway ]
         (JWT Auth, RBAC, Rate Limiting)
                  │
         ┌────────┴────────┐
         │                 │
         ▼                 ▼
[ SQLite / PostgreSQL ]  [ Multi-Modal Hybrid Risk Engine ]
(Transactions, Users,    ├── 1. PaySim Preprocessor (Leak-Free Features)
 Prediction Logs,         ├── 2. Supervised XGBoost Classifier (60%)
 Fraud Alerts, Case SAR)  ├── 3. Unsupervised Isolation Forest (25%)
                          ├── 4. Behavioural Typology Heuristics (15%)
                          └── 5. SHAP TreeExplainer Local Attribution
                                   │
                                   ▼
                        [ Composite Risk Score (0-100) ]
                        [ Low: <35 | Medium: 35-65 | High: >=65 ]
                                   │
                                   ▼
         [ React 18 Fintech Dashboard (Tailwind CSS) ]
         ├── Executive Overview & Real-Time Trend Charts
         ├── Live Transaction Inference Studio
         ├── Financial Crime Investigation Dossier
         └── Azure Cloud Infrastructure Operations
```

## Hybrid Model Mathematical Formulation

The composite multi-signal fraud risk index $R \in [0, 100]$ is computed as:

$$R = 100 \cdot \Big( w_{\text{xgb}} \cdot P(\text{fraud} \mid x) + w_{\text{iforest}} \cdot S_{\text{anomaly}}(x) + w_{\text{rules}} \cdot S_{\text{rules}}(x) \Big)$$

Where:
- $w_{\text{xgb}} = 0.60$ (Tuned supervised discriminative weight)
- $w_{\text{iforest}} = 0.25$ (Unsupervised novelty score weight)
- $w_{\text{rules}} = 0.15$ (Deterministic typology heuristic weight)

Decision Boundaries:
- $R < 35$: **Low Risk** -> Action: `ALLOW`
- $35 \le R < 65$: **Medium Risk** -> Action: `REVIEW`
- $R \ge 65$: **High Risk** -> Action: `BLOCK`
