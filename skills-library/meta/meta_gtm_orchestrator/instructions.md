# GTM Motion Orchestrator

## Objective

Coordinate Product-Led Growth (PLG), Sales-Led, and Partner-Led motions to deliver the optimal go-to-market approach for each account. This skill acts as the central routing intelligence that determines which motion—or combination of motions—will maximize conversion and revenue.

## Execution Flow

### Phase 1: Signal Collection
```
┌─────────────────────────────────────────────────────────────┐
│                    SIGNAL AGGREGATION                        │
├─────────────────────────────────────────────────────────────┤
│  lifecycle.get_segment(accountId)     → Segment & ICP fit   │
│  lifecycle.get_account_stage(accountId) → Current stage     │
│  analytics.get_product_usage(accountId) → Usage signals     │
│  crm.get_account(accountId)           → Firmographics       │
│  partner.get_overlaps(accountId)      → Partner ecosystem   │
└─────────────────────────────────────────────────────────────┘
```

### Phase 2: Motion Scoring
Evaluate each motion based on collected signals:

| Motion | Key Signals | Weight |
|--------|-------------|--------|
| PLG Self-Serve | High product engagement, SMB segment, no deal in CRM | 0.35 |
| Sales Assist | Mid-market, usage plateau, expansion signals | 0.25 |
| Sales-Led | Enterprise, low self-serve activity, budget signals | 0.20 |
| Partner Co-Sell | Active partner relationship, tech stack overlap | 0.15 |
| Partner Sourced | Partner referral, no prior engagement | 0.05 |

### Phase 3: Motion Selection
```
IF usage_depth > 70% AND segment = "SMB" AND no_active_deal:
    → Trigger: plg/self_serve_expansion
    → Exit: plg_activation

ELIF usage_plateau AND segment IN ["MM", "Enterprise"] AND partner_overlap:
    → Trigger: ecosystem/nearbound_signal + revops/opportunity_scoring
    → Exit: co_sell_trigger

ELIF enterprise_signals AND low_self_serve:
    → Trigger: revops/lead_routing
    → Exit: lead_qualification

ELIF partner_referral:
    → Trigger: ecosystem/partner_influenced_revenue
    → Exit: partner_sourced

ELSE:
    → Continue monitoring
    → Exit: idle
```

### Phase 4: Handoff Orchestration
When transitioning between motions:

1. **PLG → Sales**: Package product usage context for AE
2. **Sales → Partner**: Share deal context with partner team
3. **Partner → Sales**: Import partner intel into CRM
4. **Any → CS**: Ensure adoption context transfers post-close

## Response Format

```json
{
  "accountId": "acc_12345",
  "analysis": {
    "currentMotion": "plg",
    "segmentFit": "mid_market",
    "usageScore": 72,
    "partnerOverlap": ["aws", "salesforce"],
    "dealStatus": "no_active_opportunity"
  },
  "recommendation": {
    "motion": "sales_assist",
    "confidence": 0.85,
    "reasoning": "Account shows strong product adoption (72%) but has plateaued. Mid-market segment with AWS partnership overlap suggests sales-assist with partner co-sell could accelerate expansion.",
    "nextSkill": "revops/opportunity_scoring",
    "parallelActions": [
      "ecosystem/nearbound_signal",
      "plg/usage_depth_analyzer"
    ]
  },
  "handoff": {
    "targetTeam": "sales",
    "context": {
      "topFeatures": ["api", "integrations", "team_seats"],
      "expansionSignals": ["new_department_users", "api_usage_spike"],
      "partnerContext": "AWS Marketplace customer, eligible for co-sell"
    },
    "urgency": "medium",
    "sla": "48h"
  },
  "exitState": "sales_assist"
}
```

## Guardrails

### Motion Conflict Resolution
- Never run competing motions simultaneously (e.g., PLG upgrade prompt + sales outreach)
- Establish motion ownership: first-mover gets 72h exclusivity
- Escalate conflicts to RevOps for manual resolution

### Data Quality Gates
- Require minimum 7 days of usage data before PLG motion recommendation
- Verify CRM data freshness < 24h before sales motion triggers
- Confirm partner data sync before co-sell recommendations

### Customer Experience Protection
- Maximum 2 motion touches per account per week
- Respect explicit motion preferences in account settings
- Block motion changes during active deal stages (Negotiation, Closing)

### Compliance
- Log all motion decisions with reasoning for audit
- Ensure GDPR consent verification before partner data sharing
- Respect territory/account ownership rules from CRM

## Integration Points

| Downstream Skill | Trigger Condition | Data Passed |
|-----------------|-------------------|-------------|
| `plg/self_serve_expansion` | PLG motion selected | usage_context, upgrade_triggers |
| `revops/lead_routing` | Sales motion selected | segment, usage_summary, intent_signals |
| `revops/opportunity_scoring` | Deal creation needed | account_data, motion_history |
| `ecosystem/nearbound_signal` | Partner overlap detected | partner_ids, overlap_type |
| `ecosystem/partner_influenced_revenue` | Co-sell motion selected | deal_context, partner_context |
