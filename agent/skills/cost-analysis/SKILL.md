# Cost Analysis Guide
# Skill: cost-analysis
# Description: Use when analyzing Azure spend, detecting anomalies, or finding savings
# Tools: RunAzCliReadCommands, AzureResourceGraph, PythonCodeExecution

## Step 1: Current Spend Overview

```bash
# Subscription-level spend this month
az consumption usage list --start-date {{MONTH_START}} --end-date {{TODAY}} --query "[].{service:consumedService, cost:pretaxCost, currency:currency}" -o table

# Spend by resource group
az cost-management query --type ActualCost --timeframe MonthToDate --dataset-aggregation '{"totalCost":{"name":"Cost","function":"Sum"}}' --dataset-grouping '[{"type":"Dimension","name":"ResourceGroupName"}]'
```

## Step 2: Anomaly Detection

```bash
# Compare this week vs last week by service
az consumption usage list --start-date {{THIS_WEEK_START}} --end-date {{TODAY}} --query "[].{service:consumedService, cost:pretaxCost}" -o json > this_week.json
az consumption usage list --start-date {{LAST_WEEK_START}} --end-date {{LAST_WEEK_END}} --query "[].{service:consumedService, cost:pretaxCost}" -o json > last_week.json
```

**Anomaly thresholds**:
| Increase | Classification | Action |
|---|---|---|
| > 50% day-over-day | **CRITICAL** | Investigate immediately |
| > 20% week-over-week | **HIGH** | Review within 24 hours |
| > 10% month-over-month | **MEDIUM** | Include in weekly review |

## Step 3: Idle Resource Detection

```bash
# Find unattached managed disks
az resource graph query -q "Resources | where type == 'microsoft.compute/disks' | where properties.diskState == 'Unattached' | project name, resourceGroup, sku.name, properties.diskSizeGB"

# Find unused public IPs
az resource graph query -q "Resources | where type == 'microsoft.network/publicipaddresses' | where properties.ipConfiguration == '' | project name, resourceGroup, properties.ipAddress"

# Find stopped VMs still incurring disk costs
az resource graph query -q "Resources | where type == 'microsoft.compute/virtualmachines' | where properties.extended.instanceView.powerState.code == 'PowerState/deallocated' | project name, resourceGroup, properties.hardwareProfile.vmSize"

# Find empty App Service plans
az resource graph query -q "Resources | where type == 'microsoft.web/serverfarms' | where properties.numberOfSites == 0 | project name, resourceGroup, sku.name, sku.tier"
```

## Step 4: Rightsizing Recommendations

```bash
# VM rightsizing: check Azure Advisor
az advisor recommendation list --category Cost --query "[?shortDescription.solution == 'Right-size or shutdown underutilized virtual machines'].{vm:resourceMetadata.resourceId, savings:extendedProperties.savingsAmount, currency:extendedProperties.savingsCurrency}" -o table

# Check Azure Monitor for underutilized VMs
az monitor metrics list --resource {{VM_RESOURCE_ID}} --metric "Percentage CPU" --interval PT1H --start-time {{SEVEN_DAYS_AGO}} --aggregation Average --query "value[0].timeseries[0].data[].{time:timeStamp, avgCpu:average}"
```

## Step 5: Reservation & Savings Plan Check

```bash
# Check reservation utilization
az consumption reservation summary list --reservation-order-id {{ORDER_ID}} --grain monthly

# List available RI recommendations
az advisor recommendation list --category Cost --query "[?shortDescription.solution contains 'reservation']"
```

## Step 6: Savings Report

Compile findings into a report:
1. **Total monthly spend**: current vs. previous month
2. **Top 5 cost drivers**: by service and resource group
3. **Quick wins**: idle resources that can be deleted immediately
4. **Rightsizing opportunities**: VMs/databases that can be downsized
5. **Commitment recommendations**: RI/Savings Plan opportunities
6. **Estimated monthly savings**: with confidence level per recommendation
