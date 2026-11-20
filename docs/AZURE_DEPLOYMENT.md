# RISKWISE AI 2.0 — Microsoft Azure Deployment Guide

## Architecture Components

1. **Azure App Service (Linux)**: Hosts FastAPI backend container and React frontend static site.
2. **Azure Blob Storage**: Manages serialized ML models (`xgb_fraud_model.joblib`, `iso_forest_model.joblib`, `scaler.joblib`) in container `riskwise-model-artifacts`.
3. **Azure Key Vault**: Stores `JWT_SECRET_KEY` and connection strings with RBAC managed identity.
4. **Application Insights & Log Analytics**: Captures request telemetry, model inference latency, and exception logs.

## Deployment Instructions

Execute the automated PowerShell deployment script from the project root:
```powershell
.\azure\deploy_azure.ps1 -ResourceGroupName "rg-riskwise-ai-prod" -Location "eastus"
```
