# Agent Knowledge: Logs & Telemetry

## Log Sources

| Source | Workspace | Retention | Key Tables |
|--------|-----------|-----------|------------|
| App Insights (Prod) | log-prod | 90 days | requests, dependencies, exceptions, traces |
| App Insights (Staging) | log-staging | 30 days | Same as prod |
| AKS Container Insights | log-prod | 30 days | ContainerLog, Perf, KubeEvents |
| Azure Activity Log | log-prod | 90 days | AzureActivity |
| NSG Flow Logs | log-network | 30 days | AzureNetworkAnalytics_CL |

## Key Tables & Fields

### Application Insights — requests
```kusto
requests
| where timestamp > ago(1h)
| project timestamp, name, url, resultCode, duration, success, cloud_RoleName
```

### Application Insights — exceptions
```kusto
exceptions
| where timestamp > ago(1h)
| project timestamp, type, outerMessage, innermostMessage, problemId, severityLevel
```

### Container Insights — ContainerLog
```kusto
ContainerLog
| where TimeGenerated > ago(1h)
| where LogEntry contains "error" or LogEntry contains "exception"
| project TimeGenerated, ContainerName, LogEntry
```

### AKS Events
```kusto
KubeEvents
| where TimeGenerated > ago(1h)
| where Level == "Warning" or Level == "Error"
| project TimeGenerated, Name, Namespace, Reason, Message
```

## Useful Query Patterns

### Error Rate Over Time
```kusto
requests
| where timestamp > ago(24h)
| summarize ErrorRate = countif(success == false) * 100.0 / count() by bin(timestamp, 15m)
| render timechart
```

### Dependency Failures
```kusto
dependencies
| where success == false and timestamp > ago(1h)
| summarize Count = count() by target, type, resultCode
| order by Count desc
```

### Resource Utilization (AKS)
```kusto
Perf
| where ObjectName == "K8SContainer"
| where CounterName in ("cpuUsageNanoCores", "memoryRssBytes")
| summarize AvgValue = avg(CounterValue) by InstanceName, CounterName, bin(TimeGenerated, 5m)
```

## Alert Rules

| Alert | Condition | Severity | Action Group |
|-------|-----------|----------|-------------|
| High Error Rate | Error rate > 5% for 5 min | Sev1 | PagerDuty + Teams |
| High Latency | P95 > 3000ms for 10 min | Sev2 | Teams |
| Pod Restarts | RestartCount > 5 in 15 min | Sev2 | Teams |
| Storage Throttling | Throttled requests > 100/min | Sev3 | Email |
