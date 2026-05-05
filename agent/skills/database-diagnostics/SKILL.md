# Database Diagnostics Guide
# Skill: database-diagnostics
# Description: Use when investigating Azure SQL, Cosmos DB, or PostgreSQL issues
# Tools: RunAzCliReadCommands, QueryApplicationInsights, QueryLogAnalytics

## Step 1: Database Health Check

```bash
# Azure SQL: Check status and DTU usage
az sql db show --resource-group {{RESOURCE_GROUP}} --server {{SERVER_NAME}} --name {{DB_NAME}} --query "{status:status, maxSizeBytes:maxSizeBytes, currentSku:currentSku}"

# Cosmos DB: Check account status
az cosmosdb show --resource-group {{RESOURCE_GROUP}} --name {{ACCOUNT_NAME}} --query "{status:provisioningState, consistencyPolicy:consistencyPolicy.defaultConsistencyLevel}"

# PostgreSQL Flexible Server
az postgres flexible-server show --resource-group {{RESOURCE_GROUP}} --name {{SERVER_NAME}} --query "{state:state, version:version, sku:sku}"
```

## Step 2: Connection Diagnostics

```kusto
// Application Insights: Failed database connections
dependencies
| where type contains "SQL" or type contains "Cosmos" or type contains "PostgreSQL"
| where success == false
| summarize FailCount = count(), AvgDuration = avg(duration) by target, resultCode, bin(timestamp, 5m)
| order by FailCount desc
| take 20
```

```kusto
// Connection pool exhaustion signals
dependencies
| where type contains "SQL"
| summarize P95Duration = percentile(duration, 95), Count = count() by bin(timestamp, 1m)
| where P95Duration > 5000  // > 5 seconds indicates pool pressure
| order by timestamp desc
```

**Common connection issues**:
| Error | Cause | Fix |
|-------|-------|-----|
| Login failed | Wrong credentials or IP not allowlisted | Check connection string, add firewall rule |
| Connection timeout | Pool exhaustion or network issue | Increase pool size, check NSG rules |
| Too many connections | Connection leak | Fix app connection disposal, add pooling |
| SSL/TLS error | Certificate mismatch | Update connection string with correct SSL mode |

## Step 3: Query Performance

```kusto
// Slow queries (Application Insights)
dependencies
| where type contains "SQL"
| where duration > 1000  // > 1 second
| summarize Count = count(), AvgMs = avg(duration), P99Ms = percentile(duration, 99) by data
| order by P99Ms desc
| take 15
```

```bash
# Azure SQL: Top resource-consuming queries
az sql db list-usages --resource-group {{RESOURCE_GROUP}} --server {{SERVER_NAME}} --name {{DB_NAME}}

# Check for blocking queries
az sql db show --resource-group {{RESOURCE_GROUP}} --server {{SERVER_NAME}} --name {{DB_NAME}} --query "currentSku"
```

## Step 4: Capacity Analysis

```bash
# Azure SQL: Check DTU/vCore utilization
az monitor metrics list --resource "/subscriptions/{{SUB_ID}}/resourceGroups/{{RESOURCE_GROUP}}/providers/Microsoft.Sql/servers/{{SERVER_NAME}}/databases/{{DB_NAME}}" --metric "dtu_consumption_percent" --interval PT5M --start-time {{START_TIME}}

# Storage usage
az monitor metrics list --resource "/subscriptions/{{SUB_ID}}/resourceGroups/{{RESOURCE_GROUP}}/providers/Microsoft.Sql/servers/{{SERVER_NAME}}/databases/{{DB_NAME}}" --metric "storage_percent"
```

## Step 5: Replication & HA

```bash
# Check geo-replication status
az sql db replica list-links --resource-group {{RESOURCE_GROUP}} --server {{SERVER_NAME}} --name {{DB_NAME}}

# Cosmos DB: Check replication lag
az cosmosdb show --resource-group {{RESOURCE_GROUP}} --name {{ACCOUNT_NAME}} --query "readLocations"
```

## Step 6: Resolution Patterns

### High DTU/CPU Resolution
1. Identify top queries consuming resources
2. Check for missing indexes: `sys.dm_db_missing_index_details`
3. Review query plans for table scans
4. Consider scaling up tier or adding read replicas

### Connection Failure Resolution
1. Verify firewall rules: `az sql server firewall-rule list`
2. Check VNet service endpoints if using private networking
3. Test connectivity with `az sql db show-connection-string`
4. Review Application Insights for connection pool metrics

### Data Consistency Resolution
1. Check Cosmos DB consistency level matches app requirements
2. Review conflict resolution policy for multi-region writes
3. Verify PostgreSQL replication slot health
4. Check for long-running transactions blocking replication
