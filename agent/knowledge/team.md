# Agent Knowledge: Team

## Team Structure

| Name | Role | Expertise | Timezone | Contact |
|------|------|-----------|----------|---------|
| [Engineer 1] | SRE Lead | AKS, Networking, Incident Command | UTC+0 | @handle |
| [Engineer 2] | Database SRE | PostgreSQL, Cosmos DB, Redis | UTC+1 | @handle |
| [Engineer 3] | Platform Engineer | CI/CD, IaC, App Service | UTC-5 | @handle |
| [Engineer 4] | Security Engineer | IAM, Network Security, Compliance | UTC+0 | @handle |

## On-Call Rotation

- **Primary**: Weekly rotation, Mon 09:00 to Mon 09:00
- **Secondary**: Same schedule, one person behind
- **Schedule**: Managed in PagerDuty, synced to Teams

## Escalation Path

1. **Automated**: SRE Agent triages and investigates (autonomous for P3/P4)
2. **Primary on-call**: Paged via PagerDuty for P1/P2
3. **Secondary on-call**: Auto-escalated after 15 minutes no acknowledgment
4. **Engineering Manager**: Escalated for P0 or after 1 hour unresolved P1
5. **VP Engineering**: Escalated for customer-impacting P0 lasting > 2 hours

## Communication Channels

| Channel | Purpose |
|---------|---------|
| Teams #incidents | Active incident coordination |
| Teams #sre-general | General SRE discussion |
| Teams #deployments | Deployment notifications |
| PagerDuty | Alerting and on-call management |
| Outlook DL: sre-team@ | Non-urgent communications |
