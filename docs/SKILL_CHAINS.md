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
