# Agent Knowledge: Overview
# This file is automatically loaded into the agent's system prompt at the start
# of every conversation (~2,000 character budget). Keep it concise.

## Environment Summary

- **Organization**: [YOUR_ORG_NAME]
- **Primary Region**: East US 2 (DR: Sweden Central)
- **Cloud Provider**: Azure (primary), with some on-premises legacy systems
- **Team Size**: [X] engineers across [Y] time zones

## Key Services

| Service | Resource Group | Criticality |
|---------|---------------|-------------|
| API Gateway | rg-prod-api | P0 |
| Web Frontend | rg-prod-web | P0 |
| PostgreSQL DB | rg-prod-data | P0 |
| AKS Cluster | rg-prod-compute | P0 |
| Redis Cache | rg-prod-cache | P1 |
| Azure Functions | rg-prod-functions | P2 |

## Architecture Quick Reference

Frontend (App Service) → API Gateway (APIM) → AKS Cluster → PostgreSQL + Redis

## Knowledge Index

Detailed knowledge files available:
- [team.md](team.md) — Team members, roles, expertise, escalation paths
- [architecture.md](architecture.md) — Full system topology and dependencies
- [deployment.md](deployment.md) — CI/CD pipelines, rollback procedures
- [auth.md](auth.md) — Authentication flows, identity providers
- [debugging.md](debugging.md) — Common issues and troubleshooting guides
- [logs.md](logs.md) — Log sources, key tables, useful queries

## Operational Preferences

- We prefer CLI over portal for changes
- All production changes require peer review
- Escalation: PagerDuty → Teams #incidents → Phone tree
- Post-incident reviews within 48 hours
