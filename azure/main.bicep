@description('Environment prefix for all RISKWISE AI 2.0 Azure resources')
param environment string = 'prod'

@description('Azure Region for deployments')
param location string = resourceGroup().location

@description('Unique suffix for globally unique resources like Key Vault and Storage')
param uniqueSuffix string = uniqueString(resourceGroup().id)

var appServicePlanName = 'asp-riskwise-${environment}-${location}'
var backendAppName = 'app-riskwise-backend-${uniqueSuffix}'
var frontendAppName = 'app-riskwise-frontend-${uniqueSuffix}'
var storageAccountName = 'striskwise${take(uniqueSuffix, 8)}'
var keyVaultName = 'kv-riskwise-${take(uniqueSuffix, 8)}'
var logAnalyticsName = 'law-riskwise-${environment}'
var appInsightsName = 'appi-riskwise-${environment}'

// 1. Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// 2. Application Insights
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

// 3. Azure Blob Storage (Model Artifacts & Audit Logs)
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    allowBlobPublicAccess: false
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storageAccount
  name: 'default'
}

resource modelContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobService
  name: 'riskwise-model-artifacts'
  properties: {
    publicAccess: 'None'
  }
}

// 4. Azure Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    enabledForDeployment: true
    enabledForTemplateDeployment: true
    enabledForDiskEncryption: false
    tenantId: subscription().tenantId
    sku: {
      name: 'standard'
      family: 'A'
    }
    enableRbacAuthorization: true
  }
}

// 5. App Service Plan (Linux)
resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: appServicePlanName
  location: location
  kind: 'linux'
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  properties: {
    reserved: true
  }
}

// 6. Backend App Service (FastAPI + ML Pipeline)
resource backendApp 'Microsoft.Web/sites@2022-09-01' = {
  name: backendAppName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.13'
      appCommandLine: 'uvicorn app.main:app --host 0.0.0.0 --port 8000'
      appSettings: [
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
        {
          name: 'AZURE_STORAGE_CONTAINER'
          value: 'riskwise-model-artifacts'
        }
        {
          name: 'DATABASE_URL'
          value: 'sqlite:///./riskwise.db'
        }
      ]
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
}

// 7. Frontend App Service (React Static / Nginx)
resource frontendApp 'Microsoft.Web/sites@2022-09-01' = {
  name: frontendAppName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'NODE|20-lts'
      appCommandLine: 'npx serve -s dist -l 3000'
      appSettings: [
        {
          name: 'VITE_API_URL'
          value: 'https://${backendApp.properties.defaultHostName}/api'
        }
      ]
    }
  }
}

output backendUrl string = 'https://${backendApp.properties.defaultHostName}'
output frontendUrl string = 'https://${frontendApp.properties.defaultHostName}'
output storageAccountName string = storageAccount.name
output keyVaultName string = keyVault.name
