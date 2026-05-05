# Azure SRE Agent — Complete Wiki

> **Last updated:** May 2026 | **Portal:** [sre.azure.com](https://sre.azure.com) | **Docs:** [learn.microsoft.com/azure/sre-agent](https://learn.microsoft.com/en-us/azure/sre-agent/)

---

## Table of Contents

1. [Service Overview](#1-service-overview)
2. [Features & Capabilities](#2-features--capabilities)
3. [Pricing & Cost Breakdown](#3-pricing--cost-breakdown)
4. [Regions & Availability](#4-regions--availability)
5. [Data Privacy, GDPR & Compliance](#5-data-privacy-gdpr--compliance)
6. [AI Models](#6-ai-models)
7. [Customization & Extensibility](#7-customization--extensibility)
8. [User Roles & Access Control](#8-user-roles--access-control)
9. [Limitations & Constraints](#9-limitations--constraints)
10. [Network & Prerequisites](#10-network--prerequisites)
11. [Comparisons](#11-comparisons)

---

## 1. Service Overview

### What Is Azure SRE Agent?

Azure SRE Agent is an **AI-powered reliability service** that brings automation and intelligence to Site Reliability Engineering (SRE) practices. It is an always-on AI reliability service that connects to your Azure resources, telemetry, runbooks, and incident tools.

It continuously monitors health, investigates alerts using logs, metrics, and dependency context, and performs **explainable root cause analysis**. The agent recommends or executes mitigations — such as restart, scale, or rollback — within **policy guardrails and human approval**.

### Key Value Propositions

| Value | Description |
|-------|-------------|
| **Reduce MTTR** | Immediate incident acknowledgment, automated correlation, autonomous resolution |
| **Reduce Operational Toil** | Automate health checks, cost anomaly detection, security posture reviews, SLA reporting |
| **Standardize Incident Response** | Consistent response regardless of who is on-call |
| **Institutional Knowledge** | Captures root causes, resolution steps, team preferences — knowledge never leaves |
| **Governance & Auditability** | Full audit trail of every action logged to Application Insights |
| **Progressive Value** | Gets smarter with every interaction over time |

### How It Works

- **Built-in Azure Knowledge**: Pre-configured understanding of Azure services with optimized operational patterns
- **Custom Runbooks**: Execute Azure CLI commands and REST API calls for any Azure service
- **Custom Agent Extensibility**: Build specialized agents for VMs, databases, networking
- **External Integrations**: Connect to monitoring, incident management, and source control via MCP
- **Memory & Learning**: Automatically captures learnings — symptoms, resolution steps, root causes, pitfalls

### Progressive Value Timeline

| Milestone | What Happens |
|-----------|-------------|
| **Day 1** | Connect tools, triage first incident, get immediate diagnostic value |
| **Week 1** | Agent learns environment topology, common failure patterns, escalation preferences |
| **Month 1** | Institutional knowledge compounds. Proactive risk identification, new team member ramp-up |

---

## 2. Features & Capabilities

### 2.1 Azure Service Management

SRE Agent can manage **ALL Azure services** through Azure CLI and REST APIs:

- **Compute**: VMs, App Service, Container Apps, AKS, Azure Functions
- **Storage**: Blob storage, file shares, managed disks, storage accounts
- **Networking**: VNets, load balancers, application gateways, NSGs
- **Databases**: Azure SQL, Cosmos DB, PostgreSQL, MySQL, Redis
- **Monitoring**: Azure Monitor, Log Analytics, Application Insights, Resource Manager

### 2.2 Built-in Tools (No Setup Required)

| Tool | Capabilities |
|------|-------------|
| Azure CLI | Run any `az` command — read and write with safety guardrails |
| Application Insights | Query application telemetry, traces, exceptions |
| Log Analytics | Query Log Analytics workspaces |
| Azure Monitor Metrics | List/query metrics, analyze trends and anomalies |
| Azure Resource Graph | Discover and query any resource across subscriptions |
| AKS Diagnostics | Run kubectl commands, diagnose Kubernetes issues |
| Container Apps | Diagnose Container Apps issues |
| App Service/Functions | Diagnose App Service and Function App issues |
| Code Execution | Python and shell in sandboxed containers |
| Visualization | Generate charts, integrate with Grafana dashboards |
| CPU Profiling | Deeper performance analysis |
| Remediation Actions | Restart, scale, rollback with approval workflows |

### 2.3 Incident Response

When an alert fires, the agent:

1. **Acknowledges** the alert in PagerDuty/ServiceNow/Azure Monitor within seconds
2. **Queries** observability tools — Azure Monitor, App Insights, connected Kusto sources
3. **Correlates** with deployment history (if source control connected)
4. **Checks memory** for similar past issues
5. **Forms hypotheses** and validates each with evidence
6. **Proposes a fix** or resolves autonomously based on run mode

### 2.4 Scheduled Tasks

Proactive monitoring on your schedule. Describe checks in natural language — no scripts needed.

| Use Case | What the Agent Does |
|----------|-------------------|
| Daily Health Check | Reviews resource health, degraded services, findings report |
| Cost Anomaly Detection | Compares spend to baselines, flags unexpected increases |
| Security Posture Review | Checks for misconfigs, expired certificates, open ports |
| Deployment Verification | Verifies recent deployments are healthy |
| SLA Reporting | Generates weekly availability and performance summaries |

### 2.5 Memory & Knowledge System

#### Automatic Learning
After each conversation, the agent captures: symptoms observed, steps that worked, root cause, and pitfalls. This happens **automatically 30 minutes** after a thread goes quiet.

#### Proactive Knowledge Persistence
The agent maintains structured knowledge files:

| File | Content |
|------|---------|
| `overview.md` | Service summary and index (~2,000 chars). Always loaded. |
| `team.md` | Team members, roles, expertise |
| `architecture.md` | Components, connections, environments |
| `logs.md` | Log sources, tables, useful queries |
| `deployment.md` | Pipeline details, rollback procedures |
| `debugging.md` | Common issues, troubleshooting guides |
| `queries/*.md` | Extracted queries organized by topic |

#### User Memories
Commands: `#remember` (save), `#retrieve` (search), `#forget` (remove).

#### Knowledge Base
Upload runbooks, architecture guides, on-call playbooks. **Supported formats:** Markdown, text, PDF, Word, PowerPoint, Excel, images. Max 16 MB/file, up to 1,000 files per custom agent.

### 2.6 Custom Agents (Sub-Agents)

Specialist agents invoked with `/agent` command:

| Pattern | Examples | Use Case |
|---------|----------|----------|
| Domain Expert | VM Expert, AKS Expert, Network Expert | Deep expertise in one technology |
| Task Specialist | Log Analyzer, Cost Optimizer, Security Scanner | Focused tasks |
| Workflow Executor | Incident Triage, Deployment Validator | Multi-step procedures |

### 2.7 Skills

Extend your agent with procedures + execution capabilities. **Automatically loaded** when relevant. Each skill has SKILL.md guidance + optional tool attachments (Azure CLI, Kusto, Python, MCP). Max 5 concurrent.

### 2.8 Workflow Automation

Chain triggers, custom agents, tools, and notifications: **trigger → investigate → act → notify**. Unlike scripts, the agent adapts. Unlike runbooks, it executes. Unlike IFTTT, it investigates before acting.

### 2.9 Execute Mitigations (Actions)

The agent can execute **ANY Azure action** through Azure CLI.

#### Safety Guardrails
- ❌ **Delete operations blocked** — agent never runs delete/remove commands
- ❌ **Key Vault commands blocked** — all `az keyvault` commands blocked
- ✅ **Management locks respected** — ReadOnly-locked resources can't be modified
- ✅ **Subscription validation** — validates GUID format before execution

### 2.10 Elicitation & Human-in-the-Loop

**Yes, SRE Agent has elicitation:**

- **Review Mode (default)**: Agent proposes action, shows Approve/Deny buttons. Only Administrators can approve.
- **Autonomous Mode**: Agent executes immediately without human approval.
- **On-Behalf-Of (OBO)**: When agent lacks permissions, prompts user to authorize temporarily.

### 2.11 Communication & Notifications

- **Teams**: Post findings and updates to channels
- **Outlook Email**: Send investigation summaries with attachments
- **Thread Sharing**: Copy deep links for team collaboration

### 2.12 Audit Trail

Every action logged to Application Insights with **9 custom event types**: AgentResponse, ModelGeneration, AgentToolExecution, AgentExecution, MetaAgent, AgentHandoff, IncidentActivitySnapshot, AgentAzCliExecution, ApprovalDecision. Full KQL queryability.

---

## 3. Pricing & Cost Breakdown

### 3.1 Billing Model

Two components using **Azure Agent Units (AAU)**:

#### Always-On Flow (Fixed)
**4 AAUs per agent per hour**. Billed from creation until deletion. This is the baseline cost regardless of activity.

#### Active Flow (Variable)
Billed when agent is processing: user questions, automation, async operations. Based on LLM tokens consumed per type.

### 3.2 AAU Rates by Model

*Per 1 million tokens (effective April 15, 2026)*:

| Model | Input | Output | Cache Read | Cache Write |
|-------|-------|--------|------------|-------------|
| Claude Opus 4.6 | 100 AAUs | 500 AAUs | 10 AAUs | 125 AAUs |
| GPT 5.3 Codex | 35 AAUs | 280 AAUs | 3.5 AAUs | — |
| GPT 5.2 | 35 AAUs | 280 AAUs | 3.5 AAUs | — |

### 3.3 Cost by Scenario

| Scenario | Input | Output | Cache Read | Cache Write | Claude AAUs | GPT AAUs |
|----------|-------|--------|------------|-------------|-------------|----------|
| Quick question | ~20K | ~2K | ~15K | ~5K | ~3.8 | ~1.6 |
| Incident investigation | ~200K | ~15K | ~150K | ~50K | ~35.5 | ~13.7 |
| Full remediation | ~500K | ~40K | ~400K | ~100K | ~86.5 | ~33.9 |

### 3.4 Monthly Always-On Cost

4 AAUs/hour × 730 hours/month = **2,920 AAUs/month** per agent. Multiply by your region's AAU unit price.

### 3.5 Cost Optimization

| Strategy | Impact |
|----------|--------|
| Add context (skills, knowledge, docs) | Fewer wasted tokens |
| Filter incidents with response plans | Less unnecessary work |
| Batch with scheduled tasks | Fewer runs |
| Test in chat before automating | Avoid wasted runs |
| Stop idle agents | Eliminate active flow (always-on continues) |
| Delete unused agents | Eliminate ALL costs |
| Consolidate workloads | Lower always-on per workload |
| Choose GPT for simple high-volume tasks | Lower per-token cost |

### 3.6 Spending Limits

Set monthly AAU allocation in **Settings > Agent Consumption** (min 500, max 1,000,000). When reached, agent goes idle until next month. Increase anytime to resume immediately.

### 3.7 No Free Tier

No free tier, trial, or Dev/Test AAUs. All usage is pay-as-you-go from creation.

---

## 4. Regions & Availability

### Supported Regions

| Region | Canonical Name | Geographic Area |
|--------|---------------|-----------------|
| East US 2 | `eastus2` | United States |
| Sweden Central | `swedencentral` | Europe |
| Australia East | `australiaeast` | Asia Pacific |

### Key Facts
- **Cross-region access**: Agent can access resources in ANY region where you grant RBAC
- **Single region per agent**: Create separate agents for multi-region
- **Cannot change region** after creation
- **Request new regions** at [github.com/microsoft/sre-agent/issues](https://github.com/microsoft/sre-agent/issues)
- **Pricing may vary by region** — use Azure Pricing Calculator

---

## 5. Data Privacy, GDPR & Compliance

### Data Residency
- All content and conversation history stored in the agent's Azure region
- Data processed and stored within the region selected at creation

### Privacy Guarantees
- ❌ **Microsoft does NOT use your data to train AI models**
- Data used ONLY to provide functionality and improve/debug the service
- Data isolated by tenant and subscription boundaries

### Model Provider Data Residency

| Provider | Processing Location | EU Data Boundary |
|----------|-------------------|------------------|
| Azure OpenAI (GPT) | Within your agent's region | ✅ Covered |
| Anthropic (Claude) | United States | ❌ EXCLUDED |

**⚠️ CRITICAL**: If EUDB compliance is required, use **Azure OpenAI only**. Anthropic sends data to the US.

### Anthropic Data Handling
- Zero data retention policy — prompts/responses not stored after processing
- Governed by Microsoft's enterprise agreements as a subprocessor

### GDPR
- **EU compliance**: Sweden Central + Azure OpenAI = full EUDB
- **Right to erasure**: Delete the agent
- **Data portability**: Audit data via Application Insights KQL
- **Privacy policy**: [microsoft.com/privacy/privacystatement](https://www.microsoft.com/privacy/privacystatement)

---

## 6. AI Models

### Available Models

| Model | Provider | Strengths | Cost |
|-------|----------|-----------|------|
| Claude Opus 4.6 | Anthropic | Thorough investigations, fewer reasoning steps | Higher AAU |
| GPT 5.3 Codex | Azure OpenAI | High-volume tasks, EUDB compliant | Lower AAU |
| GPT 5.2 | Azure OpenAI | Routine tasks, cost-efficient | Lower AAU |

### Model Selection
- **Complex incidents**: Claude Opus (fewer tool calls offsets higher cost)
- **High-volume simple tasks**: GPT models
- **EUDB required**: GPT only
- Change model anytime in **Settings > Basics**

### No Training on Your Data
Neither Microsoft nor Anthropic trains models on your data.

---

## 7. Customization & Extensibility

### 7.1 Runbooks — YES!
- **Knowledge Base Upload**: Markdown, text, PDF, Word, PPT, Excel, images (max 16 MB/file)
- **Skills**: SKILL.md + attached tools (auto-loaded when relevant)
- **Custom Agents**: Domain specialists with own knowledge base (up to 1,000 files)
- **Connectors**: Live ADO wikis or GitHub repos

### 7.2 Custom Tools

| Type | Use Case |
|------|----------|
| Kusto | Predefined KQL queries with parameter substitution |
| Python | Custom functions, 700+ packages, outbound network access |
| Link | URL templates with dynamic parameters |
| HTTP Client | REST API calls with authentication |

### 7.3 Python Execution
- Timeout: 5–900 seconds
- Fresh container per execution
- 700+ packages (pandas, requests, azure-identity, reportlab, etc.)
- Outbound network access enabled
- Managed identity auth (ARM, Key Vault, Storage)
- No GPU, no persistent state

### 7.4 MCP Connectors
Connect to ANY external system. Pre-configured: Datadog, Splunk, New Relic, Dynatrace, Elasticsearch, Grafana. 60-second heartbeats with auto-recovery.

### 7.5 All Connectors

| Category | Connectors |
|----------|-----------|
| Data Sources | Log Analytics, App Insights, Azure Data Explorer (Kusto) |
| Source Code | GitHub (MCP/OAuth), Azure DevOps (OAuth), ADO Wiki |
| Collaboration | Teams, Outlook Email |
| Incident Mgmt | PagerDuty, ServiceNow |
| Custom | Any MCP-compatible server |

### 7.6 Agent Canvas & Playground
Visual builder: Canvas (diagram), Table (list), Test Playground (split-screen + AI evaluation 0–100). VS Code extension for YAML editing.

---

## 8. User Roles & Access Control

### Built-in Roles

| Role | Can Do | Cannot Do |
|------|--------|-----------|
| Reader | View threads, logs, incidents | Chat, request actions |
| Standard User | Chat, diagnostics, request actions | Approve actions, delete resources, modify connectors |
| Administrator | Approve actions, manage connectors, delete resources | — |

### Role Assignments

| Role | Give To |
|------|---------|
| Reader | Auditors, compliance teams, stakeholders |
| Standard User | L1/L2 engineers, first responders |
| Administrator | SRE managers, cloud admins, incident commanders |

### Agent Permissions (Managed Identity)

| Level | Grants | Best For |
|-------|--------|----------|
| Reader | Monitoring roles + reader roles | Read-only diagnostics, OBO for actions |
| Privileged | Monitoring + contributor roles | Full operational access |

### OBO Flow
When managed identity lacks permissions, agent uses YOUR permissions temporarily (Entra OBO). Only Administrators with work/school accounts can authorize.

---

## 9. Limitations & Constraints

- English only in chat interface
- 3 regions only (East US 2, Sweden Central, Australia East)
- Cannot change region after creation
- No free tier / trial / Dev/Test pricing
- Delete operations always blocked
- Key Vault commands always blocked
- Max 5 concurrent active skills
- Max 1,000 files per custom agent KB
- Max 16 MB per uploaded file
- Python: max 900s, no GPU, no persistent state, JSON output only
- Always-on billing continues when stopped (only delete stops billing)
- Anthropic/Claude: data processed in US (not EUDB)
- `*.azuresre.ai` must be allowed through firewall (Zscaler blocks by default)
- WebSocket required for chat
- Agent creator needs Owner/UAA role on subscription
- OBO requires work/school account only

---

## 10. Network & Prerequisites

### Required Domains

| Domain | Purpose |
|--------|---------|
| `*.azuresre.ai` | Portal, API, WebSocket chat |
| `sre.azure.com` | Management portal |
| `portal.azure.com` | Azure portal |
| `api.applicationinsights.io` | App Insights query API |

### Prerequisites

| Requirement | Details |
|-------------|---------|
| Azure Subscription | Active, Microsoft.App registered |
| Permissions | Owner or User Access Administrator |
| Region | East US 2, Sweden Central, or Australia East |
| Network | `*.azuresre.ai` allowed, WebSocket supported |

### Auto-Created Resources
- Application Insights
- Log Analytics Workspace
- User-Assigned Managed Identity

---

## 11. Comparisons

### SRE Agent vs. Traditional Approaches

| Area | Alert Rules | Dashboards | Cron Jobs | SRE Agent |
|------|-------------|------------|-----------|-----------|
| When | After threshold | When you look | On schedule | Before thresholds |
| Shows | Single metric | Raw data | Script output | Correlated findings |
| Context | None | Configured | Script queries | Cross-source + baseline |
| Action | You investigate | You investigate | Script does | Recommends + executes |
| Adapts | Static | Static | Static | Learns over time |

### Skills vs. Custom Agents vs. Knowledge Files

| Feature | Skills | Custom Agents | Knowledge Files |
|---------|--------|---------------|-----------------|
| Access | Automatic | `/agent` command | Automatic |
| Tools | Can attach | Has own tools | No tools |
| Best for | Procedures | Domain specialists | Runbooks, docs |
