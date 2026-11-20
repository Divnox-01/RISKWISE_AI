# ==============================================================================
# RISKWISE AI 2.0 — Automated Azure Deployment Script (PowerShell for Windows 11)
# ==============================================================================

param(
    [string]$ResourceGroupName = "rg-riskwise-ai-prod",
    [string]$Location = "eastus",
    [string]$SubscriptionId = ""
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " RISKWISE AI 2.0 — MICROSOFT AZURE DEPLOYMENT ORCHESTRATOR" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check Azure CLI
Write-Host "`n[1/5] Verifying Azure CLI installation..." -ForegroundColor Yellow
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Error "Azure CLI ('az') is not installed. Install via: winget install Microsoft.AzureCLI"
    exit 1
}
Write-Host "Azure CLI verified." -ForegroundColor Green

# 2. Check Azure Login
Write-Host "`n[2/5] Checking Azure account credentials..." -ForegroundColor Yellow
$account = az account show --output json 2>$null | ConvertFrom-Json
if (-not $account) {
    Write-Host "No active Azure login session. Launching interactive authentication..." -ForegroundColor Cyan
    az login
    $account = az account show --output json | ConvertFrom-Json
}
Write-Host "Active Subscription: $($account.name) ($($account.id))" -ForegroundColor Green

if ($SubscriptionId -ne "") {
    az account set --subscription $SubscriptionId
}

# 3. Create Resource Group
Write-Host "`n[3/5] Creating or confirming resource group '$ResourceGroupName' in '$Location'..." -ForegroundColor Yellow
az group create --name $ResourceGroupName --location $Location --output table

# 4. Deploy Infrastructure as Code (Bicep)
Write-Host "`n[4/5] Deploying Bicep template (App Service, Blob Storage, Key Vault, App Insights)..." -ForegroundColor Yellow
$deployResult = az deployment group create `
    --resource-group $ResourceGroupName `
    --template-file azure/main.bicep `
    --parameters azure/parameters.json `
    --output json | ConvertFrom-Json

$outputs = $deployResult.properties.outputs
Write-Host "Infrastructure deployed successfully!" -ForegroundColor Green
Write-Host "  -> Backend API:      $($outputs.backendUrl.value)" -ForegroundColor Cyan
Write-Host "  -> Frontend App:     $($outputs.frontendUrl.value)" -ForegroundColor Cyan
Write-Host "  -> Blob Storage:     $($outputs.storageAccountName.value)" -ForegroundColor Cyan
Write-Host "  -> Key Vault:        $($outputs.keyVaultName.value)" -ForegroundColor Cyan

# 5. Upload Trained ML Artifacts to Azure Blob Storage
Write-Host "`n[5/5] Synchronizing trained ML artifacts to Azure Blob Storage..." -ForegroundColor Yellow
az storage blob upload-batch `
    --account-name $outputs.storageAccountName.value `
    --destination "riskwise-model-artifacts" `
    --source "backend/artifacts" `
    --auth-mode login `
    --output table

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " RISKWISE AI 2.0 AZURE CLOUD DEPLOYMENT COMPLETED!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
