# Deployment Rollback Guide
# Skill: deployment-rollback
# Description: Use when a deployment causes issues and rollback is needed
# Tools: RunAzCliReadCommands, RunAzCliWriteCommands, QueryApplicationInsights

## Step 1: Confirm Deployment Correlation

```kusto
// Compare error rates before and after deployment
let deployTime = datetime({{DEPLOY_TIME}});
let beforeWindow = deployTime - 30m;
let afterWindow = deployTime + 30m;
requests
| where timestamp between (beforeWindow .. afterWindow)
| summarize
    ErrorRate = countif(success == false) * 100.0 / count(),
    P95Latency = percentile(duration, 95),
    TotalRequests = count()
  by bin(timestamp, 5m), Phase = iff(timestamp < deployTime, "BEFORE", "AFTER")
| order by timestamp asc
```

**Rollback thresholds**:
- Error rate increase > 5x → **IMMEDIATE ROLLBACK**
- P99 latency increase > 3x → **ROLLBACK**
- New unhandled exception types > 10/min → **ROLLBACK**
- Gradual degradation trend → **PAUSE & INVESTIGATE**

## Step 2: Identify What Changed

```bash
# Container Apps: List revisions
az containerapp revision list --resource-group {{RESOURCE_GROUP}} --name {{APP_NAME}} --query "[].{name:name, active:active, trafficWeight:trafficWeight, createdTime:createdTime}" -o table

# App Service: List deployment slots
az webapp deployment slot list --resource-group {{RESOURCE_GROUP}} --name {{APP_NAME}}

# AKS: Rollout history
kubectl rollout history deployment/{{DEPLOYMENT_NAME}} -n {{NAMESPACE}}
```

## Step 3: Execute Rollback

### Container Apps Rollback
```bash
# Activate previous revision
az containerapp revision activate --resource-group {{RESOURCE_GROUP}} --name {{APP_NAME}} --revision {{PREVIOUS_REVISION}}

# Shift traffic to previous revision
az containerapp ingress traffic set --resource-group {{RESOURCE_GROUP}} --name {{APP_NAME}} --revision-weight {{PREVIOUS_REVISION}}=100

# Deactivate bad revision
az containerapp revision deactivate --resource-group {{RESOURCE_GROUP}} --name {{APP_NAME}} --revision {{BAD_REVISION}}
```

### App Service Rollback (Slot Swap)
```bash
# Swap staging back to production
az webapp deployment slot swap --resource-group {{RESOURCE_GROUP}} --name {{APP_NAME}} --slot staging --target-slot production
```

### AKS Rollback
```bash
# Rollback to previous revision
kubectl rollout undo deployment/{{DEPLOYMENT_NAME}} -n {{NAMESPACE}}

# Or rollback to specific revision
kubectl rollout undo deployment/{{DEPLOYMENT_NAME}} -n {{NAMESPACE}} --to-revision={{REVISION_NUMBER}}

# Verify rollback
kubectl rollout status deployment/{{DEPLOYMENT_NAME}} -n {{NAMESPACE}}
```

### Azure Functions Rollback
```bash
# Redeploy previous package
az functionapp deployment source config-zip --resource-group {{RESOURCE_GROUP}} --name {{APP_NAME}} --src {{PREVIOUS_PACKAGE_URL}}
```

## Step 4: Post-Rollback Verification

```kusto
// Verify error rates are back to baseline
requests
| where timestamp > ago(15m)
| summarize ErrorRate = countif(success == false) * 100.0 / count(),
            P95Latency = percentile(duration, 95),
            RequestCount = count()
  by bin(timestamp, 1m)
| order by timestamp desc
```

```bash
# Verify health endpoint
az rest --method GET --url "https://{{APP_URL}}/health"
```

## Step 5: Post-Incident Actions
1. Document what changed in the deployment
2. Identify root cause of the failure
3. Create a fix in a new branch/PR
4. Add regression tests for the failure mode
5. Update deployment pipeline with the missing check
