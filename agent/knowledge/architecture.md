# Agent Knowledge: Architecture

## System Topology

```
                    ┌─────────────┐
                    │   Azure CDN  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Front Door  │  (WAF + DDoS Protection)
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐ ┌──▼────┐ ┌────▼─────┐
       │ App Service  │ │ APIM  │ │ Static   │
       │ (Web UI)     │ │       │ │ Web App  │
       └──────────────┘ └──┬────┘ └──────────┘
                           │
                    ┌──────▼──────┐
                    │ AKS Cluster  │  (3 node pools)
                    │              │
                    │ ┌──────────┐ │
                    │ │ API Pods │ │
                    │ │ Worker   │ │
                    │ │ Cron     │ │
                    │ └──────────┘ │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐ ┌──▼────────┐ ┌▼───────────┐
       │ PostgreSQL   │ │ Redis     │ │ Storage    │
       │ Flexible     │ │ Enterprise│ │ Account    │
       │ Server       │ │ Cache     │ │ (Blobs)    │
       └─────────────┘ └───────────┘ └────────────┘
```

## Environments

| Environment | Resource Group Pattern | Region | Purpose |
|-------------|----------------------|--------|---------|
| Production | rg-prod-* | East US 2 | Live traffic |
| Staging | rg-staging-* | East US 2 | Pre-production validation |
| Development | rg-dev-* | Sweden Central | Developer testing |
| DR | rg-dr-* | Sweden Central | Disaster recovery |

## Key Dependencies

| Service | Depends On | Failure Impact |
|---------|-----------|----------------|
| Web UI | APIM, CDN | User-facing outage |
| API | PostgreSQL, Redis, Storage | API errors, data loss |
| Worker Pods | PostgreSQL, Service Bus | Background job failures |
| Cron Jobs | PostgreSQL | Scheduled processing stops |

## Network Architecture

- **VNet**: 10.0.0.0/16 with subnets per service
- **AKS Subnet**: 10.0.0.0/20 (Azure CNI)
- **Database Subnet**: 10.0.16.0/24 (delegated)
- **Private Endpoints**: Enabled for PostgreSQL, Redis, Storage
- **NSG**: Default deny inbound, allow only from known subnets
