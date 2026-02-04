# Land & Expand Journey Manager

## Objective

Orchestrate the complete customer journey from initial PLG acquisition through activation, adoption, and expansion. This skill ensures seamless handoffs between PLG, Customer Success, and Monetization domains while maximizing Net Revenue Retention (NRR) through timely interventions and personalized expansion paths.

## Execution Flow

### Journey Stage Model
```
┌──────────┐    ┌────────────┐    ┌───────────┐    ┌──────────┐    ┌───────────┐    ┌─────────┐
│  TRIAL   │ → │ ONBOARDING │ → │ ACTIVATION│ → │ ADOPTION │ → │ EXPANSION │ → │ RENEWAL │
└──────────┘    └────────────┘    └───────────┘    └──────────┘    └───────────┘    └─────────┘
     │               │                 │               │               │               │
     ▼               ▼                 ▼               ▼               ▼               ▼
   PLG            PLG/CS              PLG            CS/PLG         CS/Sales       CS/Finance
  Domain          Handoff           Domain          Handoff         Domains        Domains
```

### Phase 1: Stage Detection & Health Assessment
```
lifecycle.get_journey_stage(accountId)     → Current stage
lifecycle.get_account_health(accountId)    → Health score
analytics.get_adoption_metrics(accountId)  → Feature adoption
analytics.get_usage_trends(accountId)      → Usage trajectory
```

### Phase 2: Stage-Specific Orchestration

#### Trial Stage
```
IF days_remaining < 3 AND activation_score < 50%:
    → Trigger: plg/trial_extension_evaluator
    → Action: Evaluate extension or conversion push

IF quick_win_achieved = false AND day > 1:
    → Trigger: plg/quick_win_generator
    → Action: Surface easiest value path

IF trial_converting_signals:
    → Trigger: monetization/upgrade_trigger
    → Exit: expansion_ready
```

#### Onboarding Stage
```
IF setup_completion < 80% AND days_since_signup > 7:
    → Trigger: plg/guided_setup_wizard
    → Exit: activation_focus

IF onboarding_health = "at_risk":
    → Trigger: customer_success/onboarding_health
    → Exit: at_risk_intervention

IF activation_milestone_reached:
    → Trigger: plg/milestone_celebration
    → Transition: → Activation Stage
```

#### Activation Stage
```
IF time_to_value > benchmark:
    → Trigger: customer_success/time_to_impact
    → Exit: at_risk_intervention

IF aha_moment_reached AND champion_identified:
    → Trigger: customer_success/adoption_score
    → Exit: champion_building

IF activation_complete:
    → Transition: → Adoption Stage
```

#### Adoption Stage
```
IF usage_depth > 60% AND new_use_case_signals:
    → Trigger: customer_success/success_plan_generator
    → Exit: adoption_nurture

IF adoption_plateau_detected:
    → Trigger: customer_success/product_adoption_guidance
    → Action: Surface next features

IF expansion_readiness > 70%:
    → Trigger: monetization/consumption_analyzer
    → Exit: expansion_ready
```

#### Expansion Stage
```
IF usage_approaching_limit:
    → Trigger: monetization/overage_predictor + upgrade_trigger
    → Exit: expansion_ready

IF multi_product_opportunity:
    → Trigger: customer_success/multi_product_adoption
    → Action: Cross-sell motion

IF contract_renewal_approaching:
    → Transition: → Renewal Stage
```

#### Renewal Stage
```
IF renewal_90_days_out:
    → Trigger: customer_success/quarterly_business_review
    → Action: Schedule QBR

IF renewal_risk_detected:
    → Trigger: customer_success/risk_mitigation_playbook
    → Exit: at_risk_intervention

IF expansion_in_renewal:
    → Trigger: monetization/packaging_optimizer
    → Exit: expansion_ready
```

### Phase 3: Cross-Stage Interventions

Always monitor for cross-cutting signals:
- **Champion departure**: Trigger stakeholder mapping
- **Usage cliff**: Trigger adoption intervention regardless of stage
- **Support escalation**: Coordinate with incident flow
- **Competitive signals**: Alert appropriate teams

## Response Format

```json
{
  "accountId": "acc_12345",
  "journey": {
    "currentStage": "adoption",
    "stageEntryDate": "2024-01-15",
    "daysInStage": 45,
    "stageHealth": "healthy",
    "progressionVelocity": "normal"
  },
  "health": {
    "overallScore": 78,
    "adoptionScore": 72,
    "engagementTrend": "stable",
    "riskFactors": []
  },
  "expansion": {
    "readinessScore": 68,
    "signals": [
      "approaching_seat_limit",
      "api_usage_growing",
      "new_team_onboarded"
    ],
    "blockers": [
      {
        "type": "feature_gap",
        "description": "SSO required for enterprise rollout",
        "impact": "high"
      }
    ],
    "estimatedExpansionValue": 24000
  },
  "recommendation": {
    "primaryFocus": "adoption_nurture",
    "reasoning": "Account showing strong adoption (72%) but hasn't explored advanced features. SSO blocker preventing enterprise-wide rollout.",
    "nextMilestone": {
      "name": "Enterprise Readiness",
      "targetDate": "2024-03-15",
      "requirements": ["sso_enabled", "admin_training_complete"]
    },
    "skillsToTrigger": [
      {
        "skill": "customer_success/success_plan_generator",
        "priority": "high",
        "context": "Create enterprise rollout success plan"
      },
      {
        "skill": "plg/progressive_disclosure",
        "priority": "medium",
        "context": "Surface advanced analytics features"
      }
    ]
  },
  "exitState": "adoption_nurture"
}
```

## Guardrails

### Journey Integrity
- Never skip stages (Trial → Adoption is invalid)
- Minimum time in each stage before progression:
  - Trial: 1 day
  - Onboarding: 3 days
  - Activation: 7 days
  - Adoption: 30 days
- Maximum interventions per stage: 5 per week

### Handoff Quality
- CS handoff requires: activation milestone, primary contact, usage baseline
- Sales handoff requires: expansion signals, decision maker identified, budget timing
- Never hand off during active support incident

### Monetization Sensitivity
- Expansion conversations only after activation milestone
- No upgrade prompts within 7 days of support escalation
- Respect customer's stated expansion timeline

### Data Requirements
- Stage transitions require 3+ days of consistent signals
- Health scores require minimum 7 days of data
- Expansion readiness requires usage + engagement + sentiment signals

## Integration Points

| Stage | Primary Skills | Handoff Trigger |
|-------|---------------|-----------------|
| Trial | `plg/quick_win_generator`, `plg/trial_extension_evaluator` | Conversion or extension |
| Onboarding | `plg/guided_setup_wizard`, `customer_success/onboarding_health` | Activation milestone |
| Activation | `plg/milestone_celebration`, `customer_success/time_to_impact` | Value realization |
| Adoption | `customer_success/adoption_score`, `customer_success/success_plan_generator` | Usage depth threshold |
| Expansion | `monetization/upgrade_trigger`, `monetization/packaging_optimizer` | Commercial conversation |
| Renewal | `customer_success/quarterly_business_review`, `monetization/contract_value_tracker` | Contract close |
