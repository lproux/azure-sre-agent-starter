# Agent Knowledge: Debugging & Common Issues

## Top 10 Known Issues

### 1. Redis Connection Timeout
- **Symptom**: `StackExchange.Redis.RedisTimeoutException`
- **Cause**: Connection pool exhaustion or network latency
- **Fix**: Increase `syncTimeout` to 5000ms, enable connection multiplexing
- **Last seen**: [DATE]

### 2. AKS Pod OOMKilled
- **Symptom**: Pod restarts, status OOMKilled
- **Cause**: Memory limits too low for workload
- **Fix**: Increase memory limit in deployment YAML, check for memory leaks
- **Typical resources**: API pods need 512Mi-1Gi, Worker pods need 1Gi-2Gi

### 3. PostgreSQL Connection Limit
- **Symptom**: `too many connections for role`
- **Cause**: Connection pool not releasing connections
- **Fix**: Check app connection dispose patterns, reduce pool size per pod

### 4. App Service 503
- **Symptom**: Intermittent 503 errors
- **Cause**: Instance health check failing or plan at capacity
- **Fix**: Check health check endpoint, consider scaling up/out

### 5. Storage Blob Throttling
- **Symptom**: HTTP 503 or 429 from storage operations
- **Cause**: Exceeded storage account throughput limits
- **Fix**: Enable RA-GRS for read distribution, consider multiple storage accounts

### 6. Certificate Expiry
- **Symptom**: TLS handshake failures, browser warnings
- **Cause**: Certificate not renewed before expiry
- **Fix**: Check Key Vault auto-renewal, manually renew if needed

### 7. DNS Resolution Failure in AKS
- **Symptom**: `Name or service not known` from pods
- **Cause**: CoreDNS pod unhealthy or DNS policy misconfigured
- **Fix**: Check CoreDNS pods, verify DNS policy in pod spec

### 8. Deployment Stuck in Pending
- **Symptom**: New pods stay in Pending state
- **Cause**: Insufficient node capacity or PVC binding issue
- **Fix**: Check cluster autoscaler, verify storage class exists

### 9. High APIM Latency
- **Symptom**: API responses > 5 seconds
- **Cause**: Backend pool unhealthy or policy evaluation slow
- **Fix**: Check backend health, review policy expressions

### 10. Function App Cold Start
- **Symptom**: First request after idle takes 10+ seconds
- **Cause**: Consumption plan cold start
- **Fix**: Switch to Premium plan with always-ready instances

## Debugging Tools Quick Reference

| Task | Command/Query |
|------|--------------|
| Check resource health | `az resource graph query -q "HealthResources"` |
| Tail app logs | `az monitor app-insights events show` |
| Check AKS events | `kubectl get events --sort-by=.metadata.creationTimestamp` |
| Query slow requests | App Insights: `requests \| where duration > 5000` |
