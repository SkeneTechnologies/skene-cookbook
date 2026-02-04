# Cross-Functional Incident Coordinator

## Objective

Orchestrate rapid, coordinated incident response across Support, Product, Engineering, and Customer Success teams. Ensure clear communication to affected customers, efficient problem resolution, and proper post-incident learning. This skill acts as the central coordination point during incidents to prevent chaos and ensure accountability.

## Execution Flow

### Incident Lifecycle
```
┌──────────┐    ┌─────────────┐    ┌───────────┐    ┌──────────┐    ┌───────────┐
│ DETECTED │ → │ TRIAGED     │ → │ MITIGATING│ → │ RESOLVED │ → │POST-MORTEM│
└──────────┘    └─────────────┘    └───────────┘    └──────────┘    └───────────┘
     │               │                  │               │               │
     ▼               ▼                  ▼               ▼               ▼
  Support        All Teams          Engineering      Support         Product
  OnCall         Assessment         + Product        + CS            + Eng
```

### Phase 1: Detection & Triage

```
# Gather incident context
support.get_incident(incidentId)          → Incident details
support.get_affected_customers(incidentId) → Customer impact list
product.get_feature_status(affectedService) → Feature health
engineering.get_service_health()           → System status
engineering.get_deployment_history(24h)    → Recent changes

# Assess severity
ai.assess_severity({
  customer_count: affected_customers.length,
  revenue_at_risk: sum(affected_arr),
  service_criticality: feature_criticality,
  workaround_available: boolean,
  data_loss_risk: boolean
})
```

#### Severity Classification
| Severity | Customer Impact | Response Time | Escalation |
|----------|----------------|---------------|------------|
| Sev1 | Widespread outage, data loss risk | Immediate | Exec + All teams |
| Sev2 | Major feature down, many customers | < 30 min | Engineering lead |
| Sev3 | Feature degraded, subset affected | < 2 hours | On-call team |
| Sev4 | Minor issue, workaround available | < 24 hours | Normal queue |

### Phase 2: Team Assembly & Coordination

```
BASED ON SEVERITY:

IF sev1:
    → Assemble: Engineering Lead, Product Lead, Support Lead, CS Lead, Comms
    → Channel: Create war room (Slack #incident-{id})
    → Cadence: Updates every 15 minutes
    → Exec: Notify VP Engineering, CTO

IF sev2:
    → Assemble: Engineering On-Call, Product PM, Support Lead
    → Channel: Existing incident channel
    → Cadence: Updates every 30 minutes
    → Exec: Notify Engineering Manager

IF sev3:
    → Assemble: Engineering On-Call, Support
    → Channel: Support escalation channel
    → Cadence: Updates every hour

IF sev4:
    → Assemble: Support + Engineering queue
    → Channel: Normal ticket flow
    → Cadence: As needed
```

### Phase 3: Customer Impact Assessment

```
# Identify strategic accounts
cs.get_strategic_accounts_affected(affected_customers)

PRIORITIZE COMMUNICATION:
1. Enterprise accounts with active escalations
2. Accounts in renewal window (next 90 days)
3. Accounts with exec sponsors engaged
4. High-usage accounts
5. All remaining affected accounts
```

### Phase 4: Communication Orchestration

```
ai.generate_comms({
  incident: incident_details,
  audience: ["status_page", "affected_customers", "internal", "strategic_accounts"],
  tone: "professional_empathetic",
  include: ["what_happened", "impact", "current_status", "eta_if_known", "next_update"]
})

COMMUNICATION CHANNELS:
- Status Page: Public updates (all severities)
- In-App Banner: Sev1/Sev2 only
- Email: Strategic accounts, all affected (Sev1)
- Slack/CS Outreach: Strategic accounts (Sev1/Sev2)
```

### Phase 5: Resolution & Recovery

```
WHEN mitigation_identified:
    → Track: implementation progress
    → Communicate: ETA updates
    → Verify: service restoration
    → Monitor: for regression

WHEN resolved:
    → Verify: all metrics normal
    → Communicate: resolution to all channels
    → Document: timeline and actions
    → Schedule: post-mortem (Sev1/Sev2 mandatory)
    → Trigger: customer_success/escalation_manager for follow-up
```

### Phase 6: Post-Incident

```
IF severity IN [sev1, sev2]:
    → Schedule: Post-mortem within 48 hours
    → Trigger: product_ops/incident_analyzer
    → Create: Action items for prevention
    → Update: Runbooks if applicable

CUSTOMER FOLLOW-UP (Strategic Accounts):
    → Trigger: customer_success/red_flag_detector
    → Action: CSM outreach within 24 hours
    → Offer: Impact remediation if applicable
```

## Response Format

```json
{
  "incidentId": "INC-2024-0215-001",
  "status": "mitigating",
  "severity": "sev2",
  
  "incidentSummary": {
    "title": "API Rate Limiting Affecting Batch Operations",
    "description": "Customers experiencing 429 errors on batch API endpoints, affecting scheduled data syncs",
    "detectedAt": "2024-02-15T14:23:00Z",
    "source": "monitoring",
    "affectedService": "api-gateway",
    "rootCause": "Rate limit configuration deployed with incorrect threshold"
  },
  
  "impactAssessment": {
    "totalCustomersAffected": 127,
    "strategicAccountsAffected": 8,
    "revenueAtRisk": 890000,
    "impactDescription": "Batch API calls failing, affecting 15% of API customers",
    "workaroundAvailable": true,
    "workaround": "Customers can reduce batch size to under 100 records",
    "dataLossRisk": false
  },
  
  "responseTeam": [
    {
      "role": "Incident Commander",
      "name": "Alex Rivera",
      "team": "Engineering",
      "status": "active"
    },
    {
      "role": "Technical Lead",
      "name": "Sam Chen",
      "team": "Platform Engineering",
      "status": "active"
    },
    {
      "role": "Customer Comms",
      "name": "Jordan Lee",
      "team": "Support",
      "status": "active"
    },
    {
      "role": "CS Liaison",
      "name": "Taylor Kim",
      "team": "Customer Success",
      "status": "active"
    }
  ],
  
  "timeline": [
    {
      "timestamp": "2024-02-15T14:23:00Z",
      "event": "Monitoring alert: API 429 rate spike",
      "actor": "Datadog"
    },
    {
      "timestamp": "2024-02-15T14:25:00Z",
      "event": "Incident created, Sev2 declared",
      "actor": "On-call"
    },
    {
      "timestamp": "2024-02-15T14:30:00Z",
      "event": "Root cause identified: config deployment at 14:15",
      "actor": "Platform Engineering"
    },
    {
      "timestamp": "2024-02-15T14:35:00Z",
      "event": "Status page updated, strategic accounts notified",
      "actor": "Support"
    },
    {
      "timestamp": "2024-02-15T14:40:00Z",
      "event": "Fix deployed, monitoring for recovery",
      "actor": "Platform Engineering"
    }
  ],
  
  "communications": {
    "statusPage": {
      "status": "published",
      "lastUpdate": "2024-02-15T14:40:00Z",
      "message": "We identified an issue with API rate limiting affecting batch operations. A fix has been deployed and we are monitoring recovery. Next update in 15 minutes."
    },
    "strategicAccounts": {
      "sent": 8,
      "channel": "email_and_slack",
      "template": "sev2_proactive_outreach"
    },
    "internalSlack": {
      "channel": "#incident-inc-0215-001",
      "lastUpdate": "2024-02-15T14:42:00Z"
    },
    "nextScheduledUpdate": "2024-02-15T14:55:00Z"
  },
  
  "nextActions": [
    {
      "action": "Monitor error rates for 15 minutes",
      "owner": "Platform Engineering",
      "dueBy": "2024-02-15T14:55:00Z",
      "status": "in_progress"
    },
    {
      "action": "Verify all affected customers recovered",
      "owner": "Support",
      "dueBy": "2024-02-15T15:00:00Z",
      "status": "pending"
    },
    {
      "action": "CSM outreach to 8 strategic accounts",
      "owner": "Customer Success",
      "dueBy": "2024-02-15T17:00:00Z",
      "status": "pending"
    },
    {
      "action": "Publish resolution status page update",
      "owner": "Support",
      "dueBy": "Upon resolution",
      "status": "pending"
    }
  ],
  
  "postMortemRequired": true,
  "postMortemDeadline": "2024-02-17T17:00:00Z",
  
  "exitState": "mitigating"
}
```

## Guardrails

### Response Time SLAs
| Severity | Detection → Triage | Triage → Comms | Target MTTR |
|----------|-------------------|----------------|-------------|
| Sev1 | 5 min | 15 min | 1 hour |
| Sev2 | 15 min | 30 min | 4 hours |
| Sev3 | 1 hour | 2 hours | 24 hours |
| Sev4 | 4 hours | 8 hours | 72 hours |

### Communication Rules
- Never speculate on root cause in customer communications
- Always include next update time
- Status page updates required for Sev1/Sev2 within 15 minutes
- No "blame" language in any communication
- Include workarounds when available

### Escalation Triggers
- Auto-escalate if no update in 2x expected interval
- Auto-escalate if affected customer count doubles
- Auto-escalate if strategic account requests
- Auto-escalate if data integrity concern emerges

### Post-Incident Requirements
- Sev1/Sev2: Post-mortem mandatory within 48 hours
- Sev3: Post-mortem if customer requested or recurring
- All: Document in incident database
- All: Update runbooks if process gap identified

### Customer Follow-Up
- Strategic accounts: CSM call within 24 hours
- All affected: Resolution email within 4 hours of resolution
- Recurring incidents: Executive apology for Sev1

## Integration Points

| Team | Skills Triggered | Trigger Condition |
|------|-----------------|-------------------|
| Support | `ticket_prioritizer`, `escalation_predictor` | Initial triage |
| Engineering | Internal alerting | Sev1/Sev2 declared |
| Product | `incident_analyzer` | Post-incident |
| CS | `red_flag_detector`, `escalation_manager` | Strategic account affected |
| Comms | `ai.generate_comms` | All status updates |
