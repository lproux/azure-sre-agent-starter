# Runbook: Database Failover

## Trigger
- PostgreSQL primary becomes unresponsive
- Replication lag exceeds 30 seconds
- Automated alert: "Database Health Degraded"

## Pre-Checks
1. Confirm the issue is with the primary, not the application
2. Check if failover is already in progress: `az postgres flexible-server show --name <server>`
3. Verify replica health: `az postgres flexible-server replica list --resource-group <rg> --name <server>`

## Failover Procedure

### Automatic Failover (HA-enabled servers)
Azure handles failover automatically. Monitor the process:
```bash
az postgres flexible-server show -g <rg> -n <server> --query "{state:state, haState:highAvailability.state}"
```
Expected failover time: **60-120 seconds**.

### Manual Failover (Forced)
```bash
# Force failover to standby
az postgres flexible-server restart -g <rg> -n <server> --failover Forced

# Monitor progress
watch -n 5 'az postgres flexible-server show -g <rg> -n <server> --query state -o tsv'
```

## Post-Failover Verification
1. Confirm new primary is accepting connections
2. Check application connectivity: review App Insights dependency success rate
3. Verify replication is re-established to new standby
4. Check for data consistency: compare row counts on critical tables

## Rollback
If failover causes worse issues:
1. Force failover again to switch back to original primary
2. If original primary is corrupted, restore from point-in-time backup

## Communication
- Notify: Teams #incidents channel
- Update: Status page if customer-facing
- Timeline: Post-incident review within 48 hours

## Expected Impact
- **Downtime**: 60-120 seconds during failover
- **Data loss**: Zero for synchronous HA; up to replication lag for async
- **Connection reset**: All active connections will be dropped and need reconnection
