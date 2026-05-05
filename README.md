# Azure SRE Agent — Complete Starter Kit 🤖

> **Deploy and configure a fully-featured Azure SRE Agent** — Infrastructure-as-Code + 6 custom agents + 5 skills + 8 custom tools + knowledge base + incident response plans + scheduled tasks + connectors + workflow automation. Clone, deploy, configure.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/lproux/azure-sre-agent-starter)

## What's In This Repo

This is not just an infrastructure deployment — it's a **complete, production-ready SRE Agent environment** with 40+ ready-to-use configuration files:

| Category | Count | What You Get |
|----------|-------|-------------|
| 🤖 **Custom Agents** | 6 | Database Expert, AKS Expert, Security Auditor, Deployment Analyzer, Cost Optimizer, Incident Triage |
| 🛠️ **Skills** | 5 | AKS troubleshooting, DB diagnostics, deployment rollback, certificate renewal, cost analysis |
| 🔧 **Custom Tools** | 8 | 4 KQL queries + 3 Python tools + 1 HTTP webhook |
| 📚 **Knowledge Sources** | 11 | Agent memory files + 4 operational runbooks |
| 🔌 **Connectors** | 8 | GitHub, Azure DevOps, PagerDuty, ServiceNow, Teams, Outlook, Datadog, Grafana |
| 🚨 **Incident Response Plans** | 4 | P1-P3 severity routing with agent handoff chains |
| ⏰ **Scheduled Tasks** | 5 | Health checks, cost detection, security review, deploy verification, SLA reports |
| 🌐 **HTTP Triggers** | 2 | Webhook endpoints for Azure Monitor alerts + CI/CD post-deploy verification |
| 🪝 **Hooks** | 2 | Pre-action safety check + post-action audit log |
| 🔄 **Workflows** | 2 | End-to-end incident resolution + daily health with email |
| 📖 **Documentation** | 4 | Setup guide, architecture diagrams, wiki, 250+ FAQ |

---

## 🚀 Quick Start

### Prerequisites
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) + [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- Azure subscription with **Owner** or **User Access Administrator** role
- `Microsoft.App` resource provider registered

### Step 1: Deploy Infrastructure

```bash
git clone https://github.com/lproux/azure-sre-agent-starter.git
cd azure-sre-agent-starter
azd auth login
azd up
```

### Step 2: Create Agent in Portal
1. Go to [sre.azure.com](https://sre.azure.com) → **Create agent**
2. Select the resource group created by `azd up`
3. Start with **Reader** permissions (upgrade later)

### Step 3: Configure Everything Else
Follow the **[Complete Setup Guide](docs/SETUP-GUIDE.md)** — it walks through every capability with copy-paste configs from this repo.

---

## 📁 Repository Structure

```
azure-sre-agent-starter/
├── azure.yaml                              # AZD project configuration
├── infra/                                  # 🏗️ Infrastructure-as-Code
│   ├── main.bicep                          #   Subscription-level deployment
│   ├── main.parameters.json               #   AZD parameter bindings
│   └── modules/
│       └── sre-agent.bicep                 #   Log Analytics + App Insights + UAMI + RBAC
│
├── agent/                                  # 🤖 Agent Configuration (paste into portal)
│   ├── custom-agents/                      #   6 specialist agent YAMLs
│   │   ├── incident-triage.yaml            #     First responder → routes to specialists
│   │   ├── database-expert.yaml            #     SQL, Cosmos DB, PostgreSQL specialist
│   │   ├── aks-expert.yaml                 #     Kubernetes & AKS specialist
│   │   ├── security-auditor.yaml           #     Security posture & compliance
│   │   ├── deployment-analyzer.yaml        #     Deploy verification & rollback
│   │   └── cost-optimizer.yaml             #     FinOps & spend optimization
│   │
│   ├── skills/                             #   5 skill packages (SKILL.md + tool config)
│   │   ├── aks-troubleshooting/SKILL.md
│   │   ├── database-diagnostics/SKILL.md
│   │   ├── deployment-rollback/SKILL.md
│   │   ├── certificate-renewal/SKILL.md
│   │   └── cost-analysis/SKILL.md
│   │
│   ├── tools/                              #   8 custom tools
│   │   ├── kusto/                          #     KQL query tools
│   │   │   ├── error-log-analyzer.kql
│   │   │   ├── performance-baseline.kql
│   │   │   ├── deployment-tracker.kql
│   │   │   └── resource-health-check.kql
│   │   ├── python/                         #     Python custom tools
│   │   │   ├── sla-calculator.py
│   │   │   ├── cost-anomaly-detector.py
│   │   │   └── certificate-expiry-checker.py
│   │   └── http/                           #     HTTP webhook tools
│   │       └── webhook-notifier.py
│   │
│   ├── knowledge/                          #   Agent knowledge persistence
│   │   ├── overview.md                     #     Loaded into every conversation
│   │   ├── team.md                         #     Team members & escalation
│   │   ├── architecture.md                 #     System topology
│   │   ├── deployment.md                   #     CI/CD & rollback procedures
│   │   ├── auth.md                         #     Identity & authentication
│   │   ├── debugging.md                    #     Known issues & fixes
│   │   ├── logs.md                         #     Log sources & queries
│   │   └── runbooks/                       #     Operational runbooks
│   │       ├── database-failover.md
│   │       ├── aks-scaling.md
│   │       ├── app-service-troubleshooting.md
│   │       └── incident-escalation.md
│   │
│   ├── connectors/                         #   8 connector configurations
│   │   ├── github.yaml                     #     Source code + issues
│   │   ├── azure-devops.yaml               #     Repos + wiki + work items
│   │   ├── pagerduty.yaml                  #     Incident platform
│   │   ├── servicenow.yaml                 #     Incident platform (alt)
│   │   ├── teams.yaml                      #     Teams notifications
│   │   ├── outlook.yaml                    #     Email notifications
│   │   ├── datadog-mcp.yaml                #     Datadog via MCP
│   │   └── grafana-mcp.yaml                #     Grafana via MCP
│   │
│   ├── incident-response/                  #   4 incident response plans
│   │   ├── p1-database-critical.yaml
│   │   ├── p1-api-outage.yaml
│   │   ├── p2-performance-degradation.yaml
│   │   └── p3-cost-anomaly.yaml
│   │
│   ├── scheduled-tasks/                    #   5 scheduled automations
│   │   ├── daily-health-check.yaml
│   │   ├── cost-anomaly-detection.yaml
│   │   ├── security-posture-review.yaml
│   │   ├── deployment-verification.yaml
│   │   └── weekly-sla-report.yaml
│   │
│   ├── http-triggers/                      #   2 HTTP webhook triggers
│   │   ├── azure-monitor-alert-handler.yaml
│   │   └── post-deploy-verification.yaml
│   │
│   ├── hooks/                              #   2 safety & governance hooks
│   │   ├── pre-action-safety-check.yaml
│   │   └── post-action-audit-log.yaml
│   │
│   └── workflows/                          #   2 end-to-end workflows
│       ├── incident-to-resolution.yaml
│       └── daily-health-with-email.yaml
│
├── docs/                                   # 📖 Documentation
│   ├── SETUP-GUIDE.md                      #   Complete portal config walkthrough
│   ├── ARCHITECTURE.md                     #   Mermaid architecture diagrams
│   ├── WIKI.md                             #   Full feature wiki
│   └── FAQ.md                              #   250+ FAQ
│
├── README.md                               # This file
├── LICENSE                                 # MIT
└── .gitignore
```

---

## 🤖 Agent Canvas Overview

The custom agents form an **incident triage → specialist handoff** chain:

```
            ┌──────────────────────┐
            │   Incident Platform   │  (PagerDuty / Azure Monitor / ServiceNow)
            └──────────┬───────────┘
                       │
            ┌──────────▼───────────┐
            │   Incident Triage     │  Classifies severity, identifies domain
            │   (First Responder)   │  Routes to appropriate specialist
            └──┬───┬───┬───┬───┬──┘
               │   │   │   │   │
    ┌──────────▼┐ ┌▼────┐ ┌▼──────┐ ┌▼────────┐ ┌▼──────┐
    │ Database   │ │ AKS │ │Security│ │Deployment│ │ Cost  │
    │ Expert     │ │Expert│ │Auditor │ │ Analyzer │ │Optim. │
    └────────────┘ └─────┘ └───────┘ └─────────┘ └───────┘
```

Each specialist has its own tools, skills, and knowledge base access.

---

## ⏰ Automation Schedule

| Task | Schedule | Agent | Mode |
|------|----------|-------|------|
| Security Posture Review | Mon 07:00 UTC | security-auditor | Review |
| Daily Health Check | Daily 08:00 UTC | Main agent | Autonomous |
| Cost Anomaly Detection | Daily 09:00 UTC | cost-optimizer | Autonomous |
| Deployment Verification | Every 30 min | deployment-analyzer | Autonomous |
| Weekly SLA Report | Fri 16:00 UTC | Main agent + Outlook | Autonomous |

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **[Setup Guide](docs/SETUP-GUIDE.md)** | Step-by-step portal configuration for every capability |
| **[Architecture](docs/ARCHITECTURE.md)** | Mermaid diagrams: agent topology, response routing, task timeline |
| **[Complete Wiki](docs/WIKI.md)** | Full service overview, pricing, regions, privacy, models, roles |
| **[FAQ (250+ Questions)](docs/FAQ.md)** | Every question by category |

---

## 💰 What Gets Deployed (Infrastructure)

| Resource | Purpose |
|----------|---------|
| **Resource Group** | Container for all SRE Agent resources |
| **Log Analytics Workspace** | Backing store for telemetry and audit logs |
| **Application Insights** | Agent telemetry, action logging, audit trail |
| **User-Assigned Managed Identity** | Agent authentication (no secrets) |
| **RBAC Role Assignments** | Reader, Log Analytics Reader, Monitoring Reader |

### Cost
- **Always-on**: 4 AAUs/hour/agent (~2,920 AAUs/month)
- **Active flow**: Variable based on token consumption
- See [Pricing Details](https://azure.microsoft.com/en-us/pricing/details/sre-agent/)

---

## 🌍 Supported Regions

| Region | Location | EUDB Compliant |
|--------|----------|----------------|
| East US 2 | United States | N/A |
| Sweden Central | Europe | ✅ Yes |
| Australia East | Asia Pacific | N/A |

---

## 🤝 Contributing

Contributions welcome! Please open an issue or PR. Key areas:
- Additional custom agent templates for new domains
- New skills and runbooks
- Connector configurations for additional platforms
- Kusto/Python tool examples

---

## 📚 Official Resources

| Resource | Link |
|----------|------|
| Portal | [sre.azure.com](https://sre.azure.com) |
| Documentation | [learn.microsoft.com/azure/sre-agent](https://learn.microsoft.com/en-us/azure/sre-agent/) |
| Pricing | [azure.microsoft.com/pricing/details/sre-agent](https://azure.microsoft.com/en-us/pricing/details/sre-agent/) |
| MCP Servers | [mcp.azure.com](https://mcp.azure.com) |

## 📄 License

MIT License — see [LICENSE](LICENSE)
