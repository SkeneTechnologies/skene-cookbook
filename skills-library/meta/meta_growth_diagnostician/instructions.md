# Growth Diagnostician

## Objective

Systematically identify growth blockers and opportunities across the entire customer funnel by analyzing metrics from Acquisition through Referral (AARRR framework). Provide data-driven diagnoses and actionable recommendations to unlock growth, whether the bottleneck is in marketing, product, CS, or monetization.

## Execution Flow

### AARRR Framework Analysis
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GROWTH FUNNEL ANALYSIS                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ACQUISITION    ACTIVATION    RETENTION    REVENUE     REFERRAL            │
│   ──────────────────────────────────────────────────────────────            │
│   │ Visitors │ → │ Signups │ → │ Active │ → │ Paying │ → │ Advocates │      │
│   └──────────┘   └─────────┘   └────────┘   └────────┘   └───────────┘      │
│        │              │             │            │              │            │
│        ▼              ▼             ▼            ▼              ▼            │
│   ┌────────┐    ┌─────────┐   ┌────────┐   ┌────────┐    ┌─────────┐       │
│   │Marketing│    │  PLG    │   │  CS    │   │  Rev   │    │  PLG    │       │
│   │ Skills  │    │ Skills  │   │ Skills │   │ Skills │    │ Skills  │       │
│   └────────┘    └─────────┘   └────────┘   └────────┘    └─────────┘       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Phase 1: Funnel Data Collection

```
# Acquisition Metrics
marketing.get_channel_performance()     → Traffic, leads by channel
analytics.get_conversion_rates("top")   → Visitor → Signup rate

# Activation Metrics  
analytics.get_funnel_metrics("activation") → Signup → Activated
lifecycle.get_velocity_metrics("onboarding") → Time to activate
product.get_friction_points("onboarding")  → Drop-off points

# Retention Metrics
analytics.get_cohort_analysis("retention") → Cohort curves
lifecycle.get_stage_distribution()       → Active/dormant/churned
analytics.get_conversion_rates("engagement") → WAU/MAU trends

# Revenue Metrics
monetization.get_expansion_funnel()      → Free → Paid → Expanded
analytics.get_conversion_rates("monetization") → Upgrade rates

# Referral Metrics
analytics.get_funnel_metrics("referral") → Viral coefficient
marketing.get_channel_performance("referral") → Referral attribution
```

### Phase 2: Benchmark Comparison

| Stage | Metric | Your Rate | Benchmark | Gap |
|-------|--------|-----------|-----------|-----|
| Acquisition | Visitor → Signup | ? | 3-5% | ? |
| Activation | Signup → Activated | ? | 20-40% | ? |
| Retention | Week 1 Retention | ? | 40-60% | ? |
| Revenue | Free → Paid | ? | 2-5% | ? |
| Referral | Viral Coefficient | ? | 0.2-0.5 | ? |

### Phase 3: Blocker Diagnosis

```
ai.diagnose_blockers({
  funnel_data: collected_metrics,
  comparison: benchmarks,
  signals: {
    acquisition: channel_performance,
    activation: friction_points,
    retention: cohort_decay_curves,
    revenue: pricing_friction,
    referral: sharing_behavior
  }
})

DIAGNOSIS PATTERNS:

IF acquisition_rate < benchmark AND cpl_rising:
    → Blocker: "Channel saturation / CAC inflation"
    → Trigger: marketing/channel_optimizer

IF signup_rate OK BUT activation_rate < 20%:
    → Blocker: "Activation friction"
    → Trigger: plg/friction_detector + plg/quick_win_generator

IF activation OK BUT week1_retention < 40%:
    → Blocker: "Habit formation failure"
    → Trigger: plg/habit_loop_builder + customer_success/onboarding_health

IF retention OK BUT conversion_rate < 2%:
    → Blocker: "Monetization friction"
    → Trigger: monetization/pricing_optimization + plg/reverse_trial

IF conversion OK BUT expansion_rate < target:
    → Blocker: "Expansion ceiling"
    → Trigger: monetization/packaging_optimizer + customer_success/multi_product_adoption
```

### Phase 4: Opportunity Identification

Look for positive signals that can be amplified:

```
OPPORTUNITY PATTERNS:

IF segment_x_activation > 2x_average:
    → Opportunity: "High-activation segment underserved"
    → Action: Double down on segment_x acquisition

IF feature_y_users_retain > 1.5x_average:
    → Opportunity: "Sticky feature underutilized"
    → Action: Surface feature_y earlier in journey

IF channel_z_cac < 0.5x_average:
    → Opportunity: "Efficient channel underinvested"
    → Action: Scale channel_z spend

IF referrer_cohort_ltv > 1.3x_average:
    → Opportunity: "Referral flywheel potential"
    → Action: Invest in referral program
```

### Phase 5: Experiment Recommendations

```
ai.recommend_experiments({
  blockers: identified_blockers,
  opportunities: identified_opportunities,
  constraints: {
    risk_tolerance: "medium",
    resource_availability: "limited",
    time_horizon: "quarter"
  }
})
```

## Response Format

```json
{
  "analysisDate": "2024-02-15",
  "period": "last_90_days",
  "segment": "all",
  
  "growthHealth": {
    "overallScore": 62,
    "trend": "flat",
    "primaryBottleneck": "activation",
    "biggestOpportunity": "retention"
  },
  
  "funnelAnalysis": {
    "acquisition": {
      "rate": 0.038,
      "benchmark": 0.04,
      "status": "on_target",
      "volume": 45000,
      "trend": "stable"
    },
    "activation": {
      "rate": 0.18,
      "benchmark": 0.30,
      "status": "below_benchmark",
      "volume": 1710,
      "trend": "declining",
      "dropOffPoints": [
        { "step": "connect_integration", "dropOff": 0.35 },
        { "step": "invite_teammate", "dropOff": 0.28 }
      ]
    },
    "retention": {
      "week1": 0.52,
      "week4": 0.38,
      "week12": 0.28,
      "benchmark_week4": 0.35,
      "status": "on_target",
      "trend": "improving"
    },
    "revenue": {
      "conversionRate": 0.032,
      "benchmark": 0.035,
      "status": "near_benchmark",
      "arpu": 89,
      "trend": "stable"
    },
    "referral": {
      "viralCoefficient": 0.15,
      "benchmark": 0.25,
      "status": "below_benchmark",
      "referralRate": 0.08
    }
  },
  
  "blockers": [
    {
      "rank": 1,
      "stage": "activation",
      "blocker": "Integration connection friction",
      "evidence": "35% drop-off at integration step, 3x higher than benchmark",
      "impact": {
        "usersAffected": 598,
        "revenueImpact": 53000,
        "confidence": 0.85
      },
      "rootCauses": [
        "OAuth flow requires 6 clicks vs industry avg of 2",
        "No progress indication during sync",
        "Error messages non-actionable"
      ],
      "skillTrigger": "plg/friction_detector"
    },
    {
      "rank": 2,
      "stage": "activation", 
      "blocker": "Team invite abandonment",
      "evidence": "28% drop-off at invite step, users who invite retain 2x better",
      "impact": {
        "usersAffected": 421,
        "revenueImpact": 38000,
        "confidence": 0.78
      },
      "rootCauses": [
        "Invite step feels mandatory but isn't",
        "No clear value prop for inviting",
        "Bulk invite UX cumbersome"
      ],
      "skillTrigger": "plg/quick_win_generator"
    }
  ],
  
  "opportunities": [
    {
      "rank": 1,
      "stage": "retention",
      "opportunity": "Dashboard users retain 2x better",
      "evidence": "Users who create custom dashboard in week 1: 68% week4 retention vs 32% average",
      "potential": {
        "targetAudience": 850,
        "estimatedLift": "15% week4 retention",
        "revenueImpact": 72000
      },
      "action": "Surface dashboard creation earlier, add templates",
      "skillTrigger": "plg/habit_loop_builder"
    },
    {
      "rank": 2,
      "stage": "acquisition",
      "opportunity": "LinkedIn organic underinvested",
      "evidence": "12% of traffic, 22% of conversions, CPL 40% below average",
      "potential": {
        "estimatedLift": "20% more signups",
        "requiredInvestment": "2x content volume"
      },
      "action": "Increase LinkedIn content cadence and promotion",
      "skillTrigger": "marketing/channel_optimizer"
    }
  ],
  
  "recommendations": [
    {
      "priority": "critical",
      "action": "Simplify OAuth integration flow",
      "expectedImpact": "+8% activation rate",
      "effort": "medium",
      "timeToImpact": "4 weeks",
      "owner": "Product + Engineering"
    },
    {
      "priority": "high",
      "action": "Add dashboard templates to onboarding",
      "expectedImpact": "+15% week4 retention",
      "effort": "low",
      "timeToImpact": "2 weeks",
      "owner": "Product"
    },
    {
      "priority": "medium",
      "action": "Make team invite optional with clear skip",
      "expectedImpact": "+5% activation rate",
      "effort": "low",
      "timeToImpact": "1 week",
      "owner": "Product"
    }
  ],
  
  "experiments": [
    {
      "hypothesis": "Reducing OAuth steps from 6 to 2 will increase integration completion by 40%",
      "metric": "integration_completion_rate",
      "baselineRate": 0.65,
      "targetRate": 0.91,
      "sampleSize": 2000,
      "duration": "14 days",
      "skillTrigger": "product_ops/experimentation"
    },
    {
      "hypothesis": "Adding 'Create Dashboard' CTA to welcome email will increase dashboard creation by 25%",
      "metric": "week1_dashboard_creation",
      "baselineRate": 0.22,
      "targetRate": 0.275,
      "sampleSize": 5000,
      "duration": "21 days",
      "skillTrigger": "product_ops/experimentation"
    }
  ],
  
  "exitState": "blocker_identified"
}
```

## Guardrails

### Statistical Rigor
- Minimum sample size for conclusions: 100 users per segment
- Confidence threshold for blocker identification: 80%
- Flag low-confidence insights clearly
- Use proper cohort comparison (same acquisition period)

### Diagnosis Quality
- Distinguish correlation from causation
- Consider seasonality in period comparisons
- Account for product changes in the analysis period
- Validate blockers with qualitative data when possible

### Recommendation Safety
- Never recommend changes that could harm existing user experience
- Prioritize reversible experiments over permanent changes
- Consider downstream effects on other funnel stages
- Include effort estimation to enable prioritization

### Data Requirements
- Minimum 30 days of data for trend analysis
- Minimum 90 days for cohort analysis
- Flag data gaps that affect confidence
- Require funnel instrumentation completeness > 90%

## Integration Points

| Funnel Stage | Primary Skills | Trigger Condition |
|--------------|---------------|-------------------|
| Acquisition | `marketing/channel_optimizer`, `marketing/conversion_optimizer` | CAC spike, conversion drop |
| Activation | `plg/friction_detector`, `plg/quick_win_generator` | Activation < 20% |
| Retention | `plg/habit_loop_builder`, `customer_success/onboarding_health` | Week4 retention < 35% |
| Revenue | `monetization/pricing_optimization`, `plg/reverse_trial` | Conversion < 2% |
| Referral | `plg/network_effect_amplifier`, `marketing/referral_optimizer` | Viral coefficient < 0.2 |
| All | `product_ops/experimentation`, `product_ops/impact_analyzer` | Experiment ready |
