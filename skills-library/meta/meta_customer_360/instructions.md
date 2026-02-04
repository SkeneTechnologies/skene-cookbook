# Customer 360 Aggregator

## Objective

Provide a complete, unified view of any customer by aggregating and synthesizing data from Customer Success, Support, Product Analytics, and Billing systems. Enable any team member to quickly understand account context, identify risks and opportunities, and take informed action without navigating multiple systems.

## Execution Flow

### Data Architecture
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CUSTOMER 360 VIEW                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │     CRM      │  │      CS      │  │   SUPPORT    │  │  ANALYTICS   │    │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤    │
│  │ Account      │  │ Health Score │  │ Tickets      │  │ Usage        │    │
│  │ Contacts     │  │ Success Plan │  │ CSAT/NPS     │  │ Features     │    │
│  │ Activities   │  │ Lifecycle    │  │ Escalations  │  │ Engagement   │    │
│  │ Opportunities│  │ Risks        │  │ SLA          │  │ Trends       │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                 │                 │                  │            │
│         └─────────────────┼─────────────────┼──────────────────┘            │
│                           ▼                 ▼                               │
│                    ┌──────────────┐  ┌──────────────┐                       │
│                    │ MONETIZATION │  │   AI/ML      │                       │
│                    ├──────────────┤  ├──────────────┤                       │
│                    │ Contract     │  │ Synthesis    │                       │
│                    │ Billing      │  │ Prediction   │                       │
│                    │ Entitlements │  │ Insights     │                       │
│                    └──────────────┘  └──────────────┘                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Phase 1: Data Collection

```
# Account Foundation
crm.get_account(accountId)           → Firmographics, segment, owner
crm.get_contacts(accountId)          → Stakeholder map
crm.get_activities(accountId, 90d)   → Recent engagement

# Customer Success
cs.get_health_score(accountId)       → Current health, trend
cs.get_success_plan(accountId)       → Goals, milestones, progress

# Support
support.get_tickets(accountId, 90d)  → Open/closed tickets
support.get_satisfaction(accountId)  → CSAT, NPS scores

# Product
analytics.get_product_usage(accountId)   → Usage metrics
analytics.get_feature_adoption(accountId) → Feature engagement

# Commercial
monetization.get_contract(accountId)      → Contract details
monetization.get_billing_history(accountId) → Payment history
```

### Phase 2: Signal Synthesis

#### Health Score Components
| Dimension | Weight | Signals |
|-----------|--------|---------|
| Product Usage | 30% | DAU/WAU/MAU, feature breadth, depth |
| Engagement | 25% | Meeting cadence, response rate, NPS |
| Support | 20% | Ticket volume, severity, resolution time |
| Commercial | 15% | Payment status, contract compliance |
| Outcome | 10% | Goal progress, value realization |

#### Risk Signal Detection
```
ai.predict_risk({
  signals: {
    usage_decline: usage_trend < -20%,
    engagement_drop: no_meeting_45_days,
    support_escalation: p1_tickets > 2,
    champion_risk: champion_activity_low,
    payment_issue: invoice_overdue > 30_days,
    contract_concern: renewal_90_days_no_engagement
  }
})
```

### Phase 3: Insight Generation

```
ai.synthesize_insights({
  data: [account, cs, support, usage, commercial],
  focus: requested_focus_area,
  generate: [
    "key_narrative",      // 2-3 sentence account summary
    "risk_indicators",    // Prioritized risk list
    "opportunities",      // Expansion/upsell signals
    "recommended_actions" // Next best actions
  ]
})
```

### Phase 4: Action Routing

```
IF health_score < 60 OR critical_risk_detected:
    → Trigger: customer_success/red_flag_detector
    → Trigger: customer_success/risk_mitigation_playbook
    → Exit: at_risk

IF support_escalation_active:
    → Trigger: support_ops/escalation_predictor
    → Exit: escalation_required

IF expansion_signals AND health_score > 75:
    → Trigger: customer_success/success_plan_generator
    → Exit: expansion_ready

IF renewal_approaching AND no_qbr_scheduled:
    → Trigger: customer_success/quarterly_business_review
    → Exit: renewal_focus

IF minor_concerns:
    → Exit: attention_needed

ELSE:
    → Exit: healthy
```

## Response Format

```json
{
  "accountId": "acc_12345",
  "generatedAt": "2024-02-15T14:30:00Z",
  "dataCompleteness": 0.94,
  
  "accountProfile": {
    "name": "Acme Corporation",
    "segment": "Enterprise",
    "industry": "Financial Services",
    "arr": 180000,
    "customerSince": "2022-03-15",
    "csm": "Sarah Chen",
    "ae": "Michael Torres",
    "contractEnd": "2024-09-30"
  },
  
  "healthSummary": {
    "overallScore": 72,
    "trend": "declining",
    "trendDelta": -8,
    "dimensions": {
      "usage": { "score": 78, "trend": "stable" },
      "engagement": { "score": 65, "trend": "declining" },
      "support": { "score": 70, "trend": "stable" },
      "commercial": { "score": 85, "trend": "stable" },
      "outcome": { "score": 60, "trend": "unknown" }
    }
  },
  
  "engagementSummary": {
    "lastMeeting": "2024-01-28",
    "daysSinceContact": 18,
    "meetingCadence": "monthly",
    "responsiveness": "medium",
    "npsScore": 7,
    "executiveSponsor": {
      "name": "Jennifer Wu",
      "title": "VP Operations",
      "lastEngagement": "2024-01-15",
      "sentiment": "neutral"
    },
    "champion": {
      "name": "David Kim",
      "title": "Director of Analytics",
      "engagement": "high",
      "riskFlag": false
    }
  },
  
  "supportSummary": {
    "openTickets": 2,
    "ticketsLast90Days": 8,
    "avgResolutionTime": "18h",
    "csat": 4.2,
    "escalations": 1,
    "topIssues": [
      { "category": "Integration", "count": 3 },
      { "category": "Performance", "count": 2 }
    ],
    "activeEscalation": {
      "ticketId": "TKT-4521",
      "issue": "API rate limiting causing batch job failures",
      "severity": "P2",
      "daysOpen": 5
    }
  },
  
  "usageSummary": {
    "mau": 245,
    "mauTrend": "stable",
    "dauWauRatio": 0.42,
    "topFeatures": ["Dashboard", "Reports", "API"],
    "underutilized": ["Automations", "Integrations"],
    "usageDepth": 0.65,
    "powerUsers": 12,
    "atRiskUsers": 8
  },
  
  "commercialSummary": {
    "arr": 180000,
    "contract": {
      "type": "Annual",
      "startDate": "2023-09-30",
      "endDate": "2024-09-30",
      "daysToRenewal": 227,
      "autoRenew": false
    },
    "billing": {
      "status": "current",
      "lastPayment": "2024-02-01",
      "paymentMethod": "ACH"
    },
    "expansion": {
      "currentSeats": 250,
      "usedSeats": 245,
      "seatUtilization": 0.98,
      "potentialUpsell": ["Enterprise SSO", "Advanced Analytics"]
    }
  },
  
  "keyNarrative": "Acme Corporation is a 2-year Enterprise customer ($180K ARR) showing signs of engagement decline despite stable product usage. Health score dropped 8 points to 72 over the past quarter, primarily driven by reduced meeting cadence and an active P2 escalation. With renewal in 7 months and near-full seat utilization (98%), this is both a retention risk and expansion opportunity requiring immediate CSM attention.",
  
  "riskIndicators": [
    {
      "type": "engagement_decline",
      "severity": "medium",
      "signal": "No meeting in 18 days, previously monthly cadence",
      "recommendation": "Schedule check-in call this week"
    },
    {
      "type": "active_escalation",
      "severity": "high",
      "signal": "P2 ticket open for 5 days affecting production workflows",
      "recommendation": "Escalate to engineering, CSM join resolution call"
    },
    {
      "type": "renewal_preparation",
      "severity": "low",
      "signal": "227 days to renewal, no QBR scheduled",
      "recommendation": "Schedule QBR for Q2"
    }
  ],
  
  "opportunities": [
    {
      "type": "expansion",
      "signal": "98% seat utilization, 8 users on waitlist",
      "value": 25000,
      "recommendation": "Propose seat expansion in next meeting"
    },
    {
      "type": "upsell",
      "signal": "Heavy API usage, no SSO (security requirement mentioned)",
      "value": 35000,
      "recommendation": "Present Enterprise tier with SSO"
    }
  ],
  
  "recommendedActions": [
    {
      "priority": 1,
      "action": "Resolve active escalation",
      "owner": "Support + CSM",
      "dueDate": "2024-02-17",
      "skillTrigger": "support_ops/escalation_predictor"
    },
    {
      "priority": 2,
      "action": "Schedule account check-in",
      "owner": "CSM",
      "dueDate": "2024-02-19",
      "skillTrigger": null
    },
    {
      "priority": 3,
      "action": "Prepare expansion proposal",
      "owner": "CSM + AE",
      "dueDate": "2024-02-28",
      "skillTrigger": "customer_success/success_plan_generator"
    }
  ],
  
  "exitState": "attention_needed"
}
```

## Guardrails

### Data Quality
- Flag incomplete data sources (missing > 20% of expected fields)
- Highlight stale data (>7 days old for engagement, >24h for support)
- Reconcile conflicting signals across sources
- Minimum data requirements: account, usage, support (CS optional but recommended)

### Privacy & Access
- Respect contact communication preferences
- Redact sensitive notes unless viewer has permission
- Audit log all 360 view access
- Apply segment-based data visibility rules

### Insight Accuracy
- Distinguish between observed data and AI-inferred insights
- Confidence score all predictions
- Avoid definitive statements for low-confidence insights
- Track insight accuracy over time for model improvement

### Action Recommendations
- Only recommend actions within requester's scope
- Include owner and timeline for each recommendation
- Prioritize by impact and urgency
- Limit to top 5 actions to avoid overwhelm

## Integration Points

| Data Source | Refresh Rate | Skills Triggered |
|-------------|-------------|------------------|
| CRM | Real-time | `stakeholder_mapper` on contact change |
| CS Platform | Hourly | `red_flag_detector` on health decline |
| Support | Real-time | `escalation_predictor` on P1/P2 ticket |
| Analytics | Daily | `adoption_score` on usage change |
| Billing | Daily | `dunning_automation` on payment issue |
