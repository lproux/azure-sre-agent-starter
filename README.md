# Azure SRE Agent Starter Kit 🤖

> **Deploy an Azure SRE Agent in minutes with `azd up`** — includes comprehensive wiki, FAQ (250+ questions), and Infrastructure-as-Code.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/lproux/azure-sre-agent-starter)

## 🚀 Quick Start

### Prerequisites
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- Azure subscription with **Owner** or **User Access Administrator** role
- `Microsoft.App` resource provider registered

### Deploy in 3 Commands

```bash
# Clone this repo
git clone https://github.com/lproux/azure-sre-agent-starter.git
cd azure-sre-agent-starter

# Login and deploy
azd auth login
azd up
```

You'll be prompted for:
| Parameter | Description | Options |
|-----------|-------------|---------|
| **Environment name** | Used as agent name | e.g., `prod-monitoring` |
| **Region** | Where to deploy | `eastus2`, `swedencentral`, `australiaeast` |

### After Deployment
1. Navigate to [sre.azure.com](https://sre.azure.com)
2. Sign in with your Azure credentials
3. Find your agent and start chatting!

## 📁 Repository Structure

```
azure-sre-agent-starter/
├── azure.yaml                    # AZD project configuration
├── infra/
│   ├── main.bicep               # Main deployment (subscription-level)
│   ├── main.parameters.json     # AZD parameter bindings
│   └── modules/
│       └── sre-agent.bicep      # Agent infrastructure module
├── docs/
│   ├── WIKI.md                  # 📖 Complete Wiki (all features, details)
│   └── FAQ.md                   # ❓ 250+ FAQ organized by category
└── README.md                    # This file
```

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [**Complete Wiki**](docs/WIKI.md) | Full service overview, features, pricing, regions, privacy, models, customization, roles |
| [**FAQ (250+ Questions)**](docs/FAQ.md) | Every question organized by: General, Pricing, Regions, GDPR, Models, Customization, Automation, Integrations, Roles, Memory, Security, Advanced, Use Cases, Troubleshooting, Competitive |
| [**Word Document**](Azure-SRE-Agent-Wiki-FAQ.docx) | Formatted .docx version for offline sharing |

## 💰 What Gets Deployed

| Resource | Purpose |
|----------|---------|
| **Resource Group** | Container for all SRE Agent resources |
| **Log Analytics Workspace** | Backing store for telemetry and audit logs |
| **Application Insights** | Agent telemetry, action logging, audit trail |
| **User-Assigned Managed Identity** | Agent authentication (no secrets to manage) |
| **RBAC Role Assignments** | Reader, Log Analytics Reader, Monitoring Reader |

### Cost
- **Always-on**: 4 AAUs/hour/agent (~2,920 AAUs/month)
- **Active flow**: Variable based on token consumption
- **No free tier** — billing starts at creation
- See [Pricing Details](https://azure.microsoft.com/en-us/pricing/details/sre-agent/)

## 🌍 Supported Regions

| Region | Location | EUDB Compliant (with Azure OpenAI) |
|--------|----------|-------------------------------------|
| East US 2 | United States | N/A |
| Sweden Central | Europe | ✅ Yes |
| Australia East | Asia Pacific | N/A |

## 🔐 Data Privacy

- **Microsoft does NOT use your data to train AI models**
- Data stored in your selected region
- For EU compliance: use **Sweden Central** + **Azure OpenAI** model
- See [full privacy details](docs/WIKI.md#5-data-privacy-gdpr--compliance)

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📚 Official Resources

| Resource | Link |
|----------|------|
| Portal | [sre.azure.com](https://sre.azure.com) |
| Documentation | [learn.microsoft.com/azure/sre-agent](https://learn.microsoft.com/en-us/azure/sre-agent/) |
| Pricing | [azure.microsoft.com/pricing/details/sre-agent](https://azure.microsoft.com/en-us/pricing/details/sre-agent/) |
| GitHub (Official) | [github.com/microsoft/sre-agent](https://github.com/microsoft/sre-agent) |

## 📄 License

MIT License — see [LICENSE](LICENSE)
