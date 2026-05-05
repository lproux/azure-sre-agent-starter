# Azure SRE Agent — FAQ (250+ Questions)

> Organized by category. All answers sourced from official Microsoft documentation.

---

## Table of Contents

1. [General / Overview](#1-general--overview)
2. [Pricing & Billing](#2-pricing--billing)
3. [Regions & Data Residency](#3-regions--data-residency)
4. [Privacy, GDPR & Compliance](#4-privacy-gdpr--compliance)
5. [AI Models & Capabilities](#5-ai-models--capabilities)
6. [Customization & Runbooks](#6-customization--runbooks)
7. [Automation & Actions](#7-automation--actions)
8. [Integrations](#8-integrations)
9. [Access Control & Roles](#9-access-control--roles)
10. [Memory, Knowledge & Learning](#10-memory-knowledge--learning)
11. [Security & Governance](#11-security--governance)
12. [Advanced Scenarios](#12-advanced-scenarios)
13. [Use Cases & Scenarios](#13-use-cases--scenarios)
14. [Troubleshooting](#14-troubleshooting)
15. [Competitive & Positioning](#15-competitive--positioning)
16. [Miscellaneous](#16-miscellaneous)

---

## 1. General / Overview

**Q: What is Azure SRE Agent?**
A: An AI-powered reliability service that helps operations teams monitor, diagnose, and resolve issues in Azure-hosted applications.

**Q: Is Azure SRE Agent Generally Available (GA)?**
A: Azure SRE Agent is available for deployment. Check the Azure product page for current status.

**Q: What is the service URL?**
A: sre.azure.com

**Q: Do I need to install anything?**
A: No. Browser-based at sre.azure.com. VS Code extension is optional.

**Q: Can I use it for non-Azure resources?**
A: Built-in tools are Azure-focused, but Python tools and MCP connectors can reach any system.

**Q: Is it a chatbot or autonomous agent?**
A: Both. Interactive chat + autonomous incident response + scheduled tasks.

**Q: What makes it different from Azure Monitor?**
A: Azure Monitor collects data. SRE Agent reasons about it, correlates sources, remembers past incidents, proposes/executes actions.

**Q: What makes it different from PagerDuty/ServiceNow?**
A: Those are incident platforms. SRE Agent integrates WITH them and adds AI investigation + automated remediation.

**Q: Can SRE Agent replace on-call engineers?**
A: It augments, not replaces. Handles triage and known fixes. Complex/novel issues need humans.

**Q: How long to set up?**
A: ~5 minutes to create an agent and grant resource access.

**Q: Does it work with Azure Government?**
A: Currently available in East US 2, Sweden Central, Australia East only.

**Q: Can I use it with Azure Stack?**
A: Designed for Azure public cloud. Stack Hub/HCI not directly supported.

**Q: Is there an SLA?**
A: Check Azure SLA pages for current commitments.

**Q: What resource provider does it use?**
A: Microsoft.App. Register with: `az provider register --namespace Microsoft.App`

**Q: Can I try before committing?**
A: No free tier, but create an agent, test briefly, delete to minimize costs.

---

## 2. Pricing & Billing

**Q: What is an Azure Agent Unit (AAU)?**
A: Standardized consumption unit for agentic work across Azure agents.

**Q: What are the two billing components?**
A: Always-on (4 AAUs/agent/hour, fixed) and active flow (variable, token-based).

**Q: How is always-on calculated?**
A: 4 AAUs per hour per agent, continuously from creation to deletion.

**Q: How is active flow calculated?**
A: Tokens consumed metered by type (input, output, cache read, cache write) at model-specific rates.

**Q: Am I billed when the agent waits for my response?**
A: No. Only active processing time counts.

**Q: What counts as active flow?**
A: Interactive prompts, automation triggers, async operations.

**Q: Is pricing the same in all regions?**
A: AAU unit prices may vary by region. Check Azure Pricing Calculator.

**Q: Is there a free tier?**
A: No. Charges begin at creation. No trial or Dev/Test pricing.

**Q: Can I set a spending limit?**
A: Yes. 500-1,000,000 AAUs/month in Settings > Agent Consumption.

**Q: What happens at the spending limit?**
A: Agent goes idle. Always-on billing continues. Resets next month.

**Q: Can I increase limits mid-month?**
A: Yes, immediate effect. Chat/actions resume right away.

**Q: Can I decrease limits mid-month?**
A: Yes, but takes effect next month if below current usage.

**Q: What if I stop my agent?**
A: Active flow stops. Always-on cost CONTINUES. Only delete stops all billing.

**Q: What if I delete my agent?**
A: ALL billing stops immediately.

**Q: Can one agent handle multiple workloads?**
A: Yes. Consolidating reduces always-on costs.

**Q: Does model choice affect cost?**
A: Yes. Claude Opus has higher rates but may need fewer steps. GPT is cheaper per token.

**Q: How do I monitor costs?**
A: Settings > Agent Consumption, or Microsoft Cost Management in Azure portal.

**Q: Monthly always-on cost?**
A: 2,920 AAUs/month per agent (4 x 730 hours).

**Q: Can I get volume discounts?**
A: Contact your Microsoft account team.

**Q: Does task frequency affect cost?**
A: Yes. More frequent = more AAUs. Batch tasks to optimize.

---

## 3. Regions & Data Residency

**Q: Which regions are available?**
A: East US 2, Sweden Central, Australia East.

**Q: Can I deploy to multiple regions?**
A: Each agent is single-region. Create separate agents per region.

**Q: Can I change region after creation?**
A: No. Create a new agent.

**Q: Can I request a new region?**
A: Yes, at github.com/microsoft/sre-agent/issues.

**Q: Can my agent access other-region resources?**
A: Yes. Agent region = compute location. RBAC controls resource access.

**Q: Where is data stored?**
A: In the agent's Azure region.

**Q: Does data leave my region?**
A: Azure OpenAI: stays in region. Anthropic: sent to US.

**Q: Which region for EU compliance?**
A: Sweden Central + Azure OpenAI.

**Q: Is there a Middle East / UK region?**
A: Not currently. Submit region requests.

---

## 4. Privacy, GDPR & Compliance

**Q: Does Microsoft use my data to train models?**
A: No.

**Q: Does Anthropic use my data to train models?**
A: No. Zero data retention policy.

**Q: Is SRE Agent GDPR compliant?**
A: Yes (Sweden Central + Azure OpenAI = full EUDB compliance).

**Q: What about EU Data Boundary?**
A: Azure OpenAI = covered. Anthropic = EXCLUDED (US processing).

**Q: Can I achieve data sovereignty?**
A: Yes — Sweden Central + Azure OpenAI.

**Q: How is tenant data isolated?**
A: By tenant and subscription boundaries.

**Q: Can I export data?**
A: Audit data via App Insights KQL. Conversations in agent portal.

**Q: Right to erasure?**
A: Delete the agent.

**Q: Is there a DPA?**
A: Yes, Microsoft standard enterprise agreements.

**Q: Who is the data processor?**
A: Microsoft. Anthropic is a subprocessor.

**Q: Does the agent store PII?**
A: Stores conversation history. If resources contain PII, it may appear in conversations.

**Q: Can I use it in regulated industries?**
A: Depends on requirements. Azure OpenAI + appropriate region provides strongest posture.

**Q: SOC 2 compliance?**
A: Check Microsoft compliance offerings.

**Q: What happens to data on deletion?**
A: All agent data deleted.

**Q: Can I disable data collection?**
A: Agent needs data to function. Control access via RBAC.

---

## 5. AI Models & Capabilities

**Q: What models are available?**
A: Claude Opus 4.6 (Anthropic), GPT 5.3 Codex (Azure OpenAI), GPT 5.2 (Azure OpenAI).

**Q: Which model is best?**
A: Claude Opus for complex investigations. GPT for high-volume simple tasks + EUDB.

**Q: Can I change model after creation?**
A: Yes, anytime in Settings > Basics.

**Q: Can I bring my own model?**
A: No. Choose from available models only.

**Q: Does the model have internet access?**
A: Accesses your Azure resources and connected systems. No general browsing.

**Q: How does it learn my environment?**
A: Memory (auto-learning), knowledge base (uploads), skills (procedures).

**Q: Is the model fine-tuned for Azure?**
A: Built-in Azure knowledge + optimized patterns. Not custom fine-tuned per customer.

**Q: What about context window?**
A: Determined by underlying model. Service manages prompt caching.

**Q: Can the model hallucinate?**
A: Yes, like all LLMs. Review mode provides oversight. Agent grounds in your data with citations.

**Q: How do I validate recommendations?**
A: Review mode — agent proposes with evidence, you approve/deny.

**Q: Can I use multiple models simultaneously?**
A: One model per agent. Create multiple agents to compare.

---

## 6. Customization & Runbooks

**Q: Can I add runbooks?**
A: YES. Upload to Knowledge Base, create Skills, or build Custom Agents with their own KB.

**Q: What formats are supported?**
A: Markdown, text, PDF, Word, PPT, Excel, images. Max 16 MB/file.

**Q: How many files can I upload?**
A: Up to 1,000 files per custom agent. 50 MB/file for custom agent KB.

**Q: Can the agent execute runbooks automatically?**
A: Yes. Skills combine guidance with executable tools.

**Q: Can I create custom agents?**
A: Yes. Builder > Agent Canvas with system prompt, tools, handoffs, KB.

**Q: Can custom agents call each other?**
A: Yes. Handoff chains.

**Q: Can I test before deploying?**
A: Yes. Agent Canvas > Test Playground with AI evaluation (0-100).

**Q: Can I create custom Kusto tools?**
A: Yes. Predefined KQL with parameter substitution.

**Q: Can I write Python tools?**
A: Yes. Custom functions, 700+ packages, outbound network.

**Q: What Python packages are available?**
A: 700+ including pandas, requests, azure-identity, reportlab.

**Q: Can Python tools access Azure resources?**
A: Yes. Managed identity auth for ARM, Key Vault, Storage.

**Q: Can Python tools call external APIs?**
A: Yes. Outbound network enabled.

**Q: Can I use MCP connectors?**
A: Yes. Any MCP-compatible server.

**Q: Can I connect my own MCP server?**
A: Yes. Streamable-HTTP (remote) or stdio (local).

**Q: Can I edit in VS Code?**
A: Yes. SRE Agent MCP server extension syncs YAML changes.

**Q: What is the Agent Canvas?**
A: Visual builder with Canvas, Table, and Test Playground views.

**Q: Can I import/export configs?**
A: Custom agents use YAML definitions.

**Q: Can I version configs?**
A: Via Git with YAML in source control.

**Q: Can skills use MCP tools?**
A: Yes. Skills attach MCP, Azure CLI, Kusto, Python tools.

---

## 7. Automation & Actions

**Q: How much can I automate?**
A: Anything via Azure CLI + Python tools + MCP + HTTP endpoints.

**Q: Can it restart services?**
A: Yes. With appropriate permissions + run mode approval.

**Q: Can it scale resources?**
A: Yes. Any az command.

**Q: Can it rollback deployments?**
A: Yes, with source control connected.

**Q: Can it create resources?**
A: Yes, with Privileged permissions or OBO.

**Q: Can it delete resources?**
A: NO. Delete/remove commands are BLOCKED. Use Azure portal.

**Q: Can it modify Key Vault?**
A: NO. All az keyvault commands blocked.

**Q: What about management locks?**
A: Respected. ReadOnly-locked resources can't be modified.

**Q: Can it run kubectl?**
A: Yes. Built-in AKS diagnostics.

**Q: Can it query App Insights?**
A: Yes. Built-in, no connector needed.

**Q: Can it query Log Analytics?**
A: Yes. Built-in. Connector adds persistent awareness.

**Q: Can it query Kusto (ADX)?**
A: Yes, via connector with auto-schema learning.

**Q: Can it send emails?**
A: Yes, with Outlook connector.

**Q: Can it post to Teams?**
A: Yes, with Teams connector.

**Q: Can it create GitHub issues?**
A: Yes, with GitHub MCP connector.

**Q: Can it create ADO work items?**
A: Yes, with ADO connector.

**Q: Can it trigger GitHub Actions?**
A: Yes, through workflow automation.

**Q: Can it trigger Azure Pipelines?**
A: Yes, through Azure CLI or custom integrations.

**Q: What are response plans?**
A: Filters controlling which incidents the agent handles.

**Q: Review vs Autonomous mode?**
A: Review = propose + human approve. Autonomous = execute immediately.

**Q: Different modes per task?**
A: Yes. Per response plan and per scheduled task.

**Q: What if autonomous mode makes a mistake?**
A: Full audit trail. Management locks protect critical resources. Deletes always blocked.

**Q: Can I schedule tasks?**
A: Yes. Natural language descriptions, cron or human-readable schedules.

**Q: Can I edit scheduled tasks?**
A: Yes. Schedule, instructions, agent, date range, run limit, autonomy level.

**Q: Does it support cron?**
A: Yes. Human-readable AND cron expressions.

**Q: Can scheduled tasks send emails?**
A: Yes. Custom agent + Outlook connector + scheduled trigger.

**Q: Can I chain multiple custom agents?**
A: Yes. Handoff chains for multi-step workflows.

---

## 8. Integrations

**Q: Which monitoring tools?**
A: Azure Monitor (built-in), App Insights (built-in), Log Analytics (built-in), Grafana, Datadog, Splunk, New Relic, Dynatrace, Elasticsearch (via MCP).

**Q: Which incident platforms?**
A: PagerDuty, ServiceNow, Azure Monitor Alerts.

**Q: Which source control?**
A: GitHub (repos, issues, PRs, wikis), Azure DevOps (repos, work items, wikis).

**Q: Jira?**
A: Not native. Custom MCP connector possible.

**Q: Slack?**
A: Not native. Teams is supported. Custom MCP possible.

**Q: OpsGenie?**
A: Check MCP availability or build custom.

**Q: Prometheus?**
A: Via custom MCP connector or Python tool.

**Q: Grafana?**
A: Yes, listed as supported integration.

**Q: On-premises monitoring?**
A: Yes, via Python tools with network access or MCP.

**Q: How to set up connectors?**
A: Builder > Connectors. Admins only.

**Q: Multiple PagerDuty services?**
A: Yes, multiple response plans.

**Q: OAuth authentication?**
A: Yes. GitHub OAuth, ADO OAuth connectors.

**Q: Managed identity auth?**
A: Yes. Kusto/ADX connectors use managed identity.

---

## 9. Access Control & Roles

**Q: Who can create an agent?**
A: Owner or User Access Administrator on the subscription.

**Q: Who gets admin by default?**
A: The creator.

**Q: Can I invite external users?**
A: Yes. Added as Entra ID guest users.

**Q: Can I assign roles via CLI?**
A: Yes. `az role assignment create --role 'SRE Agent Standard User' --assignee user@company.com --scope <id>`

**Q: Can Standard Users approve actions?**
A: No. Administrators only.

**Q: Can personal Microsoft accounts use OBO?**
A: No. Work/school accounts only.

**Q: What if I have no SRE Agent role?**
A: Access Required screen. Azure Owner/Contributor can auto-assign Admin.

**Q: Custom RBAC roles?**
A: Three built-in roles. Custom definitions via standard Azure IAM.

**Q: How does the portal enforce?**
A: Frontend checks + backend 403 enforcement.

**Q: Multiple admins?**
A: Yes.

---

## 10. Memory, Knowledge & Learning

**Q: How does it learn?**
A: Automatically from conversations + uploaded docs + #remember commands.

**Q: Does it learn from my data?**
A: Yes, from YOUR conversations. Does NOT train the underlying model.

**Q: Is learning automatic?**
A: Yes. 30 minutes after thread goes quiet.

**Q: Can I manually teach it?**
A: Yes. #remember or upload to KB.

**Q: Can I see what it learned?**
A: Ask it, or check Monitor > Session Insights.

**Q: Can I delete learned knowledge?**
A: #forget for memories. Remove docs from KB.

**Q: Does knowledge persist across conversations?**
A: Yes.

**Q: Does it prioritize recent knowledge?**
A: Prioritizes same-resource sessions.

**Q: What is overview.md?**
A: Main knowledge file, always loaded at conversation start.

**Q: Can I ask it to save knowledge?**
A: Yes. "Save this to your knowledge: [fact]"

**Q: #remember vs knowledge files?**
A: #remember = discrete searchable facts. Knowledge files = structured persistent references.

**Q: Can it search all sources simultaneously?**
A: Yes. Past incidents + user memories + knowledge base in parallel.

**Q: Does it provide citations?**
A: Yes. Clickable citations with sources.

**Q: Can I connect live wikis?**
A: Yes. ADO wiki and GitHub wiki connectors.

---

## 11. Security & Governance

**Q: Is the identity managed?**
A: Yes. User-assigned managed identity, no secrets.

**Q: What RBAC roles are always assigned?**
A: Reader, Log Analytics Reader, Monitoring Reader (RG scope), Monitoring Contributor (subscription).

**Q: Cross-subscription access?**
A: Yes, with appropriate RBAC.

**Q: Can I restrict to specific resources?**
A: Yes. Assign RBAC at resource or RG scope.

**Q: What is the permission flow?**
A: Check managed identity → if sufficient, use it → if not, OBO from Administrator.

**Q: Are actions auditable?**
A: Yes. 9 event types in Application Insights, KQL queryable.

**Q: Can I query audit logs?**
A: Yes. Monitor > Logs → customEvents table.

**Q: Azure Activity Log?**
A: Yes. ARM operations captured.

**Q: Compliance checks?**
A: Yes. Schedule security posture reviews, certificate checks, config audits.

**Q: Network security?**
A: *.azuresre.ai must be allowed. WebSocket required.

**Q: Private endpoints?**
A: Check docs for current options.

**Q: Encrypted traffic?**
A: Yes. HTTPS/WSS.

---

## 12. Advanced Scenarios

**Q: Multi-cloud monitoring?**
A: Yes via Python tools (AWS/GCP APIs) and MCP connectors.

**Q: On-premises infrastructure?**
A: Yes via Python tools or MCP with network access.

**Q: Microservices?**
A: Yes. Topology mapping, cross-service correlation.

**Q: Capacity planning?**
A: Yes via scheduled tasks + Python tools for forecasting.

**Q: PDF reports?**
A: Yes. Python with ReportLab.

**Q: Charts?**
A: Yes. Built-in visualization + Python (matplotlib, plotly).

**Q: Direct database connections?**
A: Yes via Python (SQL, PostgreSQL, MongoDB, Redis).

**Q: CI/CD integration?**
A: Via webhooks/API triggers + GitHub/ADO work items.

**Q: Multiple agents per subscription?**
A: Yes. Each is independent.

**Q: Agent-to-agent communication?**
A: No. Each agent is independent. Custom agents within one agent share context.

**Q: Azure outage impact?**
A: Agent unavailable if region affected. Multi-region agents for resilience.

**Q: Backup configuration?**
A: Export YAML definitions. Re-upload KB files.

**Q: Clone an agent?**
A: Not directly. Recreate with same config.

**Q: API available?**
A: Webhooks for chat-from-your-tools. Check docs.

**Q: White-label?**
A: No.

**Q: ITSM/ITIL support?**
A: Integrates with ServiceNow, PagerDuty. Follows your processes.

**Q: Chaos engineering?**
A: Not built-in. Configurable with custom tools.

**Q: SLO/SLI monitoring?**
A: Yes via scheduled tasks + Python SLO calculations.

**Q: Terraform integration?**
A: Via custom tools or GitHub/ADO connectors.

**Q: Blue/green deployments?**
A: With source control + custom agents for health verification.

**Q: Multi-team sharing?**
A: Yes. RBAC controls who can chat, approve, configure.

**Q: Simultaneous incidents from multiple sources?**
A: Yes. Independent processing via response plans.

**Q: Cross-agent learning?**
A: No. Each agent's memory is isolated.

**Q: Migrate between models?**
A: Yes. Change in Settings. Memory persists.

**Q: Memory persist on model change?**
A: Yes. Memory is agent-level, not model-level.

---

## 13. Use Cases & Scenarios

**Q: Best for startups?**
A: 24/7 monitoring without dedicated SRE team.

**Q: Best for enterprise?**
A: Standardize response, reduce MTTR, capture institutional knowledge.

**Q: Best for DevOps?**
A: Automate post-deploy verification, health checks, cost anomaly detection.

**Q: Best for MSPs?**
A: Per-customer agents with isolated data.

**Q: Application performance monitoring?**
A: Yes. App Insights queries, error rates, response times.

**Q: Cost optimization?**
A: Yes. Anomaly detection, underutilized resources, right-sizing.

**Q: Security monitoring?**
A: Yes. Posture reviews, misconfigs, threat monitoring.

**Q: Database troubleshooting?**
A: Yes. Create Database Expert custom agent.

**Q: Kubernetes management?**
A: Yes. Built-in AKS diagnostics + kubectl.

**Q: Serverless monitoring?**
A: Yes. Functions + Container Apps diagnostics.

**Q: Network troubleshooting?**
A: Yes. VNets, NSGs, load balancers via CLI.

**Q: Compliance reporting?**
A: Yes. Scheduled checks with automated reports.

**Q: During incident bridges?**
A: Yes. Share investigation thread links.

**Q: Post-mortem analysis?**
A: Yes. Session insights capture structured learnings.

**Q: Change management?**
A: Yes. Work items in GitHub/ADO. Review mode for approvals.

---

## 14. Troubleshooting

**Q: Create button unavailable?**
A: Register provider: `az provider register --namespace Microsoft.App`

**Q: Region dropdown empty?**
A: Submit registration request with subscription ID.

**Q: Portal doesn't load?**
A: Allow *.azuresre.ai in firewall. Check WebSocket. Try incognito.

**Q: Chat unresponsive?**
A: Check WebSocket connectivity. Zscaler may block by default.

**Q: Agent can't see resources?**
A: Verify RBAC on managed identity (minimum Reader on RGs).

**Q: 403 error?**
A: Missing SRE Agent role. Check IAM on agent resource.

**Q: OBO prompt not showing?**
A: Need Administrator role. Personal accounts can't authorize.

**Q: DeploymentNotFound?**
A: Register Microsoft.App provider and retry.

**Q: Hit AAU limit?**
A: Increase in Settings > Agent Consumption. Immediate effect.

**Q: Connector not connecting?**
A: Check network, credentials, service reachability.

**Q: MCP tools not available?**
A: Agent defers and auto-loads when connection establishes.

**Q: Scheduled task not running?**
A: Check status (On/Off), schedule, AAU limit.

**Q: Agent can't take actions?**
A: Check: permission level, run mode, management locks.

**Q: Custom agent not responding?**
A: Check instructions, tool assignments. Test in Playground first.

---

## 15. Competitive & Positioning

**Q: vs. AWS CloudWatch AI?**
A: SRE Agent provides autonomous incident response, memory/learning, custom agents, multi-tool orchestration.

**Q: vs. Datadog AI?**
A: Complementary. SRE Agent integrates WITH Datadog via MCP. Adds autonomous remediation + memory.

**Q: vs. PagerDuty AIOps?**
A: PagerDuty = alert management. SRE Agent adds investigation, RCA, memory, and can execute fixes.

**Q: vs. Shoreline.io?**
A: Both automate remediation. SRE Agent is Azure-native with broader LLM reasoning + memory.

**Q: Unique value proposition?**
A: Azure-native AI agent that learns your environment, remembers every incident, manages any Azure service, gets smarter over time.

**Q: Why not hire more SREs?**
A: Augments your team. 24/7 coverage, consistent quality, captured knowledge. Makes SREs more effective.

**Q: Works alongside other AIOps?**
A: Yes. Integrates with Datadog, Splunk, New Relic, Grafana, any MCP platform.

---

## 16. Miscellaneous

**Q: Documentation?**
A: learn.microsoft.com/en-us/azure/sre-agent/

**Q: GitHub repo?**
A: github.com/microsoft/sre-agent

**Q: Community?**
A: GitHub repo discussions.

**Q: Demo videos?**
A: Yes, on the overview page.

**Q: Training available?**
A: Check Microsoft Learn.

**Q: Support?**
A: Standard Azure support channels.

**Q: Product roadmap?**
A: GitHub repo for public roadmap.

**Q: Update frequency?**
A: Continuous. Check release notes.

**Q: Current version?**
A: Settings > Basics in agent portal.

**Q: Downgrade possible?**
A: No. Continuously updated.

**Q: Mobile app?**
A: No. Browser at sre.azure.com.

**Q: Use from Teams?**
A: Agent posts TO Teams. Check chat-from-your-tools docs.

**Q: Supported browsers?**
A: Modern browsers (Edge, Chrome, Firefox, Safari).

**Q: CLI available?**
A: Azure CLI for resource management. Agent accessed via web portal.

**Q: Embed in own portal?**
A: Check chat-from-your-tools for webhook/integration options.
