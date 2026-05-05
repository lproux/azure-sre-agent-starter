# Runbook: App Service Troubleshooting

## Trigger
- HTTP 5xx errors from App Service
- High response latency (P95 > 3 seconds)
- App Service plan at capacity
- Health check failures

## Diagnostic Steps

### Step 1: Check App Status
```bash
az webapp show -g <rg> -n <app> --query "{state:state, hostNames:hostNames, httpsOnly:httpsOnly}"

# Check recent deployment
az webapp deployment list-publishing-profiles -g <rg> -n <app>
```

### Step 2: Check Metrics
```bash
# HTTP errors in last hour
az monitor metrics list --resource <app-resource-id> \
  --metric "Http5xx" --interval PT5M --start-time <1h-ago>

# Response time
az monitor metrics list --resource <app-resource-id> \
  --metric "AverageResponseTime" --interval PT5M --start-time <1h-ago>

# CPU and memory
az monitor metrics list --resource <plan-resource-id> \
  --metric "CpuPercentage,MemoryPercentage" --interval PT5M
```

### Step 3: Check Logs
```bash
# Stream live logs
az webapp log tail -g <rg> -n <app>

# Download recent logs
az webapp log download -g <rg> -n <app> --log-file app-logs.zip
```

## Common Issues & Fixes

### 503 Service Unavailable
1. Check if health check is configured and passing
2. Check instance count: `az webapp show -g <rg> -n <app> --query siteConfig.numberOfWorkers`
3. Restart the app: `az webapp restart -g <rg> -n <app>`
4. If persistent, scale up: `az appservice plan update -g <rg> -n <plan> --sku P2v3`

### High Memory Usage
1. Check for memory leaks in Application Insights profiler
2. Restart to free memory: `az webapp restart -g <rg> -n <app>`
3. Enable auto-heal: configure based on memory threshold

### Deployment Failures
1. Check deployment logs: `az webapp deployment list -g <rg> -n <app>`
2. Verify slot settings: `az webapp config appsettings list -g <rg> -n <app>`
3. Rollback via slot swap if staging is available

### Custom Domain / TLS Issues
1. Check SSL binding: `az webapp config ssl list -g <rg>`
2. Verify domain verification: `az webapp config hostname list -g <rg> -n <app>`
3. Renew certificate if expired

## Auto-Heal Configuration
```bash
az webapp config set -g <rg> -n <app> \
  --auto-heal-enabled true \
  --generic-configurations '{"autoHealRules":{"triggers":{"statusCodes":[{"status":503,"count":10,"timeInterval":"00:05:00"}]},"actions":{"actionType":"Recycle"}}}'
```

## Escalation
- If issue persists after restart + scale: escalate to platform team
- For Azure platform issues: open support ticket with severity B
