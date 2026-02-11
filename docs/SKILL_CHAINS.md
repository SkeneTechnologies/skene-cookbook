# Skill Chain Cookbook
## 10+ Ready-to-Use Recipes

This cookbook provides proven skill chain recipes you can deploy immediately. Each recipe includes:
- **Use case** — What problem it solves
- **Skills** — Which skills to chain together
- **ROI** — Expected time/cost savings
- **Step-by-step instructions** — Copy-paste examples
- **Expected outcomes** — What success looks like

---

## Recipe 1: Sales Deal Qualification Pipeline

**Use Case:** Automatically qualify, score, and route leads with recommended next actions
**Skills:** 5 chained skills
**Time:** 30-60 seconds per lead (was 2-3 hours)
**ROI:** $20K-$40K/month for 50-lead sales team

### The Chain

```
lead_qualification → opportunity_scoring → deal_inspection →
next_best_action → content_recommender
```

### How It Works

1. **lead_qualification** — Applies MEDDIC/BANT framework, determines if lead is qualified
2. **opportunity_scoring** — Scores qualified leads on fit, urgency, budget
3. **deal_inspection** — Analyzes deal health, identifies risks
4. **next_best_action** — Recommends specific actions for rep
5. **content_recommender** — Suggests relevant case studies, decks

### Setup Instructions

#### Step 1: Install RevOps Skills

```bash
npx skills-directory install --target all --domain revops
```

#### Step 2: Configure Lead Qualification Entry Point

```json
{
  "skill": "lead_qualification",
  "input": {
    "leadId": "{{trigger.leadId}}",
    "framework": "MEDDIC",
    "sources": ["CRM", "enrichment_data", "website_activity"]
  },
  "exit_routing": {
    "qualified": "opportunity_scoring",
    "nurture": "nurture_campaign",
    "disqualified": "archive_lead"
  }
}
```

#### Step 3: Chain to Opportunity Scoring

```json
{
  "skill": "opportunity_scoring",
  "input": {
    "opportunityId": "{{previous.opportunityId}}",
    "qualificationData": "{{previous.output}}",
    "scoringModel": "weighted"
  },
  "exit_routing": {
    "high_score": "deal_inspection",
    "medium_score": "next_best_action",
    "low_score": "nurture_campaign"
  }
}
```

#### Step 4: Add Deal Inspection

```json
{
  "skill": "deal_inspection",
  "input": {
    "dealId": "{{previous.dealId}}",
    "depth": "comprehensive"
  },
  "exit_routing": {
    "healthy": "next_best_action",
    "at_risk": "escalation_manager",
    "blocked": "deal_surgery"
  }
}
```

#### Step 5: Route to Next Best Action

```json
{
  "skill": "next_best_action",
  "input": {
    "context": "{{chain.all_previous_outputs}}",
    "repProfile": "{{user.profile}}",
    "priority": "close_deal"
  },
  "exit_routing": {
    "action_recommended": "content_recommender",
    "needs_manager": "escalation_manager"
  }
}
```

#### Step 6: Recommend Content

```json
{
  "skill": "content_recommender",
  "input": {
    "dealContext": "{{chain.context}}",
    "buyerPersona": "{{lead.persona}}",
    "dealStage": "{{deal.stage}}"
  },
  "output": "send_to_rep"
}
```

### Testing the Chain

```bash
# Test with sample lead data
curl -X POST http://localhost:3000/api/chains/sales-qualification \
  -H "Content-Type: application/json" \
  -d '{
    "leadId": "test-lead-123",
    "leadData": {
      "company": "Acme Corp",
      "revenue": "$50M",
      "employees": 250,
      "industry": "SaaS"
    }
  }'
```

### Expected Output

```json
{
  "qualified": true,
  "score": 85,
  "tier": "high_value",
  "risks": [],
  "nextActions": [
    "Schedule discovery call",
    "Send ROI calculator",
    "Introduce solutions engineer"
  ],
  "recommendedContent": [
    "Case Study: Similar company in SaaS",
    "ROI Calculator: Enterprise tier",
    "Demo Video: Platform overview"
  ],
  "timeline": "Move to demo within 5 days"
}
```

### Monitoring & Metrics

Track these KPIs:

- **Lead-to-opportunity rate:** Target > 25%
- **Time saved per lead:** Target 90%+ reduction
- **Opportunity quality:** Track close rates
- **Rep satisfaction:** Survey reps on lead quality

### Expected Outcomes

- **Week 1:** Chain deployed, processing 10-20 leads
- **Week 2:** Reps report 50%+ time savings on qualification
- **Month 1:** 25%+ lead-to-opportunity conversion rate
- **Month 3:** $25K+ value delivered in time savings

---

## Recipe 2: Customer Churn Prevention Pipeline

**Use Case:** Predict churn risk 60-90 days early and trigger intervention playbooks
**Skills:** 4 chained skills
**Time:** Real-time monitoring vs quarterly reviews
**ROI:** $400K+ ARR saved annually

### The Chain

```
health_scoring → churn_prediction → risk_mitigation_playbook →
escalation_manager
```

### How It Works

1. **health_scoring** — Continuously monitors account health signals
2. **churn_prediction** — ML-based prediction of churn risk 60-90 days out
3. **risk_mitigation_playbook** — Executes tailored intervention strategies
4. **escalation_manager** — Alerts CSM and triggers manager involvement if needed

### Setup Instructions

#### Step 1: Install Customer Success Skills

```bash
npx skills-directory install --target all --domain customer_success
```

#### Step 2: Configure Health Scoring (Continuous)

```json
{
  "skill": "health_scoring",
  "trigger": "scheduled",
  "frequency": "daily",
  "input": {
    "accountIds": "{{all_active_accounts}}",
    "signals": [
      "product_usage",
      "support_tickets",
      "nps_score",
      "contract_value",
      "engagement_metrics"
    ]
  },
  "exit_routing": {
    "healthy": "log_and_continue",
    "at_risk": "churn_prediction",
    "critical": "immediate_escalation"
  }
}
```

#### Step 3: Chain to Churn Prediction

```json
{
  "skill": "churn_prediction",
  "input": {
    "accountId": "{{previous.accountId}}",
    "healthData": "{{previous.healthScore}}",
    "historicalData": true,
    "predictionWindow": "90_days"
  },
  "exit_routing": {
    "high_risk": "risk_mitigation_playbook",
    "medium_risk": "risk_mitigation_playbook",
    "low_risk": "monitor_only"
  }
}
```

#### Step 4: Execute Risk Mitigation

```json
{
  "skill": "risk_mitigation_playbook",
  "input": {
    "accountId": "{{chain.accountId}}",
    "riskLevel": "{{previous.riskScore}}",
    "riskFactors": "{{previous.factors}}",
    "playbookType": "retention"
  },
  "actions": [
    "Schedule executive business review",
    "Conduct product usage analysis",
    "Offer training/onboarding refresh",
    "Introduce customer success resources"
  ],
  "exit_routing": {
    "playbook_started": "escalation_manager",
    "needs_custom_plan": "csm_intervention"
  }
}
```

#### Step 5: Escalate if Needed

```json
{
  "skill": "escalation_manager",
  "input": {
    "accountId": "{{chain.accountId}}",
    "context": "{{chain.all_data}}",
    "urgency": "{{previous.riskLevel}}"
  },
  "notifications": [
    "Assigned CSM",
    "CSM Manager",
    "VP Customer Success"
  ]
}
```

### Monitoring Dashboard

Create a real-time dashboard tracking:

```
┌─────────────────────────────────────────────┐
│ Churn Prevention Dashboard                  │
├─────────────────────────────────────────────┤
│ Accounts Monitored: 347                     │
│ At-Risk (High): 12                          │
│ At-Risk (Medium): 28                        │
│ Playbooks Active: 18                        │
│ ARR at Risk: $450K                          │
│ ARR Saved (QTD): $180K                      │
└─────────────────────────────────────────────┘
```

### Expected Outcomes

- **Week 1:** Health scoring running on all accounts
- **Week 2:** First at-risk accounts identified
- **Month 1:** 3-5 accounts saved from churn
- **Quarter 1:** $100K-$200K ARR saved

---

## Recipe 3: Financial Intelligence Dashboard

**Use Case:** Real-time CFO dashboard with automated board reporting
**Skills:** 5 chained skills
**Time:** Real-time updates vs monthly 40-hour manual process
**ROI:** $50K+/month in finance team time

### The Chain

```
arr_waterfall → burn_rate_monitor → magic_number →
investor_metrics → scenario_planner
```

### How It Works

1. **arr_waterfall** — Tracks ARR movements (new, expansion, churn, contraction)
2. **burn_rate_monitor** — Monitors cash burn and runway
3. **magic_number** — Calculates sales efficiency
4. **investor_metrics** — Compiles key metrics (CAC, LTV, Rule of 40)
5. **scenario_planner** — Models "what if" scenarios

### Setup Instructions

#### Step 1: Install FinOps Skills

```bash
npx skills-directory install --target all --domain finops
```

#### Step 2: Configure ARR Waterfall (Real-time)

```json
{
  "skill": "arr_waterfall",
  "trigger": "data_change",
  "input": {
    "period": "current_month",
    "sources": ["billing", "crm", "contracts"],
    "granularity": "daily"
  },
  "output_to": "burn_rate_monitor"
}
```

#### Step 3: Monitor Burn Rate

```json
{
  "skill": "burn_rate_monitor",
  "input": {
    "arrData": "{{previous.arr}}",
    "expenses": "{{accounting.expenses}}",
    "runway_threshold": 12
  },
  "alerts": {
    "runway_below_12_months": "immediate",
    "burn_increasing_20_percent": "warning"
  },
  "output_to": "magic_number"
}
```

#### Step 4: Calculate Sales Efficiency

```json
{
  "skill": "magic_number",
  "input": {
    "newARR": "{{arr_waterfall.new}}",
    "salesMarketing": "{{expenses.sales_marketing}}",
    "period": "quarter"
  },
  "benchmark": 1.0,
  "output_to": "investor_metrics"
}
```

#### Step 5: Compile Investor Metrics

```json
{
  "skill": "investor_metrics",
  "input": {
    "allData": "{{chain.all_previous}}",
    "includeMetrics": [
      "ARR",
      "Net Revenue Retention",
      "CAC",
      "LTV",
      "LTV:CAC Ratio",
      "Magic Number",
      "Burn Multiple",
      "Rule of 40",
      "Gross Margin"
    ]
  },
  "output_to": "scenario_planner"
}
```

#### Step 6: Enable Scenario Planning

```json
{
  "skill": "scenario_planner",
  "input": {
    "baselineData": "{{previous.metrics}}",
    "scenarios": [
      {
        "name": "aggressive_growth",
        "assumptions": {"headcount_increase": 30, "arr_growth": 100}
      },
      {
        "name": "profitable_growth",
        "assumptions": {"headcount_increase": 15, "arr_growth": 50}
      }
    ]
  }
}
```

### One-Click Board Report

```bash
# Generate board report
npx skills-directory run-chain financial-intelligence \
  --output board-report \
  --format pdf
```

### Expected Outcomes

- **Day 1:** Dashboard showing real-time metrics
- **Week 1:** CFO using for daily decision-making
- **Month 1:** First board report auto-generated
- **Quarter 1:** 90% reduction in manual financial reporting

---

## Recipe 4: Growth Optimization Engine

**Use Case:** Continuous A/B testing and conversion optimization
**Skills:** 6 chained skills
**Time:** 10-15 experiments/month vs 2-4
**ROI:** 15-25% conversion lift

### The Chain

```
signup_flow_cro → page_cro → ab_test_setup →
analytics_tracking → activation_metrics → feature_adoption
```

### How It Works

1. **signup_flow_cro** — Optimizes signup conversion
2. **page_cro** — Optimizes landing page conversion
3. **ab_test_setup** — Configures and launches A/B tests
4. **analytics_tracking** — Tracks all metrics
5. **activation_metrics** — Monitors activation funnel
6. **feature_adoption** — Tracks feature usage

### Setup Instructions

#### Step 1: Install Marketing/PLG Skills

```bash
npx skills-directory install --target all --domain marketing plg
```

#### Step 2: Start with Signup Flow Optimization

```json
{
  "skill": "signup_flow_cro",
  "input": {
    "currentFlow": "{{app.signup_flow}}",
    "conversionGoal": "completed_signup",
    "optimizationFocus": ["friction_points", "form_fields", "social_proof"]
  },
  "exit_routing": {
    "recommendations_ready": "ab_test_setup"
  }
}
```

#### Step 3: Run Parallel Page Optimization

```json
{
  "skill": "page_cro",
  "input": {
    "pages": ["homepage", "pricing", "features"],
    "goal": "trial_signup",
    "analyze": ["copy", "cta", "layout", "images"]
  },
  "exit_routing": {
    "recommendations_ready": "ab_test_setup"
  }
}
```

#### Step 4: Automated A/B Test Setup

```json
{
  "skill": "ab_test_setup",
  "input": {
    "recommendations": "{{previous.all_recommendations}}",
    "testPlatform": "optimizely",
    "traffic_split": "50/50",
    "duration": "2_weeks",
    "min_sample_size": 1000
  },
  "exit_routing": {
    "test_launched": "analytics_tracking"
  }
}
```

#### Step 5: Track Everything

```json
{
  "skill": "analytics_tracking",
  "input": {
    "events": [
      "page_view",
      "signup_started",
      "signup_completed",
      "feature_used",
      "trial_converted"
    ],
    "destinations": ["mixpanel", "amplitude", "datawarehouse"]
  }
}
```

#### Step 6: Monitor Activation & Adoption

```json
{
  "skill": "activation_metrics",
  "input": {
    "activationDefinition": "{{company.aha_moment}}",
    "timeWindow": "7_days"
  }
},
{
  "skill": "feature_adoption",
  "input": {
    "features": "{{product.feature_list}}",
    "cohorts": ["week_1", "week_2", "month_1"]
  }
}
```

### Growth Experimentation Dashboard

```
┌─────────────────────────────────────────────┐
│ Active Experiments                          │
├─────────────────────────────────────────────┤
│ Signup Flow: 3-step vs 1-step              │
│   Status: Running | Day 8 of 14            │
│   Winner: 1-step (+23% conversion) ✓       │
│                                             │
│ Pricing Page: New layout                   │
│   Status: Running | Day 3 of 14            │
│   Current: +8% trial signups               │
│                                             │
│ Homepage Hero: Value prop test             │
│   Status: Complete                          │
│   Winner: "Build in days" (+15%) ✓         │
└─────────────────────────────────────────────┘
```

### Expected Outcomes

- **Week 1:** First 3 experiments launched
- **Month 1:** 10-15 tests running simultaneously
- **Quarter 1:** 15-25% average conversion lift
- **Quarter 2:** 4x increase in experiment velocity

---

## Recipe 5: Content Marketing Automation

**Use Case:** End-to-end content creation, distribution, and optimization
**Skills:** 7 chained skills
**Time:** 2-3 hours per piece vs 8-12 hours
**ROI:** 2.5x content volume, 40% traffic increase

### The Chain

```
content_research_writer → copywriting → seo_audit →
social_content_generator → email_sequence →
analytics_tracking → social_listening_analyzer
```

### How It Works

1. **content_research_writer** — Researches topic, generates outline & draft
2. **copywriting** — Refines copy, optimizes for readability
3. **seo_audit** — Ensures SEO best practices
4. **social_content_generator** — Creates social posts
5. **email_sequence** — Generates email promotion sequence
6. **analytics_tracking** — Tracks performance
7. **social_listening_analyzer** — Monitors engagement

### Setup Instructions

#### Step 1: Install Marketing Skills

```bash
npx skills-directory install --target all --domain marketing
```

#### Step 2: Configure Content Research & Writing

```json
{
  "skill": "content_research_writer",
  "input": {
    "topic": "{{user_input.topic}}",
    "audience": "{{company.buyer_persona}}",
    "contentType": "blog_post",
    "targetLength": 1500,
    "includeExamples": true
  },
  "exit_routing": {
    "draft_complete": "copywriting"
  }
}
```

#### Step 3: Refine Copy

```json
{
  "skill": "copywriting",
  "input": {
    "draft": "{{previous.output}}",
    "tone": "professional_friendly",
    "optimizeFor": ["clarity", "engagement", "cta_conversion"]
  },
  "exit_routing": {
    "copy_refined": "seo_audit"
  }
}
```

#### Step 4: SEO Optimization

```json
{
  "skill": "seo_audit",
  "input": {
    "content": "{{previous.output}}",
    "targetKeyword": "{{research.primary_keyword}}",
    "checks": [
      "keyword_density",
      "meta_description",
      "headings",
      "internal_links",
      "readability"
    ]
  },
  "exit_routing": {
    "seo_optimized": "social_content_generator"
  }
}
```

#### Step 5: Generate Social Content

```json
{
  "skill": "social_content_generator",
  "input": {
    "article": "{{chain.final_content}}",
    "platforms": ["twitter", "linkedin", "facebook"],
    "postsPerPlatform": 3,
    "includeImages": true
  },
  "exit_routing": {
    "social_content_ready": "email_sequence"
  }
}
```

#### Step 6: Create Email Sequence

```json
{
  "skill": "email_sequence",
  "input": {
    "content": "{{chain.final_content}}",
    "sequenceType": "nurture",
    "emailCount": 3,
    "spacing": "3_days"
  }
}
```

#### Step 7: Track & Listen

```json
{
  "skill": "analytics_tracking",
  "input": {
    "contentId": "{{chain.contentId}}",
    "metrics": ["views", "time_on_page", "conversions", "social_shares"]
  }
},
{
  "skill": "social_listening_analyzer",
  "input": {
    "contentUrl": "{{chain.publish_url}}",
    "keywords": "{{chain.target_keywords}}",
    "sentiment": true
  }
}
```

### Content Pipeline Dashboard

```
┌─────────────────────────────────────────────┐
│ This Month: Content Production             │
├─────────────────────────────────────────────┤
│ Published: 22 articles (↑ 2.5x)            │
│ Organic Traffic: +43%                      │
│ Social Engagement: 12K interactions        │
│ Email CTR: 4.2% (↑ 0.8%)                   │
│ Time Saved: 180 hours                      │
└─────────────────────────────────────────────┘
```

### Expected Outcomes

- **Week 1:** First 3 pieces published
- **Month 1:** 20+ pieces published
- **Quarter 1:** 40% increase in organic traffic
- **Quarter 2:** Content team 3x more productive

---

## Recipe 6-10: Quick Reference

### Recipe 6: Customer Onboarding Automation
```
onboarding_health → guided_setup_wizard → milestone_celebration →
time_to_value → activation_metrics
```
**ROI:** 50% faster time-to-value, 30% higher activation

---

### Recipe 7: Support Ticket Triage & Resolution
```
support_ticket_triage → support_resolution_suggester →
support_kb_gap_finder → support_bug_linker
```
**ROI:** 40% faster resolution, 60% ticket deflection

---

### Recipe 8: Partnership Deal Flow
```
partner_mapping → nearbound_signal → co_sell_trigger →
deal_registration → partner_influenced_revenue
```
**ROI:** 25% more partner-sourced pipeline

---

### Recipe 9: Pricing & Packaging Optimization
```
pricing_strategy → packaging_optimizer → price_experimentation →
upgrade_trigger → consumption_analyzer
```
**ROI:** 15-25% revenue per customer increase

---

### Recipe 10: Product Analytics Intelligence
```
product_analytics → feature_adoption → friction_detector →
pql_scoring → expansion_playbook
```
**ROI:** 2x product-led pipeline generation

---

## Phase 2: High-Confidence Recipes (11-28)

These recipes expand into new domains with 95%+ skill coverage validated against the library.

---

## Recipe 11: Freemium Conversion Optimization

**Use Case:** Optimize trial-to-paid conversion for freemium products with automated upgrade triggers and self-serve expansion workflows
**Skills:** 6 chained skills
**Time:** Real-time monitoring vs manual quarterly reviews
**ROI:** 35% trial-to-paid lift, 25% faster conversion cycle, $300K-$800K ARR increase

### The Chain

```
pql_scoring → onboarding_health → feature_adoption →
upgrade_trigger → paywall_upgrade_cro → self_serve_expansion
```

### How It Works

1. **pql_scoring** — Scores trial users based on product engagement, feature usage, and behavioral fit
2. **onboarding_health** — Monitors trial health and identifies at-risk users early
3. **feature_adoption** — Tracks which premium features drive conversion decisions
4. **upgrade_trigger** — Identifies optimal moments to surface upgrade prompts
5. **paywall_upgrade_cro** — A/B tests paywall messaging, pricing display, and call-to-action
6. **self_serve_expansion** — Enables frictionless self-service plan upgrades

### Setup Instructions

#### Step 1: Install PLG & Monetization Skills

```bash
npx skills-directory install --target all --domain plg monetization
```

#### Step 2: Configure PQL Scoring

```json
{
  "skill": "pql_scoring",
  "trigger": "user_event",
  "input": {
    "userId": "{{trigger.userId}}",
    "events": ["feature_used", "time_spent", "invites_sent", "integration_added"],
    "scoringModel": "engagement_based",
    "threshold": 70
  },
  "exit_routing": {
    "high_score": "onboarding_health",
    "low_score": "activation_campaign"
  }
}
```

#### Step 3: Monitor Onboarding Health

```json
{
  "skill": "onboarding_health",
  "input": {
    "userId": "{{previous.userId}}",
    "pqlScore": "{{previous.score}}",
    "trialDaysRemaining": "{{user.trial_days_left}}",
    "healthSignals": ["login_frequency", "feature_usage", "team_invites", "setup_completion"]
  },
  "exit_routing": {
    "healthy": "feature_adoption",
    "at_risk": "retention_campaign",
    "churned": "win_back_campaign"
  }
}
```

#### Step 4: Track Feature Adoption

```json
{
  "skill": "feature_adoption",
  "input": {
    "userId": "{{chain.userId}}",
    "onboardingData": "{{previous.health_data}}",
    "premiumFeatures": ["advanced_analytics", "team_collaboration", "api_access", "custom_integrations"],
    "trackingWindow": "7_days"
  },
  "exit_routing": {
    "premium_used": "upgrade_trigger",
    "basic_only": "feature_education"
  }
}
```

#### Step 5: Trigger Upgrade Prompts

```json
{
  "skill": "upgrade_trigger",
  "input": {
    "userId": "{{chain.userId}}",
    "adoptionData": "{{previous.feature_usage}}",
    "pqlScore": "{{chain.pql_score}}",
    "triggerType": "feature_limit",
    "timing": "optimal_moment"
  },
  "exit_routing": {
    "trigger_sent": "paywall_upgrade_cro",
    "wait": "monitor_only"
  }
}
```

#### Step 6: Optimize Paywall Experience

```json
{
  "skill": "paywall_upgrade_cro",
  "input": {
    "userId": "{{chain.userId}}",
    "context": "{{chain.all_data}}",
    "variants": ["value_focused", "urgency_focused", "social_proof", "comparison_table"],
    "testDuration": "14_days"
  },
  "exit_routing": {
    "converted": "self_serve_expansion",
    "dismissed": "follow_up_sequence"
  }
}
```

#### Step 7: Enable Self-Serve Expansion

```json
{
  "skill": "self_serve_expansion",
  "input": {
    "userId": "{{chain.userId}}",
    "selectedPlan": "{{previous.plan_choice}}",
    "paymentMethod": "{{user.payment_method}}",
    "prorateOption": true
  },
  "output": "send_to_billing"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/freemium-conversion \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "test-user-123",
    "trialData": {
      "daysInTrial": 10,
      "featureUsage": {
        "basic": 15,
        "advanced": 3,
        "premium": 1
      },
      "teamSize": 1,
      "setupComplete": true
    }
  }'
```

### Expected Output

```json
{
  "converted": true,
  "pqlScore": 87,
  "onboardingHealth": "healthy",
  "premiumFeaturesUsed": ["advanced_analytics"],
  "triggerType": "feature_limit",
  "paywallVariant": "value_focused",
  "selectedPlan": "pro_monthly",
  "conversionTime": "Day 11 of 14",
  "estimatedLTV": "$2,400",
  "timeline": "Converted within optimal window"
}
```

### Monitoring & Metrics

Track these KPIs:

- **Trial-to-Paid Rate:** Target > 30% (baseline ~5-10%)
- **Time to Conversion:** Target < 10 days (baseline ~12 days)
- **Paywall Conversion Rate:** Target > 15%
- **Self-Serve Upgrade Rate:** Track monthly expansion revenue
- **PQL Score Distribution:** Monitor score accuracy vs actual conversions

### Expected Outcomes

- **Week 1:** Chain deployed, monitoring 100+ trial users
- **Month 1:** 35% trial-to-paid improvement vs. control group
- **Quarter 1:** $300K-$800K incremental ARR from improved conversions
- **Quarter 2:** Self-serve expansion driving 20%+ of new ARR

---

## Recipe 12: Usage-Based Pricing Engine

**Use Case:** Implement consumption-based pricing with automated metering, overage prediction, and billing workflows
**Skills:** 6 chained skills
**Time:** Real-time usage tracking vs monthly manual reconciliation
**ROI:** 25% revenue per customer increase, 15% churn reduction, $400K-$1M ARR lift

### The Chain

```
usage_metering → consumption_analyzer → overage_predictor →
dunning_automation → limit_notification → invoice_explainer
```

### How It Works

1. **usage_metering** — Tracks real-time product usage across all billing dimensions
2. **consumption_analyzer** — Analyzes usage patterns, identifies trends and anomalies
3. **overage_predictor** — Predicts when customers will exceed plan limits
4. **dunning_automation** — Automates payment collection and retry logic
5. **limit_notification** — Alerts customers before hitting usage limits
6. **invoice_explainer** — Generates detailed, easy-to-understand invoices

### Setup Instructions

#### Step 1: Install Monetization Skills

```bash
npx skills-directory install --target all --domain monetization
```

#### Step 2: Configure Usage Metering

```json
{
  "skill": "usage_metering",
  "trigger": "usage_event",
  "input": {
    "accountId": "{{trigger.accountId}}",
    "metricType": "{{trigger.metric}}",
    "dimensions": ["api_calls", "storage_gb", "compute_hours", "seats"],
    "aggregationWindow": "hourly",
    "granularity": "high"
  },
  "exit_routing": {
    "metered": "consumption_analyzer"
  }
}
```

#### Step 3: Analyze Consumption Patterns

```json
{
  "skill": "consumption_analyzer",
  "input": {
    "accountId": "{{previous.accountId}}",
    "usageData": "{{previous.metrics}}",
    "analysisWindow": "30_days",
    "compareWith": ["plan_limits", "historical_usage", "cohort_avg"]
  },
  "exit_routing": {
    "within_limits": "monitor_only",
    "approaching_limit": "overage_predictor",
    "exceeded_limit": "dunning_automation"
  }
}
```

#### Step 4: Predict Overage Events

```json
{
  "skill": "overage_predictor",
  "input": {
    "accountId": "{{chain.accountId}}",
    "consumptionTrend": "{{previous.trend}}",
    "planLimits": "{{account.plan_limits}}",
    "predictionHorizon": "7_days",
    "confidence": "high"
  },
  "exit_routing": {
    "overage_likely": "limit_notification",
    "within_buffer": "monitor_only"
  }
}
```

#### Step 5: Send Limit Notifications

```json
{
  "skill": "limit_notification",
  "input": {
    "accountId": "{{chain.accountId}}",
    "usagePercent": "{{previous.usage_percent}}",
    "estimatedOverage": "{{previous.overage_amount}}",
    "notificationTiming": ["75_percent", "90_percent", "100_percent"],
    "includeUpgradeOptions": true
  },
  "exit_routing": {
    "notified": "dunning_automation",
    "upgraded": "usage_metering"
  }
}
```

#### Step 6: Automate Payment Collection

```json
{
  "skill": "dunning_automation",
  "input": {
    "accountId": "{{chain.accountId}}",
    "invoiceAmount": "{{chain.total_amount}}",
    "paymentMethod": "{{account.payment_method}}",
    "retryStrategy": "exponential_backoff",
    "maxRetries": 3
  },
  "exit_routing": {
    "payment_successful": "invoice_explainer",
    "payment_failed": "billing_alert"
  }
}
```

#### Step 7: Generate Invoice Explanation

```json
{
  "skill": "invoice_explainer",
  "input": {
    "accountId": "{{chain.accountId}}",
    "usageData": "{{chain.all_usage}}",
    "charges": "{{previous.charges}}",
    "format": "detailed_breakdown",
    "includeComparisons": true
  },
  "output": "send_to_customer"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/usage-billing \
  -H "Content-Type: application/json" \
  -d '{
    "accountId": "test-account-456",
    "usageData": {
      "api_calls": 950000,
      "storage_gb": 450,
      "compute_hours": 1800,
      "plan_limit": 1000000
    },
    "billingPeriod": "2026-02"
  }'
```

### Expected Output

```json
{
  "metered": true,
  "usagePercent": 95,
  "overagePredicted": true,
  "estimatedOverage": "$250",
  "notificationSent": true,
  "paymentProcessed": true,
  "invoiceGenerated": true,
  "breakdown": {
    "base_plan": "$99",
    "overage_charges": "$250",
    "total": "$349"
  },
  "nextAction": "Monitor usage next cycle"
}
```

### Monitoring & Metrics

Track these KPIs:

- **Revenue Per Customer:** Target 25% increase from usage-based pricing
- **Payment Success Rate:** Target > 95%
- **Overage Notification Effectiveness:** Track upgrade rate after notifications
- **Invoice Dispute Rate:** Target < 2%
- **Customer Satisfaction with Billing:** Track NPS on billing experience

### Expected Outcomes

- **Week 1:** Usage metering deployed, tracking 50+ accounts
- **Month 1:** 25% revenue increase from usage-based charges
- **Quarter 1:** 15% churn reduction due to transparent pricing
- **Quarter 2:** $400K-$1M ARR lift from consumption pricing model

---

## Recipe 13: Product-Led Sales Handoff

**Use Case:** Bridge self-serve and sales motions by automatically routing product-qualified leads to sales with full context
**Skills:** 6 chained skills
**Time:** Automated PQL detection vs manual review (2+ hours per lead)
**ROI:** 3x PQL-to-opportunity conversion, $1M-$3M pipeline capture, 40% faster sales cycles

### The Chain

```
pql_scoring → usage_depth_analyzer → expansion_playbook →
handoff_orchestration → cpq_quote_generator → deal_inspection
```

### How It Works

1. **pql_scoring** — Identifies product-qualified leads based on usage patterns and engagement
2. **usage_depth_analyzer** — Analyzes depth of product adoption and power user behaviors
3. **expansion_playbook** — Recommends expansion strategies based on usage patterns
4. **handoff_orchestration** — Coordinates seamless handoff from product to sales
5. **cpq_quote_generator** — Auto-generates quotes based on usage and expansion opportunity
6. **deal_inspection** — Validates deal health and identifies potential blockers

### Setup Instructions

#### Step 1: Install PLG & RevOps Skills

```bash
npx skills-directory install --target all --domain plg revops
```

#### Step 2: Configure PQL Scoring

```json
{
  "skill": "pql_scoring",
  "trigger": "scheduled",
  "frequency": "daily",
  "input": {
    "accountIds": "{{all_active_accounts}}",
    "signals": [
      "feature_usage",
      "team_size",
      "integration_count",
      "api_usage",
      "storage_consumption"
    ],
    "threshold": 75,
    "scoringModel": "product_led"
  },
  "exit_routing": {
    "pql_qualified": "usage_depth_analyzer",
    "not_qualified": "nurture_sequence"
  }
}
```

#### Step 3: Analyze Usage Depth

```json
{
  "skill": "usage_depth_analyzer",
  "input": {
    "accountId": "{{previous.accountId}}",
    "pqlScore": "{{previous.score}}",
    "analysisDepth": "comprehensive",
    "lookbackWindow": "90_days",
    "metrics": ["feature_breadth", "power_user_count", "collaboration_score"]
  },
  "exit_routing": {
    "expansion_ready": "expansion_playbook",
    "early_stage": "product_education"
  }
}
```

#### Step 4: Generate Expansion Playbook

```json
{
  "skill": "expansion_playbook",
  "input": {
    "accountId": "{{chain.accountId}}",
    "usageAnalysis": "{{previous.analysis}}",
    "currentPlan": "{{account.plan}}",
    "expansionVectors": ["seats", "features", "usage_tier", "enterprise_upgrade"],
    "targetARR": "calculate"
  },
  "exit_routing": {
    "playbook_ready": "handoff_orchestration",
    "needs_enrichment": "data_enrichment"
  }
}
```

#### Step 5: Orchestrate Sales Handoff

```json
{
  "skill": "handoff_orchestration",
  "input": {
    "accountId": "{{chain.accountId}}",
    "pqlData": "{{chain.pql_data}}",
    "expansionPlan": "{{previous.playbook}}",
    "assignmentRules": "territory_based",
    "notifyRep": true,
    "notifyCustomer": false
  },
  "exit_routing": {
    "assigned_to_sales": "cpq_quote_generator",
    "hold_for_timing": "schedule_outreach"
  }
}
```

#### Step 6: Generate Quote

```json
{
  "skill": "cpq_quote_generator",
  "input": {
    "accountId": "{{chain.accountId}}",
    "expansionPlan": "{{chain.expansion_plan}}",
    "discountRules": "apply_pql_discount",
    "pricingModel": "usage_based",
    "includeOnboarding": true
  },
  "exit_routing": {
    "quote_generated": "deal_inspection",
    "needs_approval": "manager_review"
  }
}
```

#### Step 7: Inspect Deal Health

```json
{
  "skill": "deal_inspection",
  "input": {
    "dealId": "{{previous.dealId}}",
    "depth": "comprehensive",
    "checkpoints": ["budget", "authority", "timeline", "competition"],
    "riskFactors": true
  },
  "output": "send_to_rep_with_insights"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/pql-handoff \
  -H "Content-Type: application/json" \
  -d '{
    "accountId": "test-account-789",
    "usageData": {
      "seats": 15,
      "featuresUsed": 12,
      "apiCalls": 500000,
      "teamCollaboration": "high",
      "powerUsers": 5
    },
    "currentPlan": "pro"
  }'
```

### Expected Output

```json
{
  "pqlQualified": true,
  "pqlScore": 89,
  "usageDepth": "high",
  "expansionOpportunity": {
    "type": "enterprise_upgrade",
    "estimatedARR": "$50,000",
    "confidence": "high"
  },
  "assignedTo": "rep_john_smith",
  "quoteGenerated": true,
  "dealHealth": "healthy",
  "recommendedActions": [
    "Schedule discovery call within 48 hours",
    "Present enterprise features demo",
    "Discuss API rate limits and custom integration needs"
  ],
  "timeline": "Close within 30 days"
}
```

### Monitoring & Metrics

Track these KPIs:

- **PQL-to-Opportunity Rate:** Target > 60% (baseline ~20%)
- **PQL-to-Close Rate:** Target > 15% (baseline ~5%)
- **Sales Cycle Length:** Target 30-40 days (baseline 60-90 days)
- **Average Deal Size:** Target $50K+ for enterprise upgrades
- **Rep Satisfaction:** Track rep feedback on PQL quality

### Expected Outcomes

- **Week 1:** PQL detection running, 10-20 accounts identified
- **Month 1:** 3x improvement in PQL-to-opportunity conversion
- **Quarter 1:** $1M-$3M incremental pipeline from product-led motion
- **Quarter 2:** 40% reduction in sales cycle for product-led deals

---

## Recipe 14: AI Support Deflection System

**Use Case:** Automate support ticket triage, classification, and resolution with AI-powered response generation and knowledge gap detection
**Skills:** 6 chained skills
**Time:** < 1 minute automated resolution vs 4-8 hour manual response time
**ROI:** 70% ticket deflection, 50% support cost reduction, $150K-$300K annual savings

### The Chain

```
ai_ticket_classifier → ai_intent_classifier → ai_response_suggester →
support_resolution_suggester → support_kb_gap_finder → support_deflector
```

### How It Works

1. **ai_ticket_classifier** — Automatically classifies tickets by type, priority, and routing
2. **ai_intent_classifier** — Identifies customer intent and underlying issue
3. **ai_response_suggester** — Generates contextual AI-powered response drafts
4. **support_resolution_suggester** — Recommends resolution steps based on historical patterns
5. **support_kb_gap_finder** — Identifies missing knowledge base articles
6. **support_deflector** — Deflects tickets to self-serve resources when appropriate

### Setup Instructions

#### Step 1: Install AI Ops & Support Ops Skills

```bash
npx skills-directory install --target all --domain ai_ops support_ops
```

#### Step 2: Configure AI Ticket Classification

```json
{
  "skill": "ai_ticket_classifier",
  "trigger": "ticket_created",
  "input": {
    "ticketId": "{{trigger.ticketId}}",
    "ticketContent": "{{trigger.body}}",
    "customerContext": "{{customer.history}}",
    "classificationTypes": ["bug", "feature_request", "how_to", "billing", "technical"],
    "priorityLevels": ["urgent", "high", "normal", "low"]
  },
  "exit_routing": {
    "classified": "ai_intent_classifier",
    "needs_human": "escalate_immediately"
  }
}
```

#### Step 3: Classify Customer Intent

```json
{
  "skill": "ai_intent_classifier",
  "input": {
    "ticketId": "{{chain.ticketId}}",
    "ticketType": "{{previous.classification}}",
    "customerMessage": "{{trigger.body}}",
    "contextualData": "{{customer.account_data}}",
    "intentCategories": ["resolve_issue", "get_information", "request_feature", "report_bug", "cancel_service"]
  },
  "exit_routing": {
    "intent_clear": "ai_response_suggester",
    "intent_ambiguous": "clarification_needed"
  }
}
```

#### Step 4: Generate AI Response

```json
{
  "skill": "ai_response_suggester",
  "input": {
    "ticketId": "{{chain.ticketId}}",
    "intent": "{{previous.intent}}",
    "classification": "{{chain.classification}}",
    "knowledgeBase": "search",
    "tone": "professional_friendly",
    "includeLinks": true
  },
  "exit_routing": {
    "response_generated": "support_resolution_suggester",
    "kb_gaps_found": "support_kb_gap_finder"
  }
}
```

#### Step 5: Suggest Resolution Steps

```json
{
  "skill": "support_resolution_suggester",
  "input": {
    "ticketId": "{{chain.ticketId}}",
    "intent": "{{chain.intent}}",
    "aiResponse": "{{previous.response}}",
    "historicalResolutions": "search_similar",
    "resolutionType": ["self_serve", "agent_assisted", "escalated"]
  },
  "exit_routing": {
    "self_serve_possible": "support_deflector",
    "needs_agent": "assign_to_agent",
    "needs_escalation": "escalate_to_tier2"
  }
}
```

#### Step 6: Find Knowledge Base Gaps

```json
{
  "skill": "support_kb_gap_finder",
  "input": {
    "ticketId": "{{chain.ticketId}}",
    "ticketType": "{{chain.classification}}",
    "searchAttempts": "{{chain.kb_searches}}",
    "commonQueries": "analyze",
    "gapThreshold": 3
  },
  "exit_routing": {
    "gap_found": "create_kb_article_task",
    "no_gap": "support_deflector"
  }
}
```

#### Step 7: Deflect to Self-Serve

```json
{
  "skill": "support_deflector",
  "input": {
    "ticketId": "{{chain.ticketId}}",
    "aiResponse": "{{chain.ai_response}}",
    "resolutionSteps": "{{previous.steps}}",
    "kbArticles": "{{chain.relevant_articles}}",
    "deflectionConfidence": "{{previous.confidence}}"
  },
  "output": "send_to_customer_or_agent"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/support-deflection \
  -H "Content-Type: application/json" \
  -d '{
    "ticketId": "test-ticket-001",
    "customerMessage": "How do I reset my API key?",
    "customerId": "cust_123",
    "accountType": "pro"
  }'
```

### Expected Output

```json
{
  "ticketClassified": true,
  "classification": "how_to",
  "priority": "normal",
  "intent": "get_information",
  "aiResponseGenerated": true,
  "deflectionPossible": true,
  "kbArticles": [
    "How to Reset Your API Key",
    "API Security Best Practices"
  ],
  "resolutionSteps": [
    "Navigate to Settings > API Keys",
    "Click 'Regenerate Key'",
    "Update key in your application"
  ],
  "deflected": true,
  "estimatedResolutionTime": "< 1 minute",
  "supportCostSaved": "$25"
}
```

### Monitoring & Metrics

Track these KPIs:

- **Deflection Rate:** Target > 70% of eligible tickets
- **First Response Time:** Target < 1 minute for AI responses
- **Customer Satisfaction:** Target > 4.5/5 for deflected tickets
- **Support Cost Savings:** Target $150K-$300K annually
- **Knowledge Base Coverage:** Track gap identification and article creation

### Expected Outcomes

- **Week 1:** AI classification active on 100% of tickets
- **Month 1:** 70% deflection rate for how-to and informational tickets
- **Quarter 1:** $50K-$100K support cost savings
- **Quarter 2:** 90% coverage in knowledge base, minimal gaps

---

## Recipe 15: Developer Experience Onboarding

**Use Case:** Accelerate developer onboarding with automated API documentation, code samples, sandbox provisioning, and integration health monitoring
**Skills:** 6 chained skills
**Time:** 2-4 hours to first API call vs 4-8 weeks manual process
**ROI:** 60% faster integration time, 40% higher completion rate, 2x API adoption

### The Chain

```
api_onboarding → code_sample_generator → sandbox_manager →
integration_health → error_explainer → changelog_tracker
```

### How It Works

1. **api_onboarding** — Guides developers through API setup, authentication, and first call
2. **code_sample_generator** — Generates working code examples in multiple languages
3. **sandbox_manager** — Provisions isolated sandbox environments for testing
4. **integration_health** — Monitors integration health and identifies issues early
5. **error_explainer** — Provides detailed explanations for API errors
6. **changelog_tracker** — Keeps developers informed of API changes and deprecations

### Setup Instructions

#### Step 1: Install DevEx Skills

```bash
npx skills-directory install --target all --domain devex
```

#### Step 2: Configure API Onboarding

```json
{
  "skill": "api_onboarding",
  "trigger": "developer_signup",
  "input": {
    "developerId": "{{trigger.developerId}}",
    "apiProduct": "{{trigger.api_product}}",
    "experienceLevel": "{{developer.experience}}",
    "preferredLanguage": "{{developer.language}}",
    "onboardingGoal": "first_successful_call"
  },
  "exit_routing": {
    "setup_complete": "code_sample_generator",
    "needs_help": "support_escalation"
  }
}
```

#### Step 3: Generate Code Samples

```json
{
  "skill": "code_sample_generator",
  "input": {
    "developerId": "{{chain.developerId}}",
    "apiEndpoints": "{{previous.endpoints_selected}}",
    "languages": ["python", "javascript", "ruby", "go", "java"],
    "includeAuth": true,
    "includeErrorHandling": true,
    "complexity": "beginner_friendly"
  },
  "exit_routing": {
    "samples_generated": "sandbox_manager",
    "needs_customization": "custom_sample_request"
  }
}
```

#### Step 4: Provision Sandbox Environment

```json
{
  "skill": "sandbox_manager",
  "input": {
    "developerId": "{{chain.developerId}}",
    "sandboxType": "isolated",
    "dataSeeding": "sample_data",
    "rateLimits": "development_tier",
    "duration": "90_days",
    "features": "all_api_features"
  },
  "exit_routing": {
    "sandbox_ready": "integration_health",
    "provisioning_failed": "retry_or_alert"
  }
}
```

#### Step 5: Monitor Integration Health

```json
{
  "skill": "integration_health",
  "input": {
    "developerId": "{{chain.developerId}}",
    "sandboxId": "{{previous.sandboxId}}",
    "healthChecks": ["api_calls_success_rate", "auth_errors", "rate_limit_hits", "response_times"],
    "monitoringWindow": "continuous",
    "alertThresholds": {
      "error_rate": 10,
      "no_activity": "7_days"
    }
  },
  "exit_routing": {
    "healthy": "changelog_tracker",
    "issues_detected": "error_explainer",
    "inactive": "re_engagement_campaign"
  }
}
```

#### Step 6: Explain API Errors

```json
{
  "skill": "error_explainer",
  "input": {
    "developerId": "{{chain.developerId}}",
    "errorCode": "{{trigger.error_code}}",
    "errorContext": "{{trigger.request_context}}",
    "explanationDepth": "detailed",
    "includeSolutions": true,
    "relatedDocs": true
  },
  "exit_routing": {
    "explained": "integration_health",
    "needs_support": "developer_support"
  }
}
```

#### Step 7: Track API Changes

```json
{
  "skill": "changelog_tracker",
  "input": {
    "developerId": "{{chain.developerId}}",
    "integratedEndpoints": "{{chain.endpoints_used}}",
    "notificationPreference": "{{developer.notification_preference}}",
    "changeTypes": ["breaking", "deprecation", "new_feature", "bug_fix"],
    "relevanceFilter": "high"
  },
  "output": "notify_developer_of_changes"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/devex-onboarding \
  -H "Content-Type: application/json" \
  -d '{
    "developerId": "dev_456",
    "apiProduct": "core_api",
    "language": "python",
    "experienceLevel": "intermediate",
    "goal": "integrate_user_auth"
  }'
```

### Expected Output

```json
{
  "onboardingComplete": true,
  "timeToFirstCall": "2 hours",
  "codeSamplesGenerated": 5,
  "languages": ["python", "javascript", "curl"],
  "sandboxProvisioned": true,
  "sandboxUrl": "https://sandbox.api.example.com",
  "integrationHealth": "healthy",
  "apiCallsSuccessRate": 98,
  "changelogSubscribed": true,
  "nextSteps": [
    "Test authentication flow",
    "Integrate user profile endpoint",
    "Review rate limits for production"
  ]
}
```

### Monitoring & Metrics

Track these KPIs:

- **Time to First API Call:** Target < 4 hours (baseline 1-2 weeks)
- **Integration Completion Rate:** Target > 70% (baseline ~30%)
- **Sandbox Utilization:** Track active developer engagement
- **Error Rate Reduction:** Target 50% reduction via error explainer
- **API Adoption Rate:** Target 2x increase in active integrations

### Expected Outcomes

- **Week 1:** 50+ developers onboarded through automated flow
- **Month 1:** 60% reduction in time to first successful API call
- **Quarter 1:** 40% increase in integration completion rate
- **Quarter 2:** 2x growth in active API integrations

---

## Recipe 16: Employee Onboarding Automation

**Use Case:** Automate employee onboarding with compensation benchmarking, skill gap analysis, performance tracking, and DEI monitoring
**Skills:** 6 chained skills
**Time:** 2-4 hours automated onboarding vs 2-3 weeks manual process
**ROI:** 70% faster onboarding, 40% cost reduction, 25% better retention

### The Chain

```
people_onboarding_checklist → people_comp_benchmarker → people_skill_gap_analyzer →
people_perf_review_generator → people_pulse_analyzer → people_dei_tracker
```

### How It Works

1. **people_onboarding_checklist** — Automates onboarding tasks, documentation, and system access
2. **people_comp_benchmarker** — Benchmarks compensation against market rates
3. **people_skill_gap_analyzer** — Identifies skill gaps and training needs
4. **people_perf_review_generator** — Generates structured performance reviews
5. **people_pulse_analyzer** — Tracks employee sentiment and engagement
6. **people_dei_tracker** — Monitors diversity, equity, and inclusion metrics

### Setup Instructions

#### Step 1: Install People Ops Skills

```bash
npx skills-directory install --target all --domain people_ops
```

#### Step 2: Configure Onboarding Checklist

```json
{
  "skill": "people_onboarding_checklist",
  "trigger": "employee_hired",
  "input": {
    "employeeId": "{{trigger.employeeId}}",
    "role": "{{employee.role}}",
    "department": "{{employee.department}}",
    "startDate": "{{employee.start_date}}",
    "checklistItems": [
      "equipment_setup",
      "system_access",
      "benefits_enrollment",
      "team_introductions",
      "training_modules"
    ]
  },
  "exit_routing": {
    "checklist_complete": "people_comp_benchmarker",
    "items_pending": "reminder_sequence"
  }
}
```

#### Step 3: Benchmark Compensation

```json
{
  "skill": "people_comp_benchmarker",
  "input": {
    "employeeId": "{{chain.employeeId}}",
    "role": "{{employee.role}}",
    "location": "{{employee.location}}",
    "experienceLevel": "{{employee.years_experience}}",
    "benchmarkSources": ["market_data", "industry_surveys", "peer_companies"],
    "includeEquity": true
  },
  "exit_routing": {
    "benchmark_complete": "people_skill_gap_analyzer",
    "compensation_alert": "hr_review"
  }
}
```

#### Step 4: Analyze Skill Gaps

```json
{
  "skill": "people_skill_gap_analyzer",
  "input": {
    "employeeId": "{{chain.employeeId}}",
    "currentSkills": "{{employee.resume_skills}}",
    "roleRequirements": "{{role.required_skills}}",
    "teamSkills": "{{team.skill_matrix}}",
    "analysisDepth": "comprehensive",
    "recommendTraining": true
  },
  "exit_routing": {
    "gaps_identified": "people_perf_review_generator",
    "no_gaps": "people_pulse_analyzer"
  }
}
```

#### Step 5: Generate Performance Framework

```json
{
  "skill": "people_perf_review_generator",
  "input": {
    "employeeId": "{{chain.employeeId}}",
    "skillGaps": "{{previous.gaps}}",
    "performanceFramework": "OKRs",
    "reviewCycle": "quarterly",
    "goals": "auto_generate_from_role",
    "includeDevelopmentPlan": true
  },
  "exit_routing": {
    "framework_set": "people_pulse_analyzer",
    "needs_manager_input": "manager_review"
  }
}
```

#### Step 6: Track Employee Pulse

```json
{
  "skill": "people_pulse_analyzer",
  "trigger": "scheduled",
  "frequency": "weekly",
  "input": {
    "employeeId": "{{chain.employeeId}}",
    "pulseQuestions": ["engagement", "satisfaction", "workload", "team_dynamics"],
    "anonymity": "partial",
    "trendAnalysis": true,
    "benchmarkAgainst": "team_avg"
  },
  "exit_routing": {
    "pulse_healthy": "people_dei_tracker",
    "concerns_detected": "manager_alert",
    "burnout_risk": "hr_intervention"
  }
}
```

#### Step 7: Monitor DEI Metrics

```json
{
  "skill": "people_dei_tracker",
  "input": {
    "employeeId": "{{chain.employeeId}}",
    "metrics": [
      "representation_by_level",
      "pay_equity",
      "promotion_rates",
      "retention_by_demographic"
    ],
    "aggregationLevel": "team",
    "privacyPreserving": true,
    "reportingFrequency": "quarterly"
  },
  "output": "aggregate_dei_dashboard"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/employee-onboarding \
  -H "Content-Type: application/json" \
  -d '{
    "employeeId": "emp_789",
    "role": "Senior Software Engineer",
    "department": "Engineering",
    "location": "San Francisco",
    "startDate": "2026-03-01"
  }'
```

### Expected Output

```json
{
  "onboardingComplete": true,
  "checklistCompletionRate": 100,
  "compensationBenchmark": {
    "market_percentile": 65,
    "status": "competitive",
    "recommendation": "within_range"
  },
  "skillGapsIdentified": 2,
  "trainingRecommended": ["Advanced Kubernetes", "System Design"],
  "performanceFrameworkSet": true,
  "okrsGenerated": 3,
  "pulseScore": 8.5,
  "deiMetricsRecorded": true,
  "estimatedOnboardingTime": "3 hours"
}
```

### Monitoring & Metrics

Track these KPIs:

- **Onboarding Completion Time:** Target < 1 week (baseline 2-3 weeks)
- **Employee Satisfaction (90-day):** Target > 8/10
- **Retention Rate (1-year):** Target 25% improvement
- **Time to Productivity:** Target 50% reduction
- **DEI Representation:** Track progress toward company goals

### Expected Outcomes

- **Week 1:** 10 employees onboarded through automated system
- **Month 1:** 70% reduction in onboarding administrative time
- **Quarter 1:** 25% improvement in 90-day employee satisfaction scores
- **Quarter 2:** 40% cost reduction in onboarding process

---

## Recipe 17: Data Quality Automation

**Use Case:** Automate data quality monitoring, validation, and anomaly detection across data pipelines
**Skills:** 6 chained skills
**Time:** Real-time data quality monitoring vs weekly manual audits
**ROI:** 80% reduction in data errors, 90% faster issue detection, $100K+ savings/year

### The Chain

```
data_anomaly_alerter → data_event_validator → data_cohort_builder →
data_funnel_optimizer → data_experiment_analyzer → data_dashboard_builder
```

### How It Works

1. **data_anomaly_alerter** — Detects anomalies in data pipelines and metrics
2. **data_event_validator** — Validates event schema, data types, and business rules
3. **data_cohort_builder** — Builds user cohorts for analysis and experimentation
4. **data_funnel_optimizer** — Analyzes and optimizes conversion funnels
5. **data_experiment_analyzer** — Analyzes A/B test results and statistical significance
6. **data_dashboard_builder** — Builds automated dashboards for data monitoring

### Setup Instructions

#### Step 1: Install Data Ops Skills

```bash
npx skills-directory install --target all --domain data_ops
```

#### Step 2: Configure Anomaly Detection

```json
{
  "skill": "data_anomaly_alerter",
  "trigger": "data_event",
  "frequency": "continuous",
  "input": {
    "dataSource": "{{trigger.source}}",
    "metrics": ["volume", "freshness", "completeness", "accuracy"],
    "anomalyThreshold": "3_standard_deviations",
    "lookbackWindow": "7_days",
    "alertChannels": ["slack", "email", "pagerduty"]
  },
  "exit_routing": {
    "anomaly_detected": "data_event_validator",
    "normal": "continue_monitoring"
  }
}
```

#### Step 3: Validate Event Data

```json
{
  "skill": "data_event_validator",
  "input": {
    "eventType": "{{trigger.event_type}}",
    "eventData": "{{trigger.data}}",
    "schemaValidation": true,
    "businessRules": [
      "revenue_must_be_positive",
      "timestamps_must_be_sequential",
      "user_id_must_exist"
    ],
    "strictMode": false
  },
  "exit_routing": {
    "valid": "data_cohort_builder",
    "invalid": "quarantine_and_alert",
    "needs_enrichment": "data_enrichment_pipeline"
  }
}
```

#### Step 4: Build User Cohorts

```json
{
  "skill": "data_cohort_builder",
  "input": {
    "userId": "{{previous.user_id}}",
    "cohortDefinitions": [
      {"name": "weekly_active", "criteria": "weekly_sessions >= 3"},
      {"name": "power_users", "criteria": "monthly_actions >= 100"},
      {"name": "at_risk", "criteria": "days_since_last_activity > 14"}
    ],
    "updateFrequency": "daily",
    "historicalWindow": "90_days"
  },
  "exit_routing": {
    "cohorts_built": "data_funnel_optimizer",
    "cohort_empty": "adjust_criteria"
  }
}
```

#### Step 5: Optimize Conversion Funnels

```json
{
  "skill": "data_funnel_optimizer",
  "input": {
    "funnelId": "{{trigger.funnel_id}}",
    "funnelSteps": ["signup", "activation", "first_purchase", "retention"],
    "cohort": "{{previous.cohort}}",
    "optimizationGoal": "maximize_conversion",
    "analysisWindow": "30_days",
    "identifyDropoffs": true
  },
  "exit_routing": {
    "optimization_complete": "data_experiment_analyzer",
    "needs_experiment": "create_ab_test"
  }
}
```

#### Step 6: Analyze Experiments

```json
{
  "skill": "data_experiment_analyzer",
  "input": {
    "experimentId": "{{trigger.experiment_id}}",
    "variants": ["control", "variant_a", "variant_b"],
    "primaryMetric": "conversion_rate",
    "secondaryMetrics": ["time_to_convert", "ltv", "retention"],
    "statisticalMethod": "bayesian",
    "confidenceLevel": 0.95
  },
  "exit_routing": {
    "winner_found": "data_dashboard_builder",
    "inconclusive": "extend_experiment",
    "significant_result": "rollout_winner"
  }
}
```

#### Step 7: Build Monitoring Dashboard

```json
{
  "skill": "data_dashboard_builder",
  "input": {
    "dashboardType": "data_quality",
    "metrics": "{{chain.all_metrics}}",
    "visualizations": ["time_series", "funnel", "cohort_retention", "experiment_results"],
    "refreshRate": "real_time",
    "recipients": ["data_team", "product_team", "executive_team"]
  },
  "output": "publish_dashboard"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/data-quality \
  -H "Content-Type: application/json" \
  -d '{
    "dataSource": "production_events",
    "eventType": "user_action",
    "timeWindow": "last_24_hours",
    "qualityChecks": ["schema", "volume", "freshness"]
  }'
```

### Expected Output

```json
{
  "dataQualityScore": 98,
  "anomaliesDetected": 0,
  "eventsValidated": 1500000,
  "invalidEvents": 30000,
  "quarantinedEvents": 50,
  "cohortsBuilt": 12,
  "funnelConversionRate": 23.5,
  "experimentsAnalyzed": 3,
  "dashboardUrl": "https://dashboard.example.com/data-quality",
  "recommendations": [
    "Investigate spike in invalid timestamps",
    "Extend experiment #47 for 3 more days",
    "Optimize funnel step 2 (30% dropoff)"
  ]
}
```

### Monitoring & Metrics

Track these KPIs:

- **Data Quality Score:** Target > 95%
- **Anomaly Detection Time:** Target < 5 minutes
- **Invalid Event Rate:** Target < 2%
- **Data Pipeline Uptime:** Target > 99.9%
- **Time to Resolution:** Target < 1 hour for critical issues

### Expected Outcomes

- **Week 1:** Data quality monitoring active across all pipelines
- **Month 1:** 80% reduction in data errors reaching production
- **Quarter 1:** 90% faster anomaly detection and resolution
- **Quarter 2:** $100K+ savings from prevented data quality issues

---

## Recipe 18: Community-Led Growth Engine

**Use Case:** Drive organic growth through community engagement, user-generated content, ambassador programs, and event management
**Skills:** 6 chained skills
**Time:** Automated community management vs 40+ hours/week manual effort
**ROI:** 40% organic growth increase, 50% CAC reduction, 3x word-of-mouth referrals

### The Chain

```
community_champion_identifier → community_ambassador_program → community_forum_moderator →
community_ugc_curator → community_event_manager → community_case_study_finder
```

### How It Works

1. **community_champion_identifier** — Identifies power users and community champions based on engagement
2. **community_ambassador_program** — Recruits and manages community ambassadors
3. **community_forum_moderator** — Assists with forum moderation and content review
4. **community_ugc_curator** — Curates and surfaces best user-generated content
5. **community_event_manager** — Plans, promotes, and manages community events
6. **community_case_study_finder** — Identifies and qualifies members for case studies

### Setup Instructions

#### Step 1: Install Community Skills

```bash
npx skills-directory install --target all --domain community
```

#### Step 2: Configure Champion Identification

```json
{
  "skill": "community_champion_identifier",
  "trigger": "scheduled",
  "frequency": "weekly",
  "input": {
    "communityMembers": "{{all_members}}",
    "engagementSignals": [
      "posts_created",
      "helpful_responses",
      "upvotes_received",
      "event_attendance",
      "referrals_made"
    ],
    "championThreshold": 80,
    "lookbackWindow": "90_days"
  },
  "exit_routing": {
    "champions_found": "community_ambassador_program",
    "no_new_champions": "engagement_campaign"
  }
}
```

#### Step 3: Manage Ambassador Program

```json
{
  "skill": "community_ambassador_program",
  "input": {
    "championIds": "{{previous.champion_list}}",
    "programTier": ["bronze", "silver", "gold", "platinum"],
    "benefits": [
      "early_feature_access",
      "exclusive_events",
      "swag",
      "revenue_share"
    ],
    "requirements": {
      "bronze": "10_quality_posts_per_month",
      "silver": "25_posts_plus_1_event",
      "gold": "50_posts_plus_3_events",
      "platinum": "100_posts_plus_5_events"
    },
    "autoPromote": true
  },
  "exit_routing": {
    "ambassadors_active": "community_forum_moderator",
    "needs_recruiting": "ambassador_recruitment_campaign"
  }
}
```

#### Step 4: Assist Forum Moderation

```json
{
  "skill": "community_forum_moderator",
  "trigger": "post_created",
  "input": {
    "postId": "{{trigger.postId}}",
    "postContent": "{{trigger.content}}",
    "authorId": "{{trigger.authorId}}",
    "moderationRules": [
      "no_spam",
      "no_self_promotion",
      "respectful_tone",
      "on_topic"
    ],
    "autoModerate": "flag_for_review",
    "ambassadorOverride": true
  },
  "exit_routing": {
    "approved": "community_ugc_curator",
    "flagged": "human_review",
    "spam": "auto_remove"
  }
}
```

#### Step 5: Curate User-Generated Content

```json
{
  "skill": "community_ugc_curator",
  "input": {
    "contentSource": "{{previous.approved_posts}}",
    "curationCriteria": ["helpfulness", "uniqueness", "engagement", "educational_value"],
    "contentTypes": ["tutorials", "use_cases", "tips", "success_stories"],
    "featuredThreshold": 90,
    "distributionChannels": ["newsletter", "social_media", "blog"]
  },
  "exit_routing": {
    "content_curated": "community_event_manager",
    "feature_worthy": "create_blog_post"
  }
}
```

#### Step 6: Manage Community Events

```json
{
  "skill": "community_event_manager",
  "input": {
    "eventType": "{{trigger.event_type}}",
    "eventFormat": ["webinar", "meetup", "workshop", "conference"],
    "ambassadorInvolvement": "required",
    "promotionChannels": ["email", "forum", "social"],
    "targetAttendance": "auto_calculate",
    "followUpSequence": "automated"
  },
  "exit_routing": {
    "event_scheduled": "community_case_study_finder",
    "low_registration": "promotion_boost"
  }
}
```

#### Step 7: Find Case Study Candidates

```json
{
  "skill": "community_case_study_finder",
  "input": {
    "memberIds": "{{chain.community_members}}",
    "qualificationCriteria": [
      "product_success_story",
      "measurable_results",
      "willing_to_share",
      "diverse_use_case"
    ],
    "outreachTemplate": "case_study_invitation",
    "incentive": "featured_placement",
    "targetCaseStudies": 10
  },
  "output": "case_study_pipeline"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/community-growth \
  -H "Content-Type: application/json" \
  -d '{
    "communitySize": 5000,
    "activeMembers": 1200,
    "timeWindow": "last_30_days",
    "eventType": "monthly_meetup"
  }'
```

### Expected Output

```json
{
  "championsIdentified": 25,
  "ambassadorsActive": 15,
  "ambassadorTiers": {
    "bronze": 8,
    "silver": 4,
    "gold": 2,
    "platinum": 1
  },
  "postsModerated": 450,
  "spamRemoved": 12,
  "ugcCurated": 35,
  "featuredContent": 8,
  "eventsScheduled": 3,
  "eventRegistrations": 180,
  "caseStudyCandidates": 12,
  "organicGrowthRate": "15% month-over-month",
  "referralConversions": 45
}
```

### Monitoring & Metrics

Track these KPIs:

- **Community Growth Rate:** Target 40% organic growth annually
- **Ambassador Engagement:** Target > 80% monthly activity rate
- **UGC Volume:** Target 50+ quality posts per month
- **Event Attendance:** Target 70%+ registration-to-attendance rate
- **Case Study Conversion:** Target 5+ case studies per quarter

### Expected Outcomes

- **Week 1:** Champion identification running, 10-20 champions found
- **Month 1:** 15 active ambassadors driving community engagement
- **Quarter 1:** 40% increase in organic community growth
- **Quarter 2:** 50% CAC reduction through community-led acquisition

---

## Recipe 19-28: Additional Domain-Specific Recipes

Due to space constraints, Recipes 19-28 follow similar patterns for:
- Multi-Platform Content Distribution (Marketing)
- Product Experimentation Engine (Product Ops)
- API Lifecycle Management (DevEx)
- Competitive Intelligence Automation (RevOps)
- Brand Consistency Engine (Marketing)
- Customer Education Platform (Customer Success)
- Security Code Review Automation (Security)
- Compliance Automation Hub (Compliance)
- E-commerce Revenue Optimization (Monetization)
- Partnership Ecosystem Automation (Ecosystem)

**For complete documentation of Recipes 19-28, see the full cookbook repository or contact support.**

---

## Phase 3: Industry-Specific Integration Patterns (29-30)

These quick-reference recipes show how to adapt existing skills for industry-specific use cases.

---

### Recipe 29: Healthcare/Life Sciences Workflows
```
[Scientific domain skills] → compliance_pii_detector → compliance_data_retention
```
**ROI:** 40% faster research workflows, 60% compliance improvement
**Note:** Uses 141 scientific domain skills for healthcare/clinical research workflows. Requires medical knowledge bases for full implementation.

---

### Recipe 30: FinTech/Banking Compliance
```
arr_waterfall → burn_rate_monitor → compliance_gdpr_manager → compliance_audit_preparer
```
**ROI:** 90% faster financial reporting, 80% compliance accuracy
**Note:** Combines finops and compliance skills for banking/fintech regulatory requirements.

---

## Tips for Building Your Own Chains

### 1. Start Simple
Begin with 2-3 skills. Prove value. Then expand.

### 2. Map Exit States
Every skill should have clear exit states that route to next skill or endpoint.

### 3. Include Human-in-the-Loop
For high-stakes decisions, add approval gates.

### 4. Monitor Continuously
Track metrics at each step to identify bottlenecks.

### 5. Iterate Based on Data
Use analytics to refine chains over time.

### 6. Document Your Patterns
Share successful chains with your team.

---

## Troubleshooting Common Issues

### Chain Breaks at Step 3

**Problem:** Skill fails or returns unexpected output
**Solution:**
- Check exit state mapping
- Validate input data format
- Add error handling/retry logic

### Performance Slow

**Problem:** Chain takes too long to execute
**Solution:**
- Run independent skills in parallel
- Cache frequently-used data
- Optimize skill configurations

### Results Not Actionable

**Problem:** Chain outputs are too generic
**Solution:**
- Provide more context in inputs
- Use customer/account-specific data
- Add human review step

---

## Next Steps

1. **Pick a recipe** that matches your use case
2. **Install the skills** for that domain
3. **Test with sample data** before going live
4. **Monitor metrics** to track ROI
5. **Iterate and expand** based on results

**Need help?** Check [Quick Wins](./QUICK_WINS.md) for simpler starting points.
