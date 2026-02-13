# Skill Chain Cookbook

**Pick a recipe, copy the chain, deploy.** Each recipe below is a tested workflow built from the library of **764 skills** (the ingredients). New to skills? [What are skills?](WHAT_ARE_SKILLS.md)

## 36 Ready-to-Use Recipes

Each recipe in this cookbook is a proven skill chain you can deploy immediately. Every recipe includes:

- **Use case** — What problem it solves
- **Skills** — Which skills to chain together
- **ROI** — Expected time/cost savings
- **Step-by-step instructions** — Copy-paste examples
- **Expected outcomes** — What success looks like

---

## 📋 Quick Navigation

### 💼 Sales & Revenue

- [Recipe 1: Sales Deal Qualification Pipeline](#recipe-1-sales-deal-qualification-pipeline)
- [Recipe 2: Financial Intelligence Dashboard](#recipe-2-financial-intelligence-dashboard)
- [Recipe 3: Product-Led Sales Handoff](#recipe-3-product-led-sales-handoff)
- [Recipe 4: Competitive Intelligence Automation](#recipe-4-competitive-intelligence-automation)

### 🤝 Customer Success & Support

- [Recipe 5: Customer Churn Prevention Pipeline](#recipe-5-customer-churn-prevention-pipeline)
- [Recipe 6: AI Support Deflection System](#recipe-6-ai-support-deflection-system)
- [Recipe 7: Customer Education Platform](#recipe-7-customer-education-platform)
- [Recipe 8: AI Ops Conversation Pipeline](#recipe-8-ai-ops-conversation-pipeline)
- [Recipe 9: Customer Onboarding Automation](#recipe-9-customer-onboarding-automation)
- [Recipe 10: Support Ticket Triage & Resolution](#recipe-10-support-ticket-triage--resolution)

### 🚀 Growth & Marketing

- [Recipe 11: Growth Optimization Engine](#recipe-11-growth-optimization-engine)
- [Recipe 12: Content Marketing Automation](#recipe-12-content-marketing-automation)
- [Recipe 13: Freemium Conversion Optimization](#recipe-13-freemium-conversion-optimization)
- [Recipe 14: Usage-Based Pricing Engine](#recipe-14-usage-based-pricing-engine)
- [Recipe 15: Community-Led Growth Engine](#recipe-15-community-led-growth-engine)
- [Recipe 16: Multi-Platform Content Distribution](#recipe-16-multi-platform-content-distribution)
- [Recipe 17: Pricing & Packaging Optimization](#recipe-17-pricing--packaging-optimization)
- [Recipe 18: Product Analytics Intelligence](#recipe-18-product-analytics-intelligence)

### 🔧 Product & Engineering

- [Recipe 19: Developer Experience Onboarding](#recipe-19-developer-experience-onboarding)
- [Recipe 20: Product Experimentation Engine](#recipe-20-product-experimentation-engine)
- [Recipe 21: API Lifecycle Management](#recipe-21-api-lifecycle-management)
- [Recipe 22: Security Code Review Automation](#recipe-22-security-code-review-automation)
- [Recipe 23: Superpowers Development Workflow](#recipe-23-superpowers-development-workflow)

### 🎨 Brand & Content

- [Recipe 24: Brand Consistency Engine](#recipe-24-brand-consistency-engine)

### ⚙️ Operations & Compliance

- [Recipe 25: Employee Onboarding Automation](#recipe-25-employee-onboarding-automation)
- [Recipe 26: Data Quality Automation](#recipe-26-data-quality-automation)
- [Recipe 27: Compliance Automation Hub](#recipe-27-compliance-automation-hub)
- [Recipe 28: E-commerce Revenue Optimization](#recipe-28-e-commerce-revenue-optimization)
- [Recipe 29: Partnership Ecosystem Automation](#recipe-29-partnership-ecosystem-automation)
- [Recipe 30: People Ops Talent Intelligence](#recipe-30-people-ops-talent-intelligence)
- [Recipe 31: Data Ops Experimentation Pipeline](#recipe-31-data-ops-experimentation-pipeline)
- [Recipe 32: Partnership Deal Flow](#recipe-32-partnership-deal-flow)

### 🔬 Research & Strategy

- [Recipe 33: Scientific Research Synthesis Pipeline](#recipe-33-scientific-research-synthesis-pipeline)
- [Recipe 34: Skene Growth Strategy Chain](#recipe-34-skene-growth-strategy-chain)

### 🌐 Community

- [Recipe 35: Community Advocacy Pipeline](#recipe-35-community-advocacy-pipeline)

### 💰 FinOps

- [Recipe 36: FinOps Standalone Dashboard](#recipe-36-finops-standalone-dashboard)

---

## Recipe index by domain

| Domain                         | Recipe numbers                 |
| ------------------------------ | ------------------------------ |
| **Sales & RevOps**             | 1, 2, 3, 4                     |
| **Customer Success & Support** | 5, 6, 7, 8, 9, 10              |
| **Growth & Marketing**         | 11, 12, 13, 14, 15, 16, 17, 18 |
| **Product & Engineering**      | 19, 20, 21, 22, 23             |
| **Brand & Content**            | 24                             |
| **Operations & Compliance**    | 25, 26, 27, 28, 29, 30, 31, 32 |
| **Research & Strategy**        | 33, 34                         |
| **Community**                  | 35                             |
| **FinOps**                     | 36                             |

---

## Niche playbooks and exact data to wire

Every recipe is backed by a **workflow blueprint** with an **ICP** (Ideal Customer Profile), **integration reference** (exact fields/events to wire), and **opinionated prompts** per step so chains are niche-specific, not generic.

- **Recipe-to-blueprint mapping:** [registry/recipe_blueprint_index.json](../registry/recipe_blueprint_index.json) maps recipe number to blueprint id and optional integration refs.
- **Exact data to wire:** Reference schemas in [registry/integration_schemas/](../registry/integration_schemas/) list required Salesforce objects/fields, HubSpot events, and Stripe data for chains that use CRM or billing. Use with Clay, n8n, or custom ETL to ship faster.
- **Full playbook list:** See [docs/PLAYBOOKS.md](PLAYBOOKS.md) for all blueprints, their ICP(s), integration references, and where opinionated prompts live (in the blueprint YAML).

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
  "nextActions": ["Schedule discovery call", "Send ROI calculator", "Introduce solutions engineer"],
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

## Recipe 2: Financial Intelligence Dashboard

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
        "assumptions": { "headcount_increase": 30, "arr_growth": 100 }
      },
      {
        "name": "profitable_growth",
        "assumptions": { "headcount_increase": 15, "arr_growth": 50 }
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

## Recipe 3: Product-Led Sales Handoff

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

## Recipe 4: Competitive Intelligence Automation

**Use Case:** Automate competitive research, feature tracking, pricing analysis, and battlecard generation
**Skills:** 6 chained skills
**Time:** Real-time competitive intelligence vs 20-40 hours/month manual research
**ROI:** 90% faster competitive analysis, 60% better win rates, $200K+ pipeline impact

### The Chain

```
competitive_intel → competitive_feature_tracker → ai_knowledge_synthesizer →
content_research_writer → battlecard_generator → win_loss_analyzer
```

### How It Works

1. **competitive_intel** — Monitors competitors' websites, announcements, and market moves
2. **competitive_feature_tracker** — Tracks competitive feature releases and updates
3. **ai_knowledge_synthesizer** — Synthesizes competitive intelligence from multiple sources
4. **content_research_writer** — Researches and documents competitive positioning
5. **battlecard_generator** — Creates sales battlecards for competitive situations
6. **win_loss_analyzer** — Analyzes win/loss patterns against specific competitors

### Setup Instructions

#### Step 1: Install RevOps, Marketing & AI Ops Skills

```bash
npx skills-directory install --target all --domain revops marketing ai_ops
```

#### Step 2: Configure Competitive Monitoring

```json
{
  "skill": "competitive_intel",
  "trigger": "scheduled",
  "frequency": "daily",
  "input": {
    "competitors": ["competitor_a", "competitor_b", "competitor_c"],
    "monitoringSources": [
      "company_websites",
      "blog_posts",
      "press_releases",
      "product_hunt",
      "linkedin",
      "job_postings",
      "tech_news"
    ],
    "alertCriteria": ["product_launch", "pricing_change", "executive_hire", "funding_news"],
    "sentimentTracking": true
  },
  "exit_routing": {
    "updates_found": "competitive_feature_tracker",
    "no_changes": "continue_monitoring"
  }
}
```

#### Step 3: Track Feature Releases

```json
{
  "skill": "competitive_feature_tracker",
  "input": {
    "competitors": "{{previous.competitors}}",
    "competitiveUpdates": "{{previous.updates}}",
    "featureCategories": [
      "core_functionality",
      "integrations",
      "enterprise_features",
      "pricing_tiers",
      "security_compliance"
    ],
    "comparisonMatrix": "auto_update",
    "gapAnalysis": true
  },
  "exit_routing": {
    "features_tracked": "ai_knowledge_synthesizer",
    "critical_feature": "alert_product_team"
  }
}
```

#### Step 4: Synthesize Intelligence

```json
{
  "skill": "ai_knowledge_synthesizer",
  "input": {
    "competitiveData": "{{chain.all_data}}",
    "synthesisGoals": [
      "market_positioning",
      "feature_gaps",
      "pricing_strategy",
      "target_customers",
      "go_to_market_approach"
    ],
    "includeTrends": true,
    "confidenceScoring": true,
    "citeSources": true
  },
  "exit_routing": {
    "synthesis_complete": "content_research_writer",
    "needs_validation": "research_team_review"
  }
}
```

#### Step 5: Research Competitive Positioning

```json
{
  "skill": "content_research_writer",
  "input": {
    "topic": "competitive_landscape",
    "synthesizedIntel": "{{previous.synthesis}}",
    "outputFormat": "structured_analysis",
    "includeStrengthsWeaknesses": true,
    "targetAudience": "sales_team",
    "updateFrequency": "monthly"
  },
  "exit_routing": {
    "research_complete": "battlecard_generator",
    "needs_expert_input": "analyst_review"
  }
}
```

#### Step 6: Generate Sales Battlecards

```json
{
  "skill": "battlecard_generator",
  "input": {
    "competitor": "{{trigger.competitor}}",
    "competitiveIntel": "{{chain.all_intel}}",
    "battlecardSections": [
      "overview",
      "strengths_weaknesses",
      "key_differentiators",
      "common_objections",
      "proof_points",
      "customer_stories",
      "pricing_comparison",
      "talk_tracks"
    ],
    "format": "sales_enablement_tool",
    "updateTrigger": "competitive_change"
  },
  "exit_routing": {
    "battlecard_ready": "win_loss_analyzer",
    "needs_review": "sales_enablement_review"
  }
}
```

#### Step 7: Analyze Win/Loss Patterns

```json
{
  "skill": "win_loss_analyzer",
  "input": {
    "competitorId": "{{chain.competitor}}",
    "dealData": "{{crm.closed_deals}}",
    "analysisWindow": "90_days",
    "winLossFactors": [
      "price",
      "features",
      "implementation_time",
      "customer_support",
      "integrations",
      "brand"
    ],
    "includeQuotes": true,
    "recommendationEngine": true
  },
  "output": "win_loss_insights_report"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/competitive-intel \
  -H "Content-Type: application/json" \
  -d '{
    "competitor": "competitor_a",
    "monitoringPeriod": "last_7_days",
    "analysisType": "comprehensive"
  }'
```

### Expected Output

```json
{
  "competitiveUpdatesFound": 5,
  "criticalUpdates": 2,
  "featuresTracked": 12,
  "newFeatures": 3,
  "pricingChanges": 1,
  "synthesisGenerated": true,
  "battlecardsUpdated": 3,
  "winRate": {
    "vs_competitor_a": "65%",
    "vs_competitor_b": "72%",
    "vs_competitor_c": "58%"
  },
  "keyInsights": [
    "Competitor A launched enterprise SSO - our feature gap",
    "Competitor B raised prices 20% - opportunity for us",
    "Competitor C struggling with customer support (source: G2)"
  ],
  "recommendations": [
    "Prioritize SSO feature development",
    "Target Competitor B's price-sensitive customers",
    "Emphasize our support quality in competitive situations"
  ]
}
```

### Monitoring & Metrics

Track these KPIs:

- **Competitive Updates Detected:** Track volume and criticality
- **Win Rate by Competitor:** Target 60%+ vs each major competitor
- **Battlecard Utilization:** Track sales team usage
- **Time to Intelligence:** Target < 24 hours for critical updates
- **Competitive Losses:** Track and categorize reasons for losses

### Expected Outcomes

- **Week 1:** Competitive monitoring active for 3-5 competitors
- **Month 1:** 90% faster competitive analysis vs manual research
- **Quarter 1:** 60% improvement in win rates against tracked competitors
- **Quarter 2:** $200K+ pipeline impact from competitive insights

---

## Recipe 5: Customer Churn Prevention Pipeline

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
  "notifications": ["Assigned CSM", "CSM Manager", "VP Customer Success"]
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

## Recipe 6: AI Support Deflection System

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
    "intentCategories": [
      "resolve_issue",
      "get_information",
      "request_feature",
      "report_bug",
      "cancel_service"
    ]
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
  "kbArticles": ["How to Reset Your API Key", "API Security Best Practices"],
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

## Recipe 7: Customer Education Platform

**Use Case:** Automate customer education and product adoption with guided onboarding, milestone celebrations, and content curation
**Skills:** 6 chained skills
**Time:** Automated vs manual 1-on-1 training sessions
**ROI:** 45% higher product adoption, 60% faster time-to-value, 70% reduction in support tickets

### The Chain

```
guided_setup_wizard → milestone_celebration → community_content_curator →
email_sequence → feedback_collection → activation_metrics
```

### How It Works

1. **guided_setup_wizard** — Walks users through initial product setup step-by-step
2. **milestone_celebration** — Celebrates user achievements to increase engagement
3. **community_content_curator** — Surfaces relevant community content and best practices
4. **email_sequence** — Sends educational email drips based on user progress
5. **feedback_collection** — Gathers user feedback on educational content
6. **activation_metrics** — Tracks activation progress and identifies stuck users

### Setup Instructions

#### Step 1: Install Customer Success & PLG Skills

```bash
npx skills-directory install --target all --domain customer_success plg
```

#### Step 2: Configure Guided Setup

```json
{
  "skill": "guided_setup_wizard",
  "trigger": "user_signup",
  "input": {
    "userId": "{{trigger.userId}}",
    "productComplexity": "medium",
    "setupSteps": [
      {
        "step": 1,
        "title": "Connect your data source",
        "required": true,
        "helpContent": "integration-guide.md"
      },
      {
        "step": 2,
        "title": "Invite your team",
        "required": false,
        "helpContent": "collaboration-guide.md"
      },
      {
        "step": 3,
        "title": "Create your first dashboard",
        "required": true,
        "helpContent": "dashboard-tutorial.md"
      }
    ],
    "adaptiveGuidance": true,
    "allowSkip": false
  },
  "exit_routing": {
    "setup_complete": "milestone_celebration",
    "setup_abandoned": "retention_campaign",
    "stuck": "intervention_trigger"
  }
}
```

#### Step 3: Celebrate Milestones

```json
{
  "skill": "milestone_celebration",
  "input": {
    "userId": "{{chain.userId}}",
    "milestone": "{{previous.completed_step}}",
    "celebrationTypes": {
      "in_app_notification": true,
      "confetti_animation": true,
      "badge_award": true,
      "email_notification": true
    },
    "nextMilestone": "auto_suggest",
    "shareOption": "social_media"
  },
  "exit_routing": {
    "celebrated": "community_content_curator",
    "user_inactive": "re_engagement"
  }
}
```

#### Step 4: Curate Educational Content

```json
{
  "skill": "community_content_curator",
  "input": {
    "userId": "{{chain.userId}}",
    "userProgress": "{{chain.milestones}}",
    "contentTypes": [
      "video_tutorials",
      "how_to_guides",
      "use_cases",
      "community_posts",
      "webinar_recordings"
    ],
    "personalization": {
      "industry": "{{user.industry}}",
      "useCase": "{{user.use_case}}",
      "skillLevel": "{{user.expertise}}"
    },
    "maxItems": 5
  },
  "exit_routing": {
    "content_delivered": "email_sequence",
    "no_relevant_content": "content_creation_request"
  }
}
```

#### Step 5: Send Educational Emails

```json
{
  "skill": "email_sequence",
  "input": {
    "userId": "{{chain.userId}}",
    "sequenceType": "educational_drip",
    "emailSchedule": [
      {
        "day": 1,
        "topic": "Getting Started",
        "content": "{{chain.curated_content[0]}}"
      },
      {
        "day": 3,
        "topic": "Best Practices",
        "content": "{{chain.curated_content[1]}}"
      },
      {
        "day": 7,
        "topic": "Advanced Features",
        "content": "{{chain.curated_content[2]}}"
      }
    ],
    "adaptToProgress": true,
    "includeSuccessStories": true
  },
  "exit_routing": {
    "sequence_started": "feedback_collection",
    "user_unsubscribed": "in_app_only"
  }
}
```

#### Step 6: Collect Feedback

```json
{
  "skill": "feedback_collection",
  "input": {
    "userId": "{{chain.userId}}",
    "feedbackTriggers": ["milestone_reached", "content_consumed", "email_opened", "feature_used"],
    "feedbackTypes": {
      "nps": true,
      "content_rating": true,
      "feature_request": true,
      "help_needed": true
    },
    "frequency": "milestone_based",
    "format": "in_app_modal"
  },
  "exit_routing": {
    "feedback_received": "activation_metrics",
    "negative_feedback": "support_escalation"
  }
}
```

#### Step 7: Track Activation Metrics

```json
{
  "skill": "activation_metrics",
  "input": {
    "userId": "{{chain.userId}}",
    "activationCriteria": [
      "completed_setup",
      "invited_team_member",
      "created_first_artifact",
      "used_core_feature_3_times",
      "returned_3_days_in_week"
    ],
    "timeWindow": "14_days",
    "activationScore": "calculate",
    "identifyBlockers": true
  },
  "output": "activation_report"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/customer-education \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "new-user-456",
    "signupDate": "2026-02-01",
    "industry": "SaaS",
    "useCase": "product_analytics"
  }'
```

### Expected Output

```json
{
  "status": "success",
  "educationPlan": {
    "setupProgress": "67%",
    "milestonesCompleted": 2,
    "milestonesRemaining": 1,
    "contentRecommended": 5,
    "emailsScheduled": 3,
    "feedbackCollected": true,
    "activationScore": 72
  },
  "userEngagement": {
    "setupTime": "12 minutes",
    "contentViews": 3,
    "emailOpenRate": "85%",
    "npsScore": 9,
    "blockers": []
  },
  "nextActions": ["Complete final setup step", "Invite team member", "Explore advanced features"]
}
```

### Monitoring & Metrics

Track these KPIs:

- **Activation Rate:** Target 60%+ within 14 days (baseline ~30%)
- **Time to Value:** Target < 2 days (baseline ~7 days)
- **Content Engagement:** Track views, clicks, completion rates
- **Support Ticket Reduction:** Target 70% fewer "how do I..." tickets
- **NPS from Educated Users:** Target 40+ points

### Expected Outcomes

- **Week 1:** Guided setup deployed, 100+ users onboarded
- **Month 1:** 45% higher activation rate vs. control group
- **Quarter 1:** 60% faster time-to-value, 70% support ticket reduction
- **Quarter 2:** $100K+ saved in customer success time

---

## Recipe 8: AI Ops Conversation Pipeline

**Use Case:** Classify, route, suggest responses, and summarize for support or sales conversations
**Skills:** 4 chained skills (AI Ops)
**Time:** Seconds per ticket; deflected volume
**ROI:** 30–50% deflection, faster first response, consistent summaries

### The Chain

```
ai_ticket_classifier → ai_intent_classifier → ai_response_suggester →
ai_summarization_agent
```

### How It Works

1. **ticket_classifier** — Categories and prioritizes incoming tickets
2. **intent_classifier** — Detects user intent for routing and context
3. **response_suggester** — Suggests replies or next actions
4. **summarization_agent** — Produces conversation or thread summaries

### Setup

Install domain: `npx skills-directory install --target all --domain ai_ops`. Chain the four skills with exit_routing from each step to the next; final step output to your CRM or support queue.

### Expected Outcomes

- **Week 1:** Pipeline running on sample tickets
- **Month 1:** 30%+ deflection or faster resolution
- **Quarter 1:** Summaries used for coaching and reporting

---

## Recipe 9: Customer Onboarding Automation

```
onboarding_health → guided_setup_wizard → milestone_celebration →
time_to_value → activation_metrics
```

**ROI:** 50% faster time-to-value, 30% higher activation

---

## Recipe 10: Support Ticket Triage & Resolution

```
support_ticket_triage → support_resolution_suggester →
support_kb_gap_finder → support_bug_linker
```

**ROI:** 40% faster resolution, 60% ticket deflection

---

## Recipe 11: Growth Optimization Engine

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

## Recipe 12: Content Marketing Automation

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
    "checks": ["keyword_density", "meta_description", "headings", "internal_links", "readability"]
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

## Recipe 13: Freemium Conversion Optimization

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
    "premiumFeatures": [
      "advanced_analytics",
      "team_collaboration",
      "api_access",
      "custom_integrations"
    ],
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

## Recipe 14: Usage-Based Pricing Engine

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

## Recipe 15: Community-Led Growth Engine

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
    "benefits": ["early_feature_access", "exclusive_events", "swag", "revenue_share"],
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
    "moderationRules": ["no_spam", "no_self_promotion", "respectful_tone", "on_topic"],
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

## Recipe 16: Multi-Platform Content Distribution

**Use Case:** Automate content creation, formatting, and distribution across multiple platforms with AI-powered generation and analytics tracking
**Skills:** 6 chained skills
**Time:** 2-3 hours per content piece vs 8-12 hours manual process
**ROI:** 3x content reach, 50% cost reduction, 80% time savings

### The Chain

```
content_research_writer → ai_content_generator → social_content_generator →
email_sequence → analytics_tracking → social_listening_analyzer
```

### How It Works

1. **content_research_writer** — Researches topics, generates outlines, and creates initial drafts
2. **ai_content_generator** — Generates polished content with AI assistance
3. **social_content_generator** — Creates platform-specific social media posts
4. **email_sequence** — Generates email nurture sequences from content
5. **analytics_tracking** — Tracks performance across all distribution channels
6. **social_listening_analyzer** — Monitors social engagement and sentiment

### Setup Instructions

#### Step 1: Install Marketing Skills

```bash
npx skills-directory install --target all --domain marketing
```

#### Step 2: Configure Content Research

```json
{
  "skill": "content_research_writer",
  "trigger": "content_request",
  "input": {
    "topic": "{{trigger.topic}}",
    "audience": "{{company.target_audience}}",
    "contentType": "blog_post",
    "targetLength": 1500,
    "researchDepth": "comprehensive",
    "includeExamples": true,
    "citeSources": true
  },
  "exit_routing": {
    "draft_complete": "ai_content_generator",
    "needs_more_research": "research_deeper"
  }
}
```

#### Step 3: Generate AI-Powered Content

```json
{
  "skill": "ai_content_generator",
  "input": {
    "draft": "{{previous.draft}}",
    "tone": "professional_friendly",
    "style": "{{company.brand_voice}}",
    "optimizeFor": ["clarity", "engagement", "seo", "readability"],
    "includeCallToAction": true,
    "targetKeyword": "{{previous.primary_keyword}}"
  },
  "exit_routing": {
    "content_ready": "social_content_generator",
    "needs_editing": "human_review"
  }
}
```

#### Step 4: Create Social Media Content

```json
{
  "skill": "social_content_generator",
  "input": {
    "article": "{{previous.content}}",
    "platforms": ["twitter", "linkedin", "facebook", "instagram"],
    "postsPerPlatform": 3,
    "includeHashtags": true,
    "includeImages": true,
    "schedulingStrategy": "optimal_times"
  },
  "exit_routing": {
    "social_ready": "email_sequence",
    "needs_images": "image_generation"
  }
}
```

#### Step 5: Generate Email Nurture Sequence

```json
{
  "skill": "email_sequence",
  "input": {
    "content": "{{chain.article}}",
    "sequenceType": "nurture",
    "emailCount": 3,
    "spacing": "3_days",
    "personalization": "high",
    "segmentation": "by_behavior",
    "includeUnsubscribe": true
  },
  "exit_routing": {
    "sequence_ready": "analytics_tracking",
    "needs_approval": "marketing_review"
  }
}
```

#### Step 6: Track Analytics

```json
{
  "skill": "analytics_tracking",
  "input": {
    "contentId": "{{chain.contentId}}",
    "trackingEvents": [
      "page_view",
      "time_on_page",
      "social_share",
      "email_open",
      "email_click",
      "conversion"
    ],
    "platforms": "all",
    "reportingFrequency": "daily"
  },
  "exit_routing": {
    "tracking_active": "social_listening_analyzer"
  }
}
```

#### Step 7: Monitor Social Engagement

```json
{
  "skill": "social_listening_analyzer",
  "input": {
    "contentUrl": "{{chain.publish_url}}",
    "keywords": "{{chain.target_keywords}}",
    "platforms": ["twitter", "linkedin", "reddit", "hackernews"],
    "sentimentAnalysis": true,
    "competitorMentions": true,
    "alertThreshold": "high_engagement"
  },
  "output": "engagement_report"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/content-distribution \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI-powered workflow automation",
    "targetAudience": "B2B SaaS founders",
    "contentType": "blog_post",
    "distributionChannels": ["blog", "social", "email"]
  }'
```

### Expected Output

```json
{
  "contentGenerated": true,
  "articleUrl": "https://blog.example.com/ai-workflow-automation",
  "wordCount": 1500,
  "readabilityScore": 65,
  "socialPosts": {
    "twitter": 3,
    "linkedin": 3,
    "facebook": 3
  },
  "emailSequence": {
    "emails": 3,
    "scheduled": true
  },
  "analyticsTracking": "active",
  "socialListening": "monitoring",
  "estimatedReach": "15000+",
  "productionTime": "2.5 hours"
}
```

### Monitoring & Metrics

Track these KPIs:

- **Content Production Volume:** Target 3x increase
- **Time per Piece:** Target 70% reduction
- **Cross-Platform Reach:** Target 3x increase
- **Engagement Rate:** Target 25% improvement
- **Content-to-Conversion Rate:** Track ROI per piece

### Expected Outcomes

- **Week 1:** 3 pieces published across all channels
- **Month 1:** 20+ pieces published (vs 8-10 manual)
- **Quarter 1:** 3x content reach, 50% cost reduction
- **Quarter 2:** Content team 3x more productive

---

## Recipe 17: Pricing & Packaging Optimization

```
pricing_strategy → packaging_optimizer → price_experimentation →
upgrade_trigger → consumption_analyzer
```

**ROI:** 15-25% revenue per customer increase

---

## Recipe 18: Product Analytics Intelligence

```
product_analytics → feature_adoption → friction_detector →
pql_scoring → expansion_playbook
```

**ROI:** 2x product-led pipeline generation

---

## Phase 2: High-Confidence Recipes (11-28)

These recipes expand into new domains with 95%+ skill coverage validated against the library.

---

## Recipe 19: Developer Experience Onboarding

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

## Recipe 20: Product Experimentation Engine

**Use Case:** Accelerate product experimentation with automated A/B test setup, analysis, and impact measurement
**Skills:** 6 chained skills
**Time:** 10-15 experiments/month vs 2-4 manual experiments
**ROI:** 5x experiment velocity, 25% faster product iteration, 20% conversion lift

### The Chain

```
experimentation → ab_test_setup → analytics_tracking →
feature_adoption → impact_analyzer → friction_detector
```

### How It Works

1. **experimentation** — Designs and configures product experiments
2. **ab_test_setup** — Sets up A/B tests with proper statistical controls
3. **analytics_tracking** — Tracks experiment metrics and user behavior
4. **feature_adoption** — Monitors feature adoption rates and patterns
5. **impact_analyzer** — Analyzes business impact of product changes
6. **friction_detector** — Identifies friction points in user experience

### Setup Instructions

#### Step 1: Install Product Ops & PLG Skills

```bash
npx skills-directory install --target all --domain product_ops plg
```

#### Step 2: Configure Experimentation Framework

```json
{
  "skill": "experimentation",
  "trigger": "experiment_proposal",
  "input": {
    "experimentId": "{{trigger.experimentId}}",
    "hypothesis": "{{trigger.hypothesis}}",
    "targetMetric": "{{trigger.primary_metric}}",
    "userSegment": "{{trigger.segment}}",
    "experimentType": "ab_test",
    "successCriteria": {
      "statistical_significance": 0.95,
      "minimum_effect_size": 0.05,
      "minimum_sample_size": 1000
    }
  },
  "exit_routing": {
    "design_complete": "ab_test_setup",
    "needs_refinement": "experiment_review"
  }
}
```

#### Step 3: Setup A/B Test

```json
{
  "skill": "ab_test_setup",
  "input": {
    "experimentId": "{{chain.experimentId}}",
    "variants": ["control", "variant_a", "variant_b"],
    "trafficAllocation": {
      "control": 34,
      "variant_a": 33,
      "variant_b": 33
    },
    "targetingRules": "{{previous.segment}}",
    "duration": "14_days",
    "rampUpStrategy": "gradual"
  },
  "exit_routing": {
    "test_live": "analytics_tracking",
    "configuration_error": "fix_and_retry"
  }
}
```

#### Step 4: Track Experiment Metrics

```json
{
  "skill": "analytics_tracking",
  "input": {
    "experimentId": "{{chain.experimentId}}",
    "events": [
      "experiment_exposure",
      "primary_metric_event",
      "secondary_metric_event",
      "conversion_event"
    ],
    "granularity": "user_level",
    "cohortTracking": true,
    "realTimeAnalysis": true
  },
  "exit_routing": {
    "tracking_active": "feature_adoption",
    "data_quality_issue": "alert_team"
  }
}
```

#### Step 5: Monitor Feature Adoption

```json
{
  "skill": "feature_adoption",
  "input": {
    "experimentId": "{{chain.experimentId}}",
    "features": "{{previous.new_features}}",
    "adoptionMetrics": [
      "first_use_rate",
      "repeat_use_rate",
      "power_user_adoption",
      "time_to_adoption"
    ],
    "cohortComparison": true,
    "timeWindow": "30_days"
  },
  "exit_routing": {
    "adoption_tracked": "impact_analyzer",
    "low_adoption": "friction_detector"
  }
}
```

#### Step 6: Analyze Business Impact

```json
{
  "skill": "impact_analyzer",
  "input": {
    "experimentId": "{{chain.experimentId}}",
    "businessMetrics": ["revenue_impact", "retention_impact", "ltv_impact", "engagement_impact"],
    "statisticalMethod": "bayesian",
    "confidenceLevel": 0.95,
    "includeSegmentAnalysis": true
  },
  "exit_routing": {
    "significant_winner": "rollout_recommendation",
    "inconclusive": "extend_experiment",
    "significant_negative": "rollback_recommendation"
  }
}
```

#### Step 7: Detect User Friction

```json
{
  "skill": "friction_detector",
  "input": {
    "experimentId": "{{chain.experimentId}}",
    "frictionSignals": [
      "high_bounce_rate",
      "abandoned_flows",
      "error_rate",
      "support_tickets",
      "negative_feedback"
    ],
    "variantComparison": true,
    "alertThreshold": "medium"
  },
  "output": "friction_report_with_recommendations"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/experimentation \
  -H "Content-Type: application/json" \
  -d '{
    "experimentId": "exp_001",
    "hypothesis": "Simplified signup flow increases conversion by 15%",
    "primaryMetric": "signup_completion_rate",
    "userSegment": "new_visitors"
  }'
```

### Expected Output

```json
{
  "experimentLive": true,
  "variants": {
    "control": "current_3_step_flow",
    "variant_a": "simplified_1_step",
    "variant_b": "2_step_with_social"
  },
  "sampleSize": 3000,
  "currentResults": {
    "control": "12.5% conversion",
    "variant_a": "18.3% conversion (+46%)",
    "variant_b": "15.7% conversion (+26%)"
  },
  "statisticalSignificance": 0.98,
  "winner": "variant_a",
  "recommendation": "Roll out variant_a to 100% of users",
  "estimatedImpact": "$150K annual revenue increase"
}
```

### Monitoring & Metrics

Track these KPIs:

- **Experiment Velocity:** Target 10-15 experiments/month
- **Time to Results:** Target < 14 days per experiment
- **Winner Rate:** Target 40%+ experiments produce winners
- **Impact per Experiment:** Track cumulative revenue/engagement impact
- **Experimentation Culture:** Track % of product decisions backed by experiments

### Expected Outcomes

- **Week 1:** First 3 experiments launched
- **Month 1:** 10-15 experiments running concurrently
- **Quarter 1:** 5x increase in experiment velocity
- **Quarter 2:** 20% cumulative conversion improvement from winning experiments

---

## Recipe 21: API Lifecycle Management

**Use Case:** Manage API versioning, deprecations, and breaking changes with automated migration assistance and developer notifications
**Skills:** 6 chained skills
**Time:** Automated change management vs 40+ hours per API update
**ROI:** 50% reduction in breaking change impact, 70% faster migrations, 90% developer satisfaction

### The Chain

```
api_deprecation → changelog_tracker → migration_assistant →
deprecation_notifier → webhook_tester → integration_health
```

### How It Works

1. **api_deprecation** — Plans and manages API deprecation timelines
2. **changelog_tracker** — Tracks and communicates API changes to developers
3. **migration_assistant** — Provides automated migration guidance and code samples
4. **deprecation_notifier** — Notifies affected customers about upcoming changes
5. **webhook_tester** — Tests webhook integrations before and after changes
6. **integration_health** — Monitors integration health across API versions

### Setup Instructions

#### Step 1: Install DevEx & Product Ops Skills

```bash
npx skills-directory install --target all --domain devex product_ops
```

#### Step 2: Configure API Deprecation Planning

```json
{
  "skill": "api_deprecation",
  "trigger": "deprecation_proposal",
  "input": {
    "apiEndpoint": "{{trigger.endpoint}}",
    "currentVersion": "{{trigger.version}}",
    "deprecationReason": "{{trigger.reason}}",
    "timelineMonths": 6,
    "migrationPath": "{{trigger.new_endpoint}}",
    "breakingChange": true,
    "affectedCustomers": "auto_calculate"
  },
  "exit_routing": {
    "plan_approved": "changelog_tracker",
    "needs_review": "api_review_board"
  }
}
```

#### Step 3: Track and Communicate Changes

```json
{
  "skill": "changelog_tracker",
  "input": {
    "deprecationId": "{{previous.deprecationId}}",
    "changeType": "deprecation",
    "affectedEndpoints": "{{previous.endpoints}}",
    "releaseNotes": "auto_generate",
    "changelogFormat": "markdown",
    "distributionChannels": ["email", "developer_portal", "slack", "rss"],
    "versionTagging": "semver"
  },
  "exit_routing": {
    "changelog_published": "migration_assistant",
    "needs_technical_writer": "documentation_review"
  }
}
```

#### Step 4: Provide Migration Assistance

```json
{
  "skill": "migration_assistant",
  "input": {
    "deprecationId": "{{chain.deprecationId}}",
    "fromVersion": "{{chain.current_version}}",
    "toVersion": "{{chain.new_version}}",
    "migrationGuides": "auto_generate",
    "codeExamples": ["python", "javascript", "ruby", "go"],
    "diffVisualization": true,
    "interactiveTutorial": true
  },
  "exit_routing": {
    "migration_docs_ready": "deprecation_notifier",
    "needs_custom_examples": "engineering_support"
  }
}
```

#### Step 5: Notify Affected Customers

```json
{
  "skill": "deprecation_notifier",
  "input": {
    "deprecationId": "{{chain.deprecationId}}",
    "affectedCustomers": "{{chain.affected_list}}",
    "notificationSchedule": ["180_days", "90_days", "30_days", "7_days"],
    "notificationChannels": ["email", "in_app", "dashboard_banner"],
    "urgencyLevel": "high",
    "includeMigrationLink": true,
    "offerSupport": true
  },
  "exit_routing": {
    "customers_notified": "webhook_tester",
    "delivery_failed": "retry_notification"
  }
}
```

#### Step 6: Test Webhook Integrations

```json
{
  "skill": "webhook_tester",
  "input": {
    "deprecationId": "{{chain.deprecationId}}",
    "webhookEndpoints": "{{customer.webhook_urls}}",
    "testPayloads": "{{chain.new_version_payloads}}",
    "validationRules": "strict",
    "retryLogic": "test",
    "timeoutSettings": "verify"
  },
  "exit_routing": {
    "tests_passed": "integration_health",
    "tests_failed": "customer_support_alert"
  }
}
```

#### Step 7: Monitor Integration Health

```json
{
  "skill": "integration_health",
  "input": {
    "deprecationId": "{{chain.deprecationId}}",
    "customerId": "{{customer.id}}",
    "healthMetrics": [
      "api_success_rate",
      "response_times",
      "error_rates",
      "version_adoption",
      "webhook_delivery_rate"
    ],
    "monitoringWindow": "continuous",
    "alerting": "proactive"
  },
  "output": "health_dashboard"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/api-lifecycle \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "/api/v1/users",
    "deprecationReason": "Moving to /api/v2/users with improved schema",
    "timelineMonths": 6,
    "affectedCustomers": 150
  }'
```

### Expected Output

```json
{
  "deprecationPlanned": true,
  "deprecationId": "dep_001",
  "timeline": {
    "announcement": "2026-03-01",
    "final_notification": "2026-08-01",
    "sunset_date": "2026-09-01"
  },
  "changelogPublished": true,
  "migrationDocsUrl": "https://docs.example.com/migrations/v1-to-v2",
  "customersNotified": 150,
  "webhookTestsPassed": 142,
  "webhookTestsFailed": 8,
  "migrationProgress": {
    "completed": 0,
    "in_progress": 0,
    "not_started": 150
  },
  "supportTicketsCreated": 3
}
```

### Monitoring & Metrics

Track these KPIs:

- **Migration Completion Rate:** Target > 95% before sunset
- **Breaking Change Impact:** Target < 5% customer disruption
- **Developer Satisfaction:** Target > 4.5/5 for deprecation process
- **Time to Migrate:** Track average customer migration time
- **Support Burden:** Track support tickets per deprecation

### Expected Outcomes

- **Week 1:** Deprecation announced, migration docs published
- **Month 1:** 30% of customers started migration
- **Month 3:** 70% of customers migrated
- **Month 6:** 95%+ migration completion, smooth sunset

---

## Recipe 22: Security Code Review Automation

**Use Case:** Automate security code reviews with vulnerability detection, variant analysis, and fix recommendations
**Skills:** 6 chained skills
**Time:** Real-time scanning vs manual quarterly audits
**ROI:** 70% faster vulnerability detection, 80% faster remediation, 90% reduction in security debt

### The Chain

```
semgrep-rule-creator → entry-point-analyzer → variant-analysis →
differential-review → fix-review → property-based-testing
```

### How It Works

1. **semgrep-rule-creator** — Creates custom security rules for codebase-specific patterns
2. **entry-point-analyzer** — Identifies code entry points and attack surfaces
3. **variant-analysis** — Finds similar vulnerabilities across the codebase
4. **differential-review** — Reviews code changes for security implications
5. **fix-review** — Validates security fixes and suggests improvements
6. **property-based-testing** — Generates tests to verify security properties

### Setup Instructions

#### Step 1: Install Security Skills

```bash
npx skills-directory install --target all --domain security
```

#### Step 2: Configure Security Rule Creation

```json
{
  "skill": "semgrep-rule-creator",
  "trigger": "vulnerability_identified",
  "input": {
    "vulnerabilityType": "{{trigger.vuln_type}}",
    "language": "{{repo.primary_language}}",
    "codeContext": "{{trigger.code_sample}}",
    "severity": "{{trigger.severity}}",
    "ruleScope": "project_wide",
    "autofix": true,
    "testCases": "generate"
  },
  "exit_routing": {
    "rule_created": "entry-point-analyzer",
    "needs_expert_input": "security_team_review"
  }
}
```

#### Step 3: Analyze Entry Points

```json
{
  "skill": "entry-point-analyzer",
  "input": {
    "repository": "{{repo.path}}",
    "securityRules": "{{previous.rules}}",
    "entryPointTypes": [
      "api_endpoints",
      "user_inputs",
      "file_uploads",
      "authentication",
      "database_queries"
    ],
    "attackSurface": "calculate",
    "dataFlowTracking": true
  },
  "exit_routing": {
    "entry_points_mapped": "variant-analysis",
    "critical_surface_found": "immediate_alert"
  }
}
```

#### Step 4: Find Vulnerability Variants

```json
{
  "skill": "variant-analysis",
  "input": {
    "vulnerabilityPattern": "{{trigger.pattern}}",
    "entryPoints": "{{previous.entry_points}}",
    "codebase": "{{repo.path}}",
    "similarityThreshold": 0.75,
    "analysisDepth": "deep",
    "includeIndirect": true,
    "prioritize": "by_exploitability"
  },
  "exit_routing": {
    "variants_found": "differential-review",
    "no_variants": "fix-review"
  }
}
```

#### Step 5: Review Code Changes

```json
{
  "skill": "differential-review",
  "input": {
    "pullRequest": "{{trigger.pr_number}}",
    "changedFiles": "{{pr.files}}",
    "securityFocus": [
      "authentication_bypass",
      "injection_attacks",
      "data_exposure",
      "access_control",
      "cryptography_misuse"
    ],
    "compareAgainst": "main",
    "severityFiltering": "high_critical_only"
  },
  "exit_routing": {
    "issues_found": "fix-review",
    "clean": "approve_pr",
    "critical_issue": "block_merge"
  }
}
```

#### Step 6: Review Proposed Fixes

```json
{
  "skill": "fix-review",
  "input": {
    "originalVulnerability": "{{chain.vulnerability}}",
    "proposedFix": "{{trigger.fix_code}}",
    "reviewCriteria": {
      "completeness": true,
      "noNewVulnerabilities": true,
      "performanceImpact": true,
      "compatibilityCheck": true
    },
    "suggestImprovements": true,
    "referenceSecurePatterns": true
  },
  "exit_routing": {
    "fix_approved": "property-based-testing",
    "fix_inadequate": "request_revision",
    "better_approach": "suggest_alternative"
  }
}
```

#### Step 7: Generate Security Tests

```json
{
  "skill": "property-based-testing",
  "input": {
    "vulnerabilityType": "{{chain.vuln_type}}",
    "fixedCode": "{{previous.approved_fix}}",
    "securityProperties": [
      "input_validation",
      "output_encoding",
      "access_control",
      "data_integrity",
      "confidentiality"
    ],
    "testFramework": "{{repo.test_framework}}",
    "edgeCases": "generate",
    "fuzzingEnabled": true
  },
  "output": "generate_test_suite"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/security-review \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "my-app",
    "scanType": "full",
    "severityFilter": ["high", "critical"],
    "autoFixEnabled": true
  }'
```

### Expected Output

```json
{
  "status": "success",
  "securityScan": {
    "vulnerabilitiesFound": 12,
    "criticalIssues": 2,
    "highIssues": 4,
    "mediumIssues": 6,
    "variantsIdentified": 8,
    "entryPointsAnalyzed": 45,
    "attackSurfaceScore": "medium"
  },
  "remediation": {
    "rulesCreated": 5,
    "autofixesApplied": 6,
    "manualReviewNeeded": 6,
    "testsGenerated": 15,
    "estimatedFixTime": "4 hours"
  },
  "recommendations": [
    "Add input validation to user profile endpoints",
    "Implement rate limiting on authentication routes",
    "Update cryptography library to latest version"
  ]
}
```

### Monitoring & Metrics

Track these KPIs:

- **Vulnerability Detection Rate:** Target 95%+ coverage
- **Mean Time to Detection (MTTD):** Target < 1 day (baseline ~30 days)
- **Mean Time to Resolution (MTTR):** Target < 3 days (baseline ~15 days)
- **False Positive Rate:** Target < 10%
- **Security Debt:** Track trend over time

### Expected Outcomes

- **Week 1:** Automated scanning active, 50+ vulnerabilities detected
- **Month 1:** 70% faster detection, 80% faster remediation
- **Quarter 1:** 90% reduction in security debt, <5 critical issues
- **Quarter 2:** Zero critical vulnerabilities in production

---

## Recipe 23: Superpowers Development Workflow

**Use Case:** Structured development from idea to verified implementation
**Skills:** 4 chained skills
**Time:** Reduces rework; plan before coding, verify before completion
**ROI:** Fewer broken branches, clearer specs, consistent quality

### The Chain

```
superpowers/brainstorming → superpowers/writing-plans →
superpowers/executing-plans → superpowers/verification-before-completion
```

### How It Works

1. **brainstorming** — Explores intent, requirements, and design before implementation
2. **writing-plans** — Produces a concrete implementation plan
3. **executing-plans** — Runs the plan (e.g. code changes)
4. **verification-before-completion** — Validates work before marking done

### Setup Instructions

#### Step 1: Install Superpowers Skills

```bash
npx skills-directory install --target all --domain superpowers
```

#### Step 2: Configure the Chain

```json
{
  "skill": "superpowers/brainstorming",
  "input": {
    "initialIdea": "{{task.description}}",
    "projectContext": "{{project}}"
  },
  "exit_routing": { "success": "superpowers/writing-plans" }
}
```

```json
{
  "skill": "superpowers/writing-plans",
  "input": {
    "design": "{{previous.design}}",
    "refinedRequirements": "{{previous.refinedRequirements}}"
  },
  "exit_routing": { "success": "superpowers/executing-plans" }
}
```

```json
{
  "skill": "superpowers/executing-plans",
  "input": {
    "plan": "{{previous.plan}}",
    "context": "{{chain.context}}"
  },
  "exit_routing": { "success": "superpowers/verification-before-completion" }
}
```

```json
{
  "skill": "superpowers/verification-before-completion",
  "input": {
    "artifacts": "{{previous.output}}",
    "successCriteria": "{{chain.design.successCriteria}}"
  },
  "output": "verified_output"
}
```

### Expected Outcomes

- **Week 1:** Team uses chain for 2–3 features
- **Month 1:** Fewer "done but broken" merges; clearer handoffs
- **Quarter 1:** Habit of plan → execute → verify

---

## Recipe 24: Brand Consistency Engine

**Use Case:** Ensure brand consistency across all content, design, and communication channels with automated brand guideline enforcement and voice validation
**Skills:** 6 chained skills
**Time:** Real-time validation vs manual review cycles
**ROI:** 80% brand compliance, 60% faster asset production, 90% reduction in off-brand content

### The Chain

```
brand_guidelines → skene_voice_guardian → humanization_engine →
copywriting → theme_factory → canvas_design
```

### How It Works

1. **brand_guidelines** — Establishes and enforces brand standards (colors, fonts, tone, messaging)
2. **skene_voice_guardian** — Validates content against brand voice and style guidelines
3. **humanization_engine** — Ensures content feels authentic and human while maintaining brand voice
4. **copywriting** — Generates on-brand copy for various channels
5. **theme_factory** — Creates consistent visual themes across platforms
6. **canvas_design** — Produces on-brand design assets at scale

### Setup Instructions

#### Step 1: Install Marketing Skills

```bash
npx skills-directory install --target all --domain marketing
```

#### Step 2: Configure Brand Guidelines

```json
{
  "skill": "brand_guidelines",
  "trigger": "content_creation",
  "input": {
    "brandName": "{{company.name}}",
    "brandAssets": {
      "primaryColors": ["#FF6B6B", "#4ECDC4", "#45B7D1"],
      "secondaryColors": ["#FFA07A", "#98D8C8"],
      "fonts": {
        "heading": "Montserrat",
        "body": "Open Sans"
      },
      "logoVariants": ["primary", "white", "black", "icon"]
    },
    "brandVoice": {
      "tone": ["professional", "approachable", "innovative"],
      "avoidWords": ["cheap", "discount", "revolutionary"],
      "preferWords": ["effective", "proven", "innovative"]
    },
    "messagingPillars": ["Customer-first innovation", "Proven results", "Transparent pricing"]
  },
  "exit_routing": {
    "guidelines_set": "skene_voice_guardian",
    "needs_review": "brand_team_approval"
  }
}
```

#### Step 3: Validate Brand Voice

```json
{
  "skill": "skene_voice_guardian",
  "input": {
    "content": "{{trigger.content}}",
    "brandGuidelines": "{{previous.guidelines}}",
    "contentType": "{{trigger.type}}",
    "validationRules": {
      "toneMatch": true,
      "terminologyCheck": true,
      "messagingAlignment": true,
      "prohibitedWords": true
    },
    "strictnessLevel": "high"
  },
  "exit_routing": {
    "approved": "humanization_engine",
    "violations_found": "revision_required",
    "minor_issues": "auto_correct"
  }
}
```

#### Step 4: Humanize Content

```json
{
  "skill": "humanization_engine",
  "input": {
    "content": "{{previous.validated_content}}",
    "brandVoice": "{{chain.brand_voice}}",
    "humanizationGoals": [
      "natural_conversational_tone",
      "remove_corporate_speak",
      "add_personality",
      "maintain_professionalism"
    ],
    "preserveBrandTerms": true,
    "targetReadability": "grade_8"
  },
  "exit_routing": {
    "humanized": "copywriting",
    "needs_refinement": "humanize_again"
  }
}
```

#### Step 5: Generate Copy Variants

```json
{
  "skill": "copywriting",
  "input": {
    "baseContent": "{{previous.humanized_content}}",
    "brandGuidelines": "{{chain.guidelines}}",
    "channels": ["website", "email", "social_media", "ads", "product_descriptions"],
    "variants": {
      "headlines": 5,
      "bodyCopy": 3,
      "ctas": 5
    },
    "optimizeFor": "conversion"
  },
  "exit_routing": {
    "copy_ready": "theme_factory",
    "needs_ab_test": "experimentation"
  }
}
```

#### Step 6: Create Visual Themes

```json
{
  "skill": "theme_factory",
  "input": {
    "brandGuidelines": "{{chain.guidelines}}",
    "contentContext": "{{chain.all_copy}}",
    "platforms": ["web", "mobile", "email", "social"],
    "themeComponents": {
      "colorSchemes": 3,
      "typographyPairings": 2,
      "layoutTemplates": 5,
      "componentStyles": "design_system_compliant"
    }
  },
  "exit_routing": {
    "themes_created": "canvas_design",
    "needs_designer_input": "design_review"
  }
}
```

#### Step 7: Generate Design Assets

```json
{
  "skill": "canvas_design",
  "input": {
    "theme": "{{previous.selected_theme}}",
    "copy": "{{chain.copy}}",
    "brandAssets": "{{chain.brand_assets}}",
    "assetTypes": [
      "social_media_posts",
      "banner_ads",
      "email_headers",
      "presentation_slides",
      "infographics"
    ],
    "dimensions": "platform_optimized",
    "outputFormat": ["png", "svg", "pdf"]
  },
  "output": "deliver_assets"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/brand-consistency \
  -H "Content-Type: application/json" \
  -d '{
    "contentType": "blog_post",
    "topic": "Product Launch Announcement",
    "channel": "website",
    "designNeeds": ["hero_image", "social_cards"]
  }'
```

### Expected Output

```json
{
  "status": "success",
  "brandCompliance": "100%",
  "voiceScore": 95,
  "humanizationScore": 88,
  "assetsGenerated": {
    "copyVariants": {
      "headlines": 5,
      "bodyCopy": 3,
      "ctas": 5
    },
    "designAssets": {
      "hero_image": "launch-hero-v1.png",
      "social_cards": ["twitter-card.png", "linkedin-card.png", "facebook-card.png"],
      "email_header": "launch-email-header.png"
    }
  },
  "validationsPassed": ["tone_check", "terminology_check", "color_compliance", "font_compliance"],
  "productionTime": "45 minutes"
}
```

### Monitoring & Metrics

Track these KPIs:

- **Brand Compliance Rate:** Target > 95% (baseline ~60%)
- **Asset Production Speed:** Target 80% faster than manual
- **Off-Brand Content:** Target < 5% rejection rate
- **Designer Time Saved:** Track hours per month
- **Content Consistency Score:** Target > 90% across channels

### Expected Outcomes

- **Week 1:** Brand guidelines enforced, voice validation active
- **Month 1:** 80% reduction in off-brand content rejections
- **Quarter 1:** 60% faster asset production, 95%+ brand compliance
- **Quarter 2:** $50K+ saved in design/creative time

---

## Recipe 25: Employee Onboarding Automation

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

## Recipe 26: Data Quality Automation

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
      { "name": "weekly_active", "criteria": "weekly_sessions >= 3" },
      { "name": "power_users", "criteria": "monthly_actions >= 100" },
      { "name": "at_risk", "criteria": "days_since_last_activity > 14" }
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

## Recipe 27: Compliance Automation Hub

**Use Case:** Automate compliance monitoring, audit preparation, and regulatory reporting across GDPR, SOC 2, and other frameworks
**Skills:** 6 chained skills
**Time:** Real-time monitoring vs quarterly manual audits
**ROI:** 90% faster compliance reporting, 60% risk reduction, 80% audit prep time savings

### The Chain

```
compliance_gdpr_manager → compliance_soc2_tracker → compliance_audit_preparer →
compliance_vendor_risk → compliance_pii_detector → compliance_data_retention
```

### How It Works

1. **compliance_gdpr_manager** — Manages GDPR compliance requirements and data subject requests
2. **compliance_soc2_tracker** — Tracks SOC 2 controls and evidence collection
3. **compliance_audit_preparer** — Prepares audit packages and documentation
4. **compliance_vendor_risk** — Assesses third-party vendor compliance risks
5. **compliance_pii_detector** — Identifies and protects personally identifiable information
6. **compliance_data_retention** — Enforces data retention and deletion policies

### Setup Instructions

#### Step 1: Install Compliance Skills

```bash
npx skills-directory install --target all --domain compliance
```

#### Step 2: Configure GDPR Management

```json
{
  "skill": "compliance_gdpr_manager",
  "trigger": "data_subject_request",
  "input": {
    "requestType": "{{trigger.type}}",
    "dataSubject": "{{trigger.user_id}}",
    "complianceFrameworks": ["GDPR", "CCPA", "LGPD"],
    "actions": {
      "dataMapping": true,
      "consentTracking": true,
      "rightToAccess": true,
      "rightToErasure": true,
      "dataPortability": true
    },
    "responseDeadline": "30_days",
    "automateWherePossible": true
  },
  "exit_routing": {
    "request_fulfilled": "compliance_soc2_tracker",
    "manual_review_needed": "legal_team_review",
    "deadline_approaching": "escalate"
  }
}
```

#### Step 3: Track SOC 2 Controls

```json
{
  "skill": "compliance_soc2_tracker",
  "input": {
    "trustServiceCriteria": ["security", "availability", "confidentiality"],
    "controls": [
      {
        "id": "CC6.1",
        "category": "Logical_and_Physical_Access_Controls",
        "frequency": "continuous"
      },
      {
        "id": "CC7.2",
        "category": "System_Operations",
        "frequency": "daily"
      }
    ],
    "evidenceCollection": "automated",
    "auditReadiness": "calculate",
    "gapAnalysis": true
  },
  "exit_routing": {
    "controls_met": "compliance_audit_preparer",
    "gaps_identified": "remediation_plan",
    "critical_failure": "immediate_escalation"
  }
}
```

#### Step 4: Prepare Audit Package

```json
{
  "skill": "compliance_audit_preparer",
  "input": {
    "auditType": "{{trigger.audit_type}}",
    "frameworks": "{{chain.frameworks}}",
    "evidenceScope": {
      "policies": true,
      "procedures": true,
      "controls": true,
      "incidentReports": true,
      "accessLogs": true,
      "changeManagement": true
    },
    "timePeriod": "last_12_months",
    "format": "auditor_preferred",
    "autoGenerate": "executive_summary"
  },
  "exit_routing": {
    "package_ready": "compliance_vendor_risk",
    "missing_evidence": "evidence_collection_trigger"
  }
}
```

#### Step 5: Assess Vendor Risk

```json
{
  "skill": "compliance_vendor_risk",
  "input": {
    "vendors": "{{company.third_party_vendors}}",
    "riskCategories": [
      "data_processing",
      "security_posture",
      "compliance_certifications",
      "breach_history",
      "geographic_location"
    ],
    "assessmentFrequency": "quarterly",
    "riskScoring": "weighted",
    "includeSubprocessors": true,
    "actionThresholds": {
      "high_risk": "immediate_review",
      "medium_risk": "quarterly_review",
      "low_risk": "annual_review"
    }
  },
  "exit_routing": {
    "assessment_complete": "compliance_pii_detector",
    "high_risk_vendor": "vendor_audit_trigger"
  }
}
```

#### Step 6: Detect PII

```json
{
  "skill": "compliance_pii_detector",
  "input": {
    "scanTargets": ["databases", "file_storage", "logs", "backups", "code_repositories"],
    "piiTypes": ["email", "phone", "ssn", "credit_card", "address", "biometric", "health_data"],
    "classification": "automatic",
    "anonymizationSuggestions": true,
    "alertOnUnprotected": true
  },
  "exit_routing": {
    "pii_mapped": "compliance_data_retention",
    "unprotected_pii": "encryption_trigger"
  }
}
```

#### Step 7: Enforce Data Retention

```json
{
  "skill": "compliance_data_retention",
  "input": {
    "dataCategories": "{{previous.pii_categories}}",
    "retentionPolicies": {
      "user_data": "7_years",
      "logs": "2_years",
      "analytics": "3_years",
      "marketing": "2_years_or_consent_withdrawn"
    },
    "deletionMethod": "secure_permanent",
    "verificationRequired": true,
    "auditTrail": "maintain",
    "automatedDeletion": true,
    "exceptions": "legal_hold_aware"
  },
  "output": "retention_report"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/compliance-automation \
  -H "Content-Type: application/json" \
  -d '{
    "complianceCheck": "full_audit_prep",
    "frameworks": ["GDPR", "SOC2"],
    "reportFormat": "executive_summary"
  }'
```

### Expected Output

```json
{
  "status": "success",
  "complianceStatus": {
    "gdpr": {
      "compliant": true,
      "dataSubjectRequests": 45,
      "requestsFulfilled": 45,
      "averageResponseTime": "8 days"
    },
    "soc2": {
      "controlsMet": "98%",
      "evidenceCollected": 1250,
      "gapsIdentified": 2,
      "auditReadiness": "high"
    }
  },
  "risks": {
    "vendorRisks": 3,
    "unprotectedPII": 0,
    "retentionViolations": 0
  },
  "auditPackage": {
    "documentsIncluded": 85,
    "evidenceItems": 1250,
    "coveragePeriod": "12 months",
    "readiness": "audit_ready"
  }
}
```

### Monitoring & Metrics

Track these KPIs:

- **Compliance Score:** Target > 95% across all frameworks
- **Data Subject Request Response Time:** Target < 10 days (legal max: 30)
- **Vendor Risk Score:** Track average and trend
- **Audit Preparation Time:** Target 80% reduction vs manual
- **Compliance Incidents:** Target zero violations

### Expected Outcomes

- **Week 1:** Compliance monitoring active, gaps identified
- **Month 1:** 90% faster compliance reporting, real-time dashboards
- **Quarter 1:** 98%+ SOC 2 control coverage, audit-ready
- **Quarter 2:** Zero compliance violations, successful audit completion

---

## Recipe 28: E-commerce Revenue Optimization

**Use Case:** Optimize e-commerce pricing, packaging, and monetization strategies to maximize revenue and margins
**Skills:** 6 chained skills
**Time:** Real-time optimization vs quarterly pricing reviews
**ROI:** 30% revenue increase, 20% margin improvement, 25% better conversion rates

### The Chain

```
pricing_strategy → packaging_optimizer → price_experimentation →
upgrade_trigger → consumption_analyzer → invoice_explainer
```

### How It Works

1. **pricing_strategy** — Analyzes market positioning and recommends optimal pricing
2. **packaging_optimizer** — Designs product packaging and tier structures
3. **price_experimentation** — Runs A/B tests on pricing and packaging
4. **upgrade_trigger** — Identifies optimal moments for upsell/cross-sell
5. **consumption_analyzer** — Tracks product usage and consumption patterns
6. **invoice_explainer** — Provides transparent billing explanations to reduce churn

### Setup Instructions

#### Step 1: Install Monetization Skills

```bash
npx skills-directory install --target all --domain monetization
```

#### Step 2: Configure Pricing Strategy

```json
{
  "skill": "pricing_strategy",
  "trigger": "pricing_review",
  "input": {
    "currentPricing": "{{company.pricing_tiers}}",
    "competitorPricing": "{{market_research.competitors}}",
    "customerSegments": [
      {
        "segment": "SMB",
        "willingness_to_pay": "$50-200/month",
        "value_drivers": ["ease_of_use", "support"]
      },
      {
        "segment": "Enterprise",
        "willingness_to_pay": "$1000-10000/month",
        "value_drivers": ["security", "customization"]
      }
    ],
    "pricingModels": ["usage_based", "tiered", "hybrid"],
    "optimizeFor": "revenue_and_margin"
  },
  "exit_routing": {
    "strategy_defined": "packaging_optimizer",
    "needs_more_data": "customer_research"
  }
}
```

#### Step 3: Optimize Packaging

```json
{
  "skill": "packaging_optimizer",
  "input": {
    "pricingStrategy": "{{previous.strategy}}",
    "features": "{{product.all_features}}",
    "currentTiers": "{{company.tiers}}",
    "optimizationGoals": {
      "clearValueLadder": true,
      "reduceDecisionParalysis": true,
      "anchorHigherPrice": true,
      "encourageMidTier": true
    },
    "tierCount": "3-4",
    "featureGating": "value_based"
  },
  "exit_routing": {
    "packaging_ready": "price_experimentation",
    "needs_stakeholder_input": "pricing_committee_review"
  }
}
```

#### Step 4: Experiment with Pricing

```json
{
  "skill": "price_experimentation",
  "input": {
    "experimentType": "ab_test",
    "variants": [
      {
        "name": "control",
        "pricing": "{{company.current_pricing}}"
      },
      {
        "name": "variant_a",
        "pricing": "{{previous.optimized_pricing}}"
      },
      {
        "name": "variant_b",
        "pricing": "{{previous.optimized_pricing_aggressive}}"
      }
    ],
    "segments": ["new_customers", "upgrade_candidates"],
    "metrics": ["conversion_rate", "revenue_per_customer", "customer_lifetime_value", "churn_rate"],
    "duration": "30_days",
    "significanceLevel": 0.95
  },
  "exit_routing": {
    "winner_identified": "upgrade_trigger",
    "inconclusive": "extend_experiment"
  }
}
```

#### Step 5: Trigger Upgrades

```json
{
  "skill": "upgrade_trigger",
  "input": {
    "userId": "{{trigger.user_id}}",
    "currentTier": "{{user.plan}}",
    "usageData": "{{consumption_analyzer.data}}",
    "triggerConditions": [
      "approaching_limit",
      "premium_feature_attempt",
      "high_engagement",
      "team_growth"
    ],
    "upgradeIncentives": {
      "discount": "first_month_20_off",
      "trial": "14_day_premium_trial",
      "urgency": "limit_approaching"
    },
    "timing": "optimal_moment"
  },
  "exit_routing": {
    "upgrade_completed": "consumption_analyzer",
    "upgrade_declined": "nurture_sequence"
  }
}
```

#### Step 6: Analyze Consumption

```json
{
  "skill": "consumption_analyzer",
  "input": {
    "userId": "{{chain.user_id}}",
    "pricingModel": "usage_based",
    "usageMetrics": ["api_calls", "storage_gb", "compute_hours", "seats", "transactions"],
    "billingPeriod": "monthly",
    "predictions": {
      "nextMonthUsage": true,
      "overageRisk": true,
      "downgradeLikelihood": true
    },
    "notifications": "proactive"
  },
  "exit_routing": {
    "normal_usage": "invoice_explainer",
    "overage_predicted": "limit_notification",
    "usage_dropping": "engagement_campaign"
  }
}
```

#### Step 7: Explain Invoices

```json
{
  "skill": "invoice_explainer",
  "input": {
    "invoiceId": "{{billing.invoice_id}}",
    "userId": "{{chain.user_id}}",
    "usageData": "{{previous.consumption}}",
    "explanationFormat": {
      "breakdown": true,
      "visualCharts": true,
      "compareToPrevious": true,
      "costDrivers": true,
      "optimizationTips": true
    },
    "deliveryMethod": ["email", "in_app"],
    "allowQuestions": true
  },
  "output": "send_explained_invoice"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/revenue-optimization \
  -H "Content-Type: application/json" \
  -d '{
    "analysisType": "full_pricing_review",
    "includeExperiments": true,
    "segments": ["smb", "enterprise"]
  }'
```

### Expected Output

```json
{
  "status": "success",
  "pricingOptimization": {
    "recommendedStrategy": "hybrid_usage_based",
    "recommendedTiers": 3,
    "expectedRevenueLift": "30%",
    "expectedMarginImprovement": "20%"
  },
  "experiments": {
    "active": 2,
    "completed": 5,
    "winningVariants": ["variant_b_tier_structure", "variant_a_pricing"]
  },
  "consumption": {
    "averageUsage": "850 API calls/month",
    "overageRate": "12%",
    "downgradePredictions": 3
  },
  "invoiceClarity": {
    "disputeRate": "2%",
    "clarityScore": 92,
    "supportTicketsReduced": "60%"
  }
}
```

### Monitoring & Metrics

Track these KPIs:

- **Revenue Per Customer:** Track average and trend
- **Gross Margin:** Target > 75% for SaaS
- **Upgrade Conversion Rate:** Target 15-25%
- **Invoice Dispute Rate:** Target < 3%
- **Pricing Experiment Win Rate:** Track learnings

### Expected Outcomes

- **Week 1:** Pricing analysis complete, experiments launched
- **Month 1:** 15% improvement in upgrade conversion rate
- **Quarter 1:** 30% revenue increase per customer, 20% margin improvement
- **Quarter 2:** $500K+ incremental ARR from optimization

---

## Recipe 29: Partnership Ecosystem Automation

**Use Case:** Automate partner channel management, co-selling, and ecosystem revenue tracking
**Skills:** 6 chained skills
**Time:** Real-time partnership management vs manual quarterly reviews
**ROI:** 40% more partner-sourced pipeline, 25% faster deal cycles, 30% ecosystem revenue growth

### The Chain

```
partner_mapping → nearbound_signal → co_sell_trigger →
deal_registration → partner_influenced_revenue → ecosystem_health
```

### How It Works

1. **partner_mapping** — Identifies and maps potential partner relationships
2. **nearbound_signal** — Detects partnership opportunities through shared connections
3. **co_sell_trigger** — Identifies opportunities for co-selling with partners
4. **deal_registration** — Manages partner deal registration and conflict resolution
5. **partner_influenced_revenue** — Attributes revenue to partner contributions
6. **ecosystem_health** — Tracks overall partnership ecosystem health

### Setup Instructions

#### Step 1: Install Ecosystem Skills

```bash
npx skills-directory install --target all --domain ecosystem
```

#### Step 2: Configure Partner Mapping

```json
{
  "skill": "partner_mapping",
  "trigger": "partner_discovery",
  "input": {
    "partnerTypes": [
      "technology_partners",
      "resellers",
      "implementation_partners",
      "referral_partners",
      "integration_partners"
    ],
    "targetIndustries": "{{company.target_industries}}",
    "geographies": "{{company.target_regions}}",
    "mappingCriteria": {
      "customerOverlap": true,
      "complementaryProducts": true,
      "marketPresence": true,
      "culturalFit": true
    },
    "prioritizationScore": "calculate"
  },
  "exit_routing": {
    "partners_identified": "nearbound_signal",
    "needs_vetting": "partner_evaluation"
  }
}
```

#### Step 3: Detect Nearbound Signals

```json
{
  "skill": "nearbound_signal",
  "input": {
    "partners": "{{previous.mapped_partners}}",
    "accountData": "{{crm.accounts}}",
    "signalTypes": [
      "shared_customers",
      "mutual_connections",
      "simultaneous_engagement",
      "integration_usage",
      "co_marketing_activity"
    ],
    "enrichmentSources": ["linkedin", "crm", "marketing_automation"],
    "signalStrength": "score",
    "autoAlert": "high_quality_signals"
  },
  "exit_routing": {
    "strong_signals": "co_sell_trigger",
    "weak_signals": "nurture_relationship"
  }
}
```

#### Step 4: Trigger Co-Selling

```json
{
  "skill": "co_sell_trigger",
  "input": {
    "opportunityId": "{{crm.opportunity_id}}",
    "nearbound_data": "{{previous.signals}}",
    "partner": "{{previous.recommended_partner}}",
    "coSellCriteria": {
      "accountFit": true,
      "partnerPresence": true,
      "dealSize": "> $50K",
      "closeProbability": "> 30%"
    },
    "introduction": "automated_warm_intro",
    "sharedContext": "opportunity_details",
    "partnerIncentive": "co_sell_credit"
  },
  "exit_routing": {
    "co_sell_initiated": "deal_registration",
    "partner_declined": "try_alternative_partner"
  }
}
```

#### Step 5: Register Partner Deals

```json
{
  "skill": "deal_registration",
  "input": {
    "dealId": "{{chain.opportunity_id}}",
    "partner": "{{chain.partner}}",
    "registrationType": "co_sell",
    "dealDetails": {
      "accountName": "{{opportunity.account}}",
      "estimatedValue": "{{opportunity.amount}}",
      "expectedCloseDate": "{{opportunity.close_date}}",
      "partnerRole": "{{trigger.role}}"
    },
    "conflictCheck": "automatic",
    "approvalWorkflow": "partner_ops",
    "partnerCommission": "calculate"
  },
  "exit_routing": {
    "registered": "partner_influenced_revenue",
    "conflict_detected": "conflict_resolution"
  }
}
```

#### Step 6: Track Partner-Influenced Revenue

```json
{
  "skill": "partner_influenced_revenue",
  "input": {
    "dealId": "{{chain.opportunity_id}}",
    "partner": "{{chain.partner}}",
    "attributionModel": "multi_touch",
    "influenceTypes": [
      "deal_registration",
      "co_sell",
      "referral",
      "integration_usage",
      "co_marketing"
    ],
    "revenueAllocation": {
      "partner_sourced": "100%",
      "partner_influenced": "weighted",
      "partner_assisted": "partial"
    },
    "reportingPeriod": "monthly"
  },
  "exit_routing": {
    "attribution_complete": "ecosystem_health",
    "dispute": "partner_review"
  }
}
```

#### Step 7: Monitor Ecosystem Health

```json
{
  "skill": "ecosystem_health",
  "input": {
    "partners": "{{company.all_partners}}",
    "healthMetrics": {
      "pipelineGenerated": true,
      "revenueInfluenced": true,
      "dealVelocity": true,
      "partnerEngagement": true,
      "nps": true,
      "certifications": true
    },
    "segmentation": "by_tier",
    "benchmarking": "against_targets",
    "alertThresholds": {
      "pipeline_drop": "-20%",
      "engagement_drop": "-30%",
      "nps_below": 30
    }
  },
  "output": "ecosystem_dashboard"
}
```

### Testing the Chain

```bash
curl -X POST http://localhost:3000/api/chains/partnership-automation \
  -H "Content-Type: application/json" \
  -d '{
    "analysisType": "full_ecosystem_health",
    "includeNearbound": true,
    "partnerTiers": ["strategic", "premier", "registered"]
  }'
```

### Expected Output

```json
{
  "status": "success",
  "ecosystemMetrics": {
    "totalPartners": 45,
    "activePartners": 32,
    "partnerSourcedPipeline": "$2.5M",
    "partnerInfluencedRevenue": "$800K",
    "averageDealCycle": "32 days"
  },
  "nearbound": {
    "strongSignals": 12,
    "coSellOpportunities": 8,
    "potentialValue": "$1.2M"
  },
  "dealRegistrations": {
    "registered": 15,
    "approved": 14,
    "conflicts": 1,
    "averageApprovalTime": "4 hours"
  },
  "health": {
    "overallScore": 87,
    "topPerformers": ["Partner A", "Partner B", "Partner C"],
    "atRisk": ["Partner X"]
  }
}
```

### Monitoring & Metrics

Track these KPIs:

- **Partner-Sourced Pipeline:** Target 30-40% of total pipeline
- **Partner-Influenced Revenue:** Track % of closed/won deals
- **Deal Velocity:** Target 25% faster with partner involvement
- **Partner Engagement Score:** Track monthly activity levels
- **Ecosystem ROI:** Calculate partner program costs vs revenue

### Expected Outcomes

- **Week 1:** Partner mapping complete, nearbound signals active
- **Month 1:** 12+ co-sell opportunities identified and initiated
- **Quarter 1:** 40% increase in partner-sourced pipeline, 25% faster deals
- **Quarter 2:** 30% ecosystem revenue growth, $500K+ partner-influenced ARR

---

## Recipe 30: People Ops Talent Intelligence

**Use Case:** Source candidates, assess skill gaps, and align compensation benchmarks
**Skills:** 3 chained skills (People Ops)
**Time:** Hours instead of days per role
**ROI:** Faster hiring, data-driven comp

### The Chain

```
people_candidate_sourcer → people_skill_gap_analyzer →
people_comp_benchmarker
```

### How It Works

1. **candidate_sourcer** — Surfaces and ranks candidates
2. **skill_gap_analyzer** — Maps gaps for role or team
3. **comp_benchmarker** — Benchmarks compensation for offers and reviews

### Setup

Install domain: `npx skills-directory install --target all --domain people_ops`. Run from ATS or HRIS; use output for role profiles and offer letters.

### Expected Outcomes

- **Week 1:** First pipeline run for one role
- **Month 1:** 40% faster time-to-fill for piloted roles
- **Quarter 1:** Comp benchmarks used for all offers

---

## Recipe 31: Data Ops Experimentation Pipeline

**Use Case:** Cohorts, experiment analysis, and funnel optimization in one flow
**Skills:** 3 chained skills (Data Ops)
**Time:** Same-day experiment readouts and funnel insights
**ROI:** 50% faster experiment cycles, consistent funnel metrics

### The Chain

```
data_cohort_builder → data_experiment_analyzer → data_funnel_optimizer
```

### How It Works

1. **cohort_builder** — Builds user cohorts for analysis and experiments
2. **experiment_analyzer** — Analyzes A/B tests and significance
3. **funnel_optimizer** — Optimizes conversion funnels from results

### Setup

Install domain: `npx skills-directory install --target all --domain data_ops`. Connect to your analytics/warehouse; chain output to dashboards or growth team.

### Expected Outcomes

- **Week 1:** One experiment analyzed end-to-end
- **Month 1:** All experiments read via chain
- **Quarter 1:** Funnel optimization driven by chain output

---

These quick-reference recipes show how to adapt existing skills for industry-specific use cases.

---

### Quick Reference: Healthcare/Life Sciences Workflows

```
[Scientific domain skills] → compliance_pii_detector → compliance_data_retention
```

**ROI:** 40% faster research workflows, 60% compliance improvement
**Note:** Uses 141 scientific domain skills for healthcare/clinical research workflows. Requires medical knowledge bases for full implementation.

---

### Quick Reference: FinTech/Banking Compliance

```
arr_waterfall → burn_rate_monitor → compliance_gdpr_manager → compliance_audit_preparer
```

**ROI:** 90% faster financial reporting, 80% compliance accuracy
**Note:** Combines finops and compliance skills for banking/fintech regulatory requirements.

---

## Recipe 32: Partnership Deal Flow

```
partner_mapping → nearbound_signal → co_sell_trigger →
deal_registration → partner_influenced_revenue
```

**ROI:** 25% more partner-sourced pipeline

---

## Recipe 33: Scientific Research Synthesis Pipeline

**Use Case:** Turn literature review into structured hypotheses and research output
**Skills:** 4 chained skills (scientific context)
**Time:** Hours instead of days for literature-to-hypothesis workflows
**ROI:** 40% faster research synthesis, consistent output structure

### The Chain

```
scientific/literature-review → scientific/hypothesis-generation →
scientific/research-lookup → scientific/scientific-writing
```

### How It Works

1. **literature-review** — Synthesizes existing literature and identifies gaps
2. **hypothesis-generation** — Generates testable hypotheses from the review
3. **research-lookup** — Enriches with current data and citations
4. **scientific-writing** — Produces structured research output (papers, reports)

### Setup Instructions

#### Step 1: Install Scientific (Context) Skills

```bash
npx skills-directory install --target all --domain scientific
```

#### Step 2: Configure Literature Review Entry Point

```json
{
  "skill": "scientific/literature-review",
  "input": {
    "topic": "{{research.topic}}",
    "scope": "{{research.scope}}",
    "sources": ["pubmed", "openalex", "biorxiv"]
  },
  "exit_routing": {
    "complete": "scientific/hypothesis-generation",
    "needs_refinement": "scientific/literature-review"
  }
}
```

#### Step 3: Chain to Hypothesis Generation and Beyond

```json
{
  "skill": "scientific/hypothesis-generation",
  "input": {
    "literatureSummary": "{{previous.output}}",
    "researchQuestion": "{{research.question}}"
  },
  "exit_routing": { "hypotheses_ready": "scientific/research-lookup" }
}
```

```json
{
  "skill": "scientific/research-lookup",
  "input": {
    "hypotheses": "{{previous.hypotheses}}",
    "context": "{{previous.output}}"
  },
  "exit_routing": { "enriched": "scientific/scientific-writing" }
}
```

```json
{
  "skill": "scientific/scientific-writing",
  "input": {
    "content": "{{chain.all_previous_outputs}}",
    "format": "paper",
    "venue": "{{research.venue}}"
  },
  "output": "research_output"
}
```

### Expected Outcomes

- **Week 1:** Pipeline runs end-to-end on sample topic
- **Month 1:** 40% faster literature-to-hypothesis cycles
- **Quarter 1:** Reusable for multiple research domains

---

## Recipe 34: Skene Growth Strategy Chain

**Use Case:** From codebase and product to a growth manifest and actionable template
**Skills:** 4 chained skills (Skene)
**Time:** Hours instead of workshops to get a first growth strategy
**ROI:** Clear growth roadmap; PLG and GTM alignment

### The Chain

```
skene_analyze_tech_stack → skene_analyze_growth_hubs →
skene_generate_growth_manifest → skene_generate_growth_template
```

### How It Works

1. **analyze_tech_stack** — Detects framework, language, database, auth, deployment
2. **analyze_growth_hubs** — Identifies viral, onboarding, monetization potential
3. **generate_growth_manifest** — Combines tech + growth gaps into a manifest
4. **generate_growth_template** — Produces actionable PLG growth recommendations

### Setup Instructions

#### Step 1: Install Skene Skills

```bash
npx skills-directory install --target all --domain skene
```

#### Step 2: Configure the Chain

```json
{
  "skill": "skene_analyze_tech_stack",
  "input": {
    "repoPath": "{{project.path}}",
    "includeDocs": true
  },
  "exit_routing": { "success": "skene_analyze_growth_hubs" }
}
```

```json
{
  "skill": "skene_analyze_growth_hubs",
  "input": {
    "techStack": "{{previous.output}}",
    "productContext": "{{product.overview}}"
  },
  "exit_routing": { "success": "skene_generate_growth_manifest" }
}
```

```json
{
  "skill": "skene_generate_growth_manifest",
  "input": {
    "techStack": "{{chain.step_1.output}}",
    "growthHubs": "{{previous.output}}"
  },
  "exit_routing": { "success": "skene_generate_growth_template" }
}
```

```json
{
  "skill": "skene_generate_growth_template",
  "input": {
    "manifest": "{{previous.output}}",
    "priorities": "{{company.growth_priorities}}"
  },
  "output": "growth_template"
}
```

### Expected Outcomes

- **Week 1:** First manifest and template from your repo
- **Month 1:** Strategy doc used for PLG/GTM planning
- **Quarter 1:** Updated quarterly with new analyses

---

## Recipe 35: Community Advocacy Pipeline

**Use Case:** Identify champions, find case study candidates, and feed ambassador program
**Skills:** 3 chained skills (Community)
**Time:** Ongoing; replaces manual hunting
**ROI:** 2x more case studies, faster ambassador recruitment

### The Chain

```
community_champion_identifier → community_case_study_finder →
community_ambassador_program
```

### How It Works

1. **champion_identifier** — Finds power users and advocates
2. **case_study_finder** — Identifies strong case study candidates
3. **ambassador_program** — Manages ambassador pipeline and engagement

### Setup

Install domain: `npx skills-directory install --target all --domain community`. Wire product/usage data into step 1; route high-fit champions to case study and ambassador steps.

### Expected Outcomes

- **Week 1:** Champion list and case study shortlist
- **Month 1:** 2+ new case studies in progress
- **Quarter 1:** Ambassador pipeline 2x

---

## Recipe 36: FinOps Standalone Dashboard

**Use Case:** Burn rate, scenarios, and investor-ready metrics without touching sales/CS chains
**Skills:** 3 chained skills (FinOps)
**Time:** Real-time vs manual board prep
**ROI:** 90% faster financial reporting, single source of truth

### The Chain

```
finops_burn_rate_monitor → finops_scenario_planner → finops_investor_metrics
```

### How It Works

1. **burn_rate_monitor** — Tracks cash burn and runway
2. **scenario_planner** — Models scenarios (e.g. growth, cuts)
3. **investor_metrics** — Produces investor-ready KPIs and visuals

### Setup

Install domain: `npx skills-directory install --target all --domain finops`. Configure with your financial data source; chain outputs to your dashboard or board deck.

### Expected Outcomes

- **Week 1:** Dashboard live with burn and scenarios
- **Month 1:** Board prep time cut by 80%+
- **Quarter 1:** Investor updates automated

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
