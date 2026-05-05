# Setup Guide — Complete SRE Agent Environment

> Step-by-step instructions to configure a fully-featured Azure SRE Agent from this repo.
> Infrastructure is deployed via `azd up`. Everything else is configured in the [SRE Agent Portal](https://sre.azure.com).

---

## Table of Contents

1. [Deploy Infrastructure](#1-deploy-infrastructure)
2. [Create the Agent](#2-create-the-agent)
3. [Configure Custom Agents](#3-configure-custom-agents)
4. [Create Skills](#4-create-skills)
5. [Create Custom Tools](#5-create-custom-tools)
6. [Upload Knowledge Base](#6-upload-knowledge-base)
7. [Connect Connectors](#7-connect-connectors)
8. [Connect Incident Platform](#8-connect-incident-platform)
9. [Create Incident Response Plans](#9-create-incident-response-plans)
10. [Create Scheduled Tasks](#10-create-scheduled-tasks)
11. [Configure Run Modes](#11-configure-run-modes)
12. [Test in Playground](#12-test-in-playground)
13. [Verify Everything Works](#13-verify-everything-works)

---

## 1. Deploy Infrastructure

```bash
git clone https://github.com/lproux/azure-sre-agent-starter.git
cd azure-sre-agent-starter
azd auth login
azd up
```

This deploys: Resource Group, Log Analytics, App Insights, Managed Identity, RBAC roles.

---

## 2. Create the Agent

1. Go to [sre.azure.com](https://sre.azure.com) → **Create agent**
2. Select your subscription and the resource group created by `azd up`
3. Name your agent (e.g., `prod-monitoring`)
4. Select region: Sweden Central, East US 2, or Australia East
5. Select the Application Insights created by `azd up`
6. Select resource groups to monitor (add your prod resource groups)
7. Set permission level to **Reader** (start safe, upgrade to Privileged later)
8. Click **Create** → Wait for deployment

**Verify**: Ask `What Azure resources can you see?`

---

## 3. Configure Custom Agents

Create each agent from the YAML files in `agent/custom-agents/`:

For each file (`database-expert.yaml`, `aks-expert.yaml`, `security-auditor.yaml`, `deployment-analyzer.yaml`, `cost-optimizer.yaml`, `incident-triage.yaml`):

1. Go to **Builder** → **Agent Canvas** → **Create** → **Custom Agent**
2. Copy these fields from the YAML file:
   - **Name**: The `name` field
   - **Instructions**: The `system_prompt` field (paste the full text)
   - **Handoff Description**: The `handoff_description` field
3. Under **Built-in Tools**, select the tools listed in `tools:` (e.g., RunAzCliReadCommands, QueryLogAnalytics)
4. Under **Choose Skills**, select skills listed in `allowed_skills:` (after creating them in step 4)
5. Under **Handoff Agents** (for incident-triage only), select the specialist agents
6. Click **Create**

Repeat for all 6 agents. The Agent Canvas should now show all agents connected.

---

## 4. Create Skills

Create each skill from the SKILL.md files in `agent/skills/`:

For each skill folder (`aks-troubleshooting`, `database-diagnostics`, `deployment-rollback`, `certificate-renewal`, `cost-analysis`):

1. Go to **Builder** → **Skills** → **Create Skill**
2. Set the **Name** and **Description** (from the SKILL.md header comments)
3. Upload the `SKILL.md` file as the skill content
4. Under **Tools**, attach the tools mentioned in the SKILL.md header:
   - e.g., `RunAzCliReadCommands`, `RunKubectlCommands`, `QueryLogAnalytics`
5. Click **Create**

---

## 5. Create Custom Tools

### 5a. Kusto Tools (from `agent/tools/kusto/`)

For each `.kql` file:

1. Go to **Builder** → **Agent Canvas** → **Create** → **Tool** → **Kusto Tool**
2. Set the name and description from the file header comments
3. Select your Log Analytics or App Insights connector as the data source
4. Paste the KQL query from the file
5. Parameters use `##paramName##` syntax — they're auto-detected
6. Click **Test** with sample values to verify
7. Click **Create Tool**
8. Attach the tool to the relevant custom agent (e.g., error-log-analyzer → database-expert)

### 5b. Python Tools (from `agent/tools/python/`)

For each `.py` file:

1. Go to **Builder** → **Agent Canvas** → **Create** → **Tool** → **Python Tool**
2. Paste the Python code from the file
3. The `main()` function parameters become the tool's input schema
4. Click **Test** with sample inputs
5. Click **Create Tool**

### 5c. HTTP Tool (from `agent/tools/http/`)

1. Same as Python tools — the webhook-notifier.py uses `requests` to POST
2. Create as a Python tool
3. Attach to incident-triage or notification custom agents

---

## 6. Upload Knowledge Base

### 6a. Agent Knowledge Files (from `agent/knowledge/`)

1. Go to **Settings** → **Knowledge Base** → **Files** tab
2. Drag and drop all files from `agent/knowledge/`:
   - `overview.md` (loaded into every conversation)
   - `team.md`, `architecture.md`, `deployment.md`, `auth.md`, `debugging.md`, `logs.md`
3. Upload runbooks from `agent/knowledge/runbooks/`:
   - `database-failover.md`, `aks-scaling.md`, `app-service-troubleshooting.md`, `incident-escalation.md`
4. Add descriptive tags for each file for better searchability

### 6b. Customize for Your Environment

Edit the knowledge files to match YOUR environment before uploading:
- `overview.md`: Replace `[YOUR_ORG_NAME]`, service names, resource groups
- `team.md`: Replace with your actual team members and escalation paths
- `architecture.md`: Replace with your actual system topology
- `deployment.md`: Replace with your CI/CD pipeline details
- `auth.md`: Replace with your identity setup
- `logs.md`: Replace with your actual workspace names and table schemas

---

## 7. Connect Connectors

Configure each connector from `agent/connectors/`:

### Source Code (pick one or both)
- **GitHub**: Builder → Connectors → + Add → GitHub → OAuth sign-in
- **Azure DevOps**: Builder → Connectors → + Add → Azure DevOps → OAuth sign-in

### Notifications (recommended both)
- **Teams**: Builder → Connectors → + Add → Send notification (Teams) → OAuth sign-in → Select channel
- **Outlook**: Builder → Connectors → + Add → Send email (Outlook) → OAuth sign-in

### Telemetry via MCP (optional, for non-Azure monitoring)
- **Datadog**: Builder → Connectors → + Add → MCP Server → Enter URL + API key
- **Grafana**: Builder → Connectors → + Add → MCP Server → Enter URL + token

**Tool limit**: 80 tools total across all connectors. Monitor the capacity bar.

---

## 8. Connect Incident Platform

> ⚠️ Only ONE incident platform can be active at a time.

### Option A: Azure Monitor (Recommended for Azure-native)
1. Builder → Incident Platform → Connect → Azure Monitor
2. Alerts from managed resource groups flow automatically
3. Enable **Quickstart response plan** for auto-handling Sev0-2

### Option B: PagerDuty
1. Builder → Incident Platform → Connect → PagerDuty
2. Enter PagerDuty API key
3. Select services to monitor
4. Enable Quickstart response plan

### Option C: ServiceNow
1. Builder → Incident Platform → Connect → ServiceNow
2. Enter instance URL and credentials

---

## 9. Create Incident Response Plans

Create each plan from `agent/incident-response/`:

1. Go to **Builder** → **Incident Response Plans** → **New incident response plan**
2. For each YAML file, configure:
   - **Name**: From the `name` field
   - **Incident Filter**: Set severity, impacted service, title contains
   - **Response Custom Agent**: Select the agent from the `response_agent` field
   - **Agent Autonomy Level**: Review or Autonomous as specified
   - **Reinvestigation Cooldown**: Set hours as specified
3. Click **Create**

> ⚠️ Delete the default "quickstart_handler" plan if you create custom plans.

---

## 10. Create Scheduled Tasks

Create each task from `agent/scheduled-tasks/`:

1. Go to **Scheduled Tasks** → **Create scheduled task**
2. For each YAML file:
   - **Task Name**: From the `name` field
   - **Schedule**: Set the cron schedule (Daily at 08:00, etc.)
   - **Response Custom Agent**: Select the agent if specified
   - **Agent Autonomy Level**: As specified in the YAML
   - **Instructions**: Paste the full `instructions:` block
   - **Message Grouping**: `new_thread` or `same_thread` as specified
3. Click **Create**

**Test each task**: Select task → "..." menu → **Run task now**

---

## 11. Configure Run Modes

Run modes are set **per response plan and per scheduled task**, not globally.

| Scenario | Recommended Mode |
|----------|-----------------|
| Production incident response | **Review** (human approves actions) |
| Cost analysis and reporting | **Autonomous** (read-only, safe) |
| Daily health checks | **Autonomous** |
| Security reviews | **Review** (human reviews findings) |
| Post-deployment verification | **Autonomous** (read-only checks) |

To change: Edit the response plan or scheduled task → Change **Agent Autonomy Level**.

---

## 12. Test in Playground

1. Go to **Builder** → **Agent Canvas** → **Test playground**
2. Select a custom agent from the dropdown
3. Test each agent with sample prompts:

| Agent | Test Prompt |
|-------|------------|
| database-expert | "Check the health of our PostgreSQL databases" |
| aks-expert | "Are there any pods in CrashLoopBackOff?" |
| security-auditor | "Review NSGs for overly permissive rules" |
| deployment-analyzer | "Were there any deployments in the last 2 hours?" |
| cost-optimizer | "Find idle resources we could delete" |
| incident-triage | "Classify this alert: High CPU on app-prod-01" |

---

## 13. Verify Everything Works

### Checklist

- [ ] `azd up` deployed infrastructure successfully
- [ ] Agent created and can see your resources
- [ ] All 6 custom agents created in Agent Canvas
- [ ] All 5 skills created with SKILL.md and tool attachments
- [ ] 4 Kusto tools + 3 Python tools + 1 HTTP tool created
- [ ] Knowledge base uploaded (7 knowledge files + 4 runbooks)
- [ ] Source code connector(s) connected (GitHub/ADO)
- [ ] Notification connector(s) connected (Teams/Outlook)
- [ ] Incident platform connected (Azure Monitor/PagerDuty/ServiceNow)
- [ ] 4 incident response plans created
- [ ] 5 scheduled tasks created and tested with "Run now"
- [ ] Run modes configured per plan/task
- [ ] Each custom agent tested in Playground

### Quick Verification Chat

```
What Azure resources can you see?
What custom agents do I have?
Run the daily health check now.
What's in my knowledge base?
```

---

## What's Next

- **Week 1**: Monitor agent investigations, validate response quality
- **Week 2**: Review session insights, add missing runbooks
- **Month 1**: Upgrade trusted tasks from Review → Autonomous
- **Ongoing**: Upload new runbooks, refine skills, add connector tools
