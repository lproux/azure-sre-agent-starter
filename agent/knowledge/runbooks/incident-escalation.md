# Runbook: Incident Escalation Procedures

## Severity Definitions

| Severity | Criteria | Response Time | Resolution Target |
|----------|----------|--------------|------------------|
| **SEV0 / P0** | Complete service outage, data loss risk | 5 minutes | 1 hour |
| **SEV1 / P1** | Major functionality impaired, many users affected | 15 minutes | 4 hours |
| **SEV2 / P2** | Partial degradation, workaround available | 30 minutes | 24 hours |
| **SEV3 / P3** | Minor issue, single user or non-critical service | 4 hours | 72 hours |
| **SEV4 / P4** | Informational, enhancement request | Next business day | Backlog |

## Escalation Flow

### Automated (SRE Agent)
1. Agent receives alert from incident platform (PagerDuty/Azure Monitor)
2. Agent triages: classifies severity, identifies affected service
3. Agent investigates: queries logs, metrics, deployment history
4. For P3/P4: Agent resolves autonomously or provides summary
5. For P1/P2: Agent provides diagnosis + recommended action, pages on-call

### Manual Escalation Path
```
On-Call Engineer (Primary)
    ↓ (15 min no ack)
On-Call Engineer (Secondary)
    ↓ (30 min no resolution for P1)
Engineering Manager
    ↓ (1 hour no resolution for P0)
VP Engineering + Exec Bridge
```

## Communication Templates

### Incident Declaration (Teams #incidents)
```
🔴 INCIDENT DECLARED — SEV[X]
Service: [SERVICE_NAME]
Impact: [DESCRIPTION]
Started: [TIME UTC]
Current Status: Investigating
Incident Commander: [NAME]
Bridge: [TEAMS MEETING LINK]
```

### Status Update (Every 30 min for P1, every 15 min for P0)
```
📋 STATUS UPDATE — SEV[X] — [SERVICE_NAME]
Duration: [X] minutes
Current Status: [Investigating/Mitigating/Monitoring]
What we know: [FINDINGS]
Next steps: [ACTIONS]
ETA to resolution: [ESTIMATE]
```

### Incident Resolution
```
✅ INCIDENT RESOLVED — SEV[X] — [SERVICE_NAME]
Duration: [X] minutes
Root Cause: [SUMMARY]
Resolution: [WHAT FIXED IT]
Action Items: [POST-INCIDENT TASKS]
PIR scheduled: [DATE/TIME]
```

## Post-Incident Review (PIR)

### Timeline: Within 48 hours of resolution

### PIR Template
1. **Incident Summary**: What happened, when, duration, impact
2. **Timeline**: Minute-by-minute of detection → response → resolution
3. **Root Cause**: Technical root cause analysis
4. **Contributing Factors**: What made it worse or delayed resolution
5. **What Went Well**: Things that worked during the response
6. **What Could Be Improved**: Gaps in monitoring, runbooks, or process
7. **Action Items**: Specific, assigned, time-bound improvements

### PIR Participants
- On-call engineers who responded
- Service owner
- Engineering manager
- SRE Agent (provides investigation thread as evidence)
