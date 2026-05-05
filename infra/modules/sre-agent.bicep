// ============================================================================
// Azure SRE Agent — Infrastructure Module
// Deploys: Log Analytics, App Insights, Managed Identity, Container App Agent
// ============================================================================

@description('Name of the SRE Agent')
param agentName string

@description('Azure region')
param location string

@description('Permission level')
@allowed(['Reader', 'Privileged'])
param permissionLevel string

@description('Tags')
param tags object

// ============================================================================
// Log Analytics Workspace (backing store for App Insights)
// ============================================================================
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-${agentName}'
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// ============================================================================
// Application Insights (agent telemetry & audit trail)
// ============================================================================
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-${agentName}'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

// ============================================================================
// User-Assigned Managed Identity (agent authentication)
// ============================================================================
resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-${agentName}'
  location: location
  tags: tags
}

// ============================================================================
// Role Assignments — Core monitoring roles (always assigned)
// ============================================================================

// Reader role on resource group
var readerRoleId = 'acdd72a7-3385-48ef-bd42-f606fba81ae7'
resource readerRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, managedIdentity.id, readerRoleId)
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', readerRoleId)
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Log Analytics Reader
var logAnalyticsReaderRoleId = '73c42c96-874c-492b-b04d-ab87d138a893'
resource logReaderRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, managedIdentity.id, logAnalyticsReaderRoleId)
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', logAnalyticsReaderRoleId)
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Monitoring Reader
var monitoringReaderRoleId = '43d0d8ad-25c7-4714-9337-8ba259a9fe05'
resource monReaderRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, managedIdentity.id, monitoringReaderRoleId)
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', monitoringReaderRoleId)
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// ============================================================================
// Outputs
// ============================================================================
output agentName string = agentName
output appInsightsName string = appInsights.name
output logAnalyticsName string = logAnalytics.name
output managedIdentityId string = managedIdentity.properties.principalId
output managedIdentityClientId string = managedIdentity.properties.clientId
output appInsightsConnectionString string = appInsights.properties.ConnectionString
