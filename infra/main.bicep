targetScope = 'subscription'

// ============================================================================
// Azure SRE Agent — AZD Deployment Template
// Deploy with: azd up
// ============================================================================

@description('Name of the SRE Agent (alphanumeric + hyphens, 3-63 chars)')
param agentName string

@description('Azure region for the SRE Agent deployment')
@allowed([
  'eastus2'
  'swedencentral'
  'australiaeast'
])
param location string

@description('Resource group name')
param resourceGroupName string = 'rg-${agentName}'

@description('Permission level for the agent managed identity')
@allowed([
  'Reader'
  'Privileged'
])
param permissionLevel string = 'Reader'

@description('Tags to apply to all resources')
param tags object = {
  'azd-env-name': agentName
  'service': 'sre-agent'
  'deployed-by': 'azd'
}

// ============================================================================
// Resource Group
// ============================================================================
resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
  tags: tags
}

// ============================================================================
// Module: SRE Agent Infrastructure
// ============================================================================
module sreAgent 'modules/sre-agent.bicep' = {
  name: 'sre-agent-${uniqueString(rg.id)}'
  scope: rg
  params: {
    agentName: agentName
    location: location
    permissionLevel: permissionLevel
    tags: tags
  }
}

// ============================================================================
// Outputs
// ============================================================================
output RESOURCE_GROUP string = rg.name
output AGENT_NAME string = sreAgent.outputs.agentName
output AGENT_PORTAL string = 'https://sre.azure.com'
output APP_INSIGHTS_NAME string = sreAgent.outputs.appInsightsName
output LOG_ANALYTICS_NAME string = sreAgent.outputs.logAnalyticsName
output MANAGED_IDENTITY_ID string = sreAgent.outputs.managedIdentityId
output REGION string = location
