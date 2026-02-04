# Revenue Intelligence Hub

## Objective

Provide a unified, real-time view of revenue health by synthesizing data from RevOps (pipeline & bookings), Monetization (MRR/ARR & expansion), and FinOps (unit economics & efficiency). Enable accurate forecasting, early anomaly detection, and actionable insights for revenue leadership.

## Execution Flow

### Revenue Data Model
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         REVENUE INTELLIGENCE HUB                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────┐      ┌──────────────┐      ┌─────────────┐               │
│   │   REVOPS    │      │ MONETIZATION │      │   FINOPS    │               │
│   ├─────────────┤      ├──────────────┤      ├─────────────┤               │
│   │ Pipeline    │      │ MRR/ARR      │      │ CAC         │               │
│   │ Bookings    │      │ Expansion    │      │ LTV         │               │
│   │ Forecast    │      │ Churn        │      │ Payback     │               │
│   │ Attribution │      │ Cohorts      │      │ Efficiency  │               │
│   └──────┬──────┘      └──────┬───────┘      └──────┬──────┘               │
│          │                    │                      │                      │
│          └────────────────────┼──────────────────────┘                      │
│                               ▼                                              │
│                    ┌──────────────────┐                                     │
│                    │ UNIFIED METRICS  │                                     │
│                    │ & FORECASTING    │                                     │
│                    └──────────────────┘                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Phase 1: Data Collection
```
# Pipeline & Bookings (RevOps)
crm.get_pipeline(period)           → Pipeline by stage, segment
crm.get_forecast(period)           → Commit, best case, pipeline

# Recurring Revenue (Monetization)  
monetization.get_mrr_movements()   → New, expansion, contraction, churn
monetization.get_arr_breakdown()   → ARR by segment, product, cohort

# Unit Economics (FinOps)
finops.get_unit_economics()        → CAC, LTV, margins
finops.get_cac_payback()           → Payback by segment

# Attribution & Cohorts
analytics.get_revenue_attribution() → Source attribution
analytics.get_cohort_analysis()     → Cohort performance
```

### Phase 2: Metric Synthesis

#### Core Revenue Metrics
| Metric | Formula | Source |
|--------|---------|--------|
| ARR | Sum of annual contract values | Monetization |
| Net New ARR | New + Expansion - Contraction - Churn | Monetization |
| NRR | (Starting ARR + Expansion - Contraction - Churn) / Starting ARR | Monetization |
| GRR | (Starting ARR - Contraction - Churn) / Starting ARR | Monetization |
| Pipeline Coverage | Pipeline / Quota | RevOps |
| Win Rate | Closed Won / Total Closed | RevOps |

#### Efficiency Metrics
| Metric | Formula | Source |
|--------|---------|--------|
| CAC Payback | CAC / (ARPU × Gross Margin) | FinOps |
| LTV:CAC | LTV / CAC | FinOps |
| Magic Number | Net New ARR / S&M Spend | FinOps |
| Burn Multiple | Net Burn / Net New ARR | FinOps |

### Phase 3: Anomaly Detection
```
ai.detect_anomalies({
  metrics: [mrr_movements, pipeline_velocity, win_rate, churn_rate],
  sensitivity: "medium",
  lookback_days: 90
})

ANOMALY TRIGGERS:
- MRR movement deviation > 2σ from trend
- Pipeline velocity drop > 20% WoW
- Win rate change > 10pp MoM
- Churn spike > 1.5x average
- CAC increase > 15% QoQ
```

### Phase 4: Forecasting
```
ai.forecast_revenue({
  method: "weighted_ensemble",
  inputs: {
    pipeline_forecast: crm_forecast,
    historical_conversion: conversion_rates,
    expansion_signals: expansion_pipeline,
    churn_probability: at_risk_accounts,
    seasonality: historical_patterns
  },
  confidence_intervals: [0.70, 0.85, 0.95]
})
```

### Phase 5: Insight Generation & Skill Routing

```
IF forecast_gap > 10%:
    → Trigger: revops/deal_inspection (top deals)
    → Trigger: revops/commit_accuracy (forecast review)
    → Exit: target_at_risk

IF churn_spike_detected:
    → Trigger: customer_success/red_flag_detector
    → Trigger: monetization/mrr_movement_tracker
    → Exit: anomaly_detected

IF expansion_opportunity > threshold:
    → Trigger: monetization/upgrade_trigger (ready accounts)
    → Exit: expansion_opportunity

IF efficiency_declining:
    → Trigger: finops/cost_allocation
    → Exit: efficiency_alert

ELSE:
    → Exit: healthy
```

## Response Format

```json
{
  "period": "Q1 2024",
  "generatedAt": "2024-02-15T10:30:00Z",
  
  "revenueSnapshot": {
    "arr": 12500000,
    "arrGrowth": 0.32,
    "mrr": 1041667,
    "netNewArr": {
      "total": 450000,
      "new": 280000,
      "expansion": 220000,
      "contraction": -30000,
      "churn": -20000
    },
    "nrr": 1.18,
    "grr": 0.96
  },
  
  "pipeline": {
    "totalValue": 4200000,
    "coverage": 3.2,
    "weightedPipeline": 1890000,
    "byStage": {
      "discovery": 1200000,
      "evaluation": 1500000,
      "negotiation": 1000000,
      "closing": 500000
    }
  },
  
  "forecast": {
    "commit": 1100000,
    "bestCase": 1400000,
    "pipeline": 1890000,
    "aiPrediction": {
      "expected": 1250000,
      "confidence_70": [1150000, 1350000],
      "confidence_95": [1050000, 1450000]
    },
    "vsTarget": {
      "target": 1300000,
      "gap": -50000,
      "gapPercent": -0.038
    }
  },
  
  "efficiency": {
    "cac": 15000,
    "ltv": 75000,
    "ltvCacRatio": 5.0,
    "cacPaybackMonths": 14,
    "magicNumber": 0.85,
    "burnMultiple": 1.2
  },
  
  "anomalies": [
    {
      "type": "churn_spike",
      "severity": "medium",
      "metric": "monthly_churn_rate",
      "expected": 0.015,
      "actual": 0.023,
      "affectedSegment": "SMB",
      "recommendation": "Investigate SMB churn - 3 accounts churned citing pricing"
    }
  ],
  
  "recommendations": [
    {
      "priority": "high",
      "area": "pipeline",
      "insight": "Pipeline coverage dropped to 3.2x, below 4x target",
      "action": "Accelerate top-of-funnel activities",
      "skillToTrigger": "marketing/demand_generation",
      "expectedImpact": "+$500k pipeline in 30 days"
    },
    {
      "priority": "medium", 
      "area": "expansion",
      "insight": "42 accounts showing expansion signals but no active opportunity",
      "action": "Create expansion opportunities for ready accounts",
      "skillToTrigger": "monetization/upgrade_trigger",
      "expectedImpact": "+$180k expansion ARR"
    }
  ],
  
  "exitState": "target_at_risk"
}
```

## Guardrails

### Data Integrity
- All revenue figures must reconcile across sources (tolerance: 0.1%)
- Forecast requires minimum 2 quarters of historical data
- Anomaly detection requires 90+ days of baseline data
- Flag data freshness issues (>24h stale data)

### Forecast Accuracy
- Track forecast vs. actuals for continuous calibration
- Require human review for forecasts with >20% variance from commit
- Distinguish between AI prediction and rep-submitted forecast

### Access Control
- Revenue details visible only to authorized roles
- Anonymize individual deal data in cross-functional reports
- Audit log all forecast overrides

### Metric Consistency
- Use standardized definitions across all reports
- Document any calculation methodology changes
- Maintain metric version history for comparisons

## Integration Points

| Domain | Skills Triggered | Trigger Condition |
|--------|-----------------|-------------------|
| RevOps | `commit_accuracy`, `deal_inspection` | Forecast gap, pipeline anomaly |
| Monetization | `mrr_movement_tracker`, `cohort_ltv_analyzer` | Churn spike, LTV deviation |
| FinOps | `budget_variance`, `cost_allocation` | Efficiency decline |
| CS | `red_flag_detector`, `risk_mitigation_playbook` | Churn risk increase |
| Marketing | `demand_generation`, `attribution_tracker` | Pipeline coverage low |
