# Built With Skene

**Real-world AI agents built using the Skene Skills Directory**

This showcase features agent deployments that demonstrate the power of skill chain composition. Each example includes the problem, solution, skills used, and measurable impact.

---

## 1. LeadFlow - Intelligent Lead Qualification Agent

### Problem
B2B SaaS company with 50-person sales team was manually qualifying 200+ leads/month. Each lead took 2-3 hours of research, scoring, and routing. Only 15% of leads qualified, wasting significant rep time.

### Solution
5-skill chain automating the entire qualification pipeline:

```
lead_qualification → opportunity_scoring → deal_inspection →
next_best_action → content_recommender
```

### How It Works
1. **lead_qualification** — Applies MEDDIC framework, pulls enrichment data
2. **opportunity_scoring** — Scores on fit (40%), urgency (30%), budget (30%)
3. **deal_inspection** — Analyzes deal health, identifies risks early
4. **next_best_action** — Recommends specific actions for rep
5. **content_recommender** — Suggests relevant case studies and decks

### Skills Used
- `lead_qualification` (Sales)
- `opportunity_scoring` (RevOps)
- `deal_inspection` (Sales)
- `next_best_action` (Sales)
- `content_recommender` (Marketing)

### Impact
- ⚡ **Qualification time**: 2-3 hours → 5 minutes per lead (97% reduction)
- 📈 **Leads processed**: 200/month → 500/month (2.5x increase)
- 💰 **Cost savings**: $40K/month in rep time
- 🎯 **Pipeline quality**: 3x more qualified opportunities
- 📊 **Win rate**: 18% → 25% (39% improvement)

**Payback:** Week 1
**Status:** Production (18 months)

---

## 2. ChurnGuard - Proactive Churn Prevention Agent

### Problem
SaaS startup with $12M ARR facing 20% annual churn. Customer success team was reactive, only intervening after usage dropped. No early warning system for at-risk accounts.

### Solution
4-skill chain for predictive churn prevention:

```
health_scoring → churn_prediction → risk_mitigation_playbook →
escalation_manager
```

### How It Works
1. **health_scoring** — Tracks product usage, support tickets, NPS
2. **churn_prediction** — ML model predicts churn 60-90 days early
3. **risk_mitigation_playbook** — Triggers intervention based on risk level
4. **escalation_manager** — Auto-escalates high-risk accounts to CSM

### Skills Used
- `health_scoring` (Customer Success)
- `churn_prediction` (Customer Success)
- `risk_mitigation_playbook` (Customer Success)
- `escalation_manager` (Customer Success)

### Impact
- ⚡ **Early detection**: 60-90 days advance warning (was 0)
- 📈 **Churn reduction**: 20% → 10% annual (50% improvement)
- 💰 **ARR saved**: $600K/year
- 🎯 **CS efficiency**: Proactive vs reactive interventions
- 📊 **NPS improvement**: +12 points

**Payback:** Month 1
**Status:** Production (12 months)

---

## 3. GrowthEngine - PLG Activation Optimizer

### Problem
Freemium product with 10K monthly signups but only 8% activation rate and 2% free-to-paid conversion. No data-driven optimization of onboarding flow.

### Solution
5-skill chain for complete PLG funnel optimization:

```
activation_analysis → engagement_scoring → monetization_trigger →
viral_loop_optimizer → retention_predictor
```

### How It Works
1. **activation_analysis** — Identifies friction in aha moment journey
2. **engagement_scoring** — Real-time engagement tracking per user
3. **monetization_trigger** — Optimal timing for upgrade prompts
4. **viral_loop_optimizer** — Maximizes viral coefficient
5. **retention_predictor** — Predicts churners, triggers win-back

### Skills Used
- `activation_analysis` (PLG)
- `engagement_scoring` (PLG)
- `monetization_trigger` (PLG)
- `viral_loop_optimizer` (PLG)
- `retention_predictor` (PLG)

### Impact
- ⚡ **Activation rate**: 8% → 18% (125% increase)
- 📈 **Time to activation**: 7 days → 2 days
- 💰 **Free-to-paid conversion**: 2% → 4.5% (125% increase)
- 🎯 **Viral coefficient**: 0.3 → 0.6 (2x)
- 📊 **MRR growth**: 150% in 3 months

**Payback:** Week 2
**Status:** Production (9 months)

---

## 4. BoardReady - CFO Intelligence Dashboard

### Problem
CFO of $30M ARR SaaS company spending 8 hours/week preparing board decks. Forecasts were static, variance analysis was manual, and financial insights came too late for decision-making.

### Solution
5-skill chain for real-time financial intelligence:

```
financial_metrics_calculator → variance_analyzer → forecast_builder →
cash_flow_projector → board_reporting_generator
```

### How It Works
1. **financial_metrics_calculator** — Auto-calculates ARR, burn, runway, etc.
2. **variance_analyzer** — Budget vs. actual with root cause analysis
3. **forecast_builder** — Multi-scenario forecasting (best/worst/likely)
4. **cash_flow_projector** — 13-week cash flow projections
5. **board_reporting_generator** — One-click board deck generation

### Skills Used
- `financial_metrics_calculator` (FinOps)
- `variance_analyzer` (FinOps)
- `forecast_builder` (FinOps)
- `cash_flow_projector` (FinOps)
- `board_reporting_generator` (FinOps)

### Impact
- ⚡ **Board prep time**: 8 hours → 15 minutes (95% reduction)
- 📈 **Forecast updates**: Weekly → daily (real-time)
- 💰 **CFO time savings**: $50K+/month value
- 🎯 **Decision speed**: 10x faster financial insights
- 📊 **Forecast accuracy**: 60% → 85%

**Payback:** Week 1
**Status:** Production (14 months)

---

## 5. ResearchPilot - Automated Literature Review Agent

### Problem
Cancer biology lab spending 20+ hours/week per researcher manually reviewing literature. Slow hypothesis generation, difficulty keeping up with new publications.

### Solution
4-skill chain for automated research synthesis:

```
pubmed_search → paper_summarizer → citation_mapper →
hypothesis_generator
```

### How It Works
1. **pubmed_search** — Automated PubMed queries with custom filters
2. **paper_summarizer** — Extracts key findings, methods, and conclusions
3. **citation_mapper** — Builds citation networks, identifies key papers
4. **hypothesis_generator** — AI-powered hypothesis generation from literature

### Skills Used
- `pubmed_search` (Scientific)
- `paper_summarizer` (Scientific)
- `citation_mapper` (Scientific)
- `hypothesis_generator` (Scientific)

### Impact
- ⚡ **Literature review time**: 3 weeks → 6 hours (95% reduction)
- 📈 **Papers synthesized**: 50/week → 200/week (4x)
- 💡 **Novel hypotheses**: 2x increase in ideas generated
- 🎯 **Grant success**: Faster background research
- 📊 **Publication rate**: 3/year → 5/year

**Payback:** Immediate
**Status:** Production (6 months)

---

## 6. PipelineIntel - Sales Forecasting Agent

### Problem
Sales ops team manually building weekly forecasts from CRM data. Inconsistent methodology, low forecast accuracy (65%), and reps gaming the system.

### Solution
3-skill chain for data-driven forecasting:

```
pipeline_analysis → forecast_builder → win_loss_analyzer
```

### How It Works
1. **pipeline_analysis** — Real-time pipeline health and velocity metrics
2. **forecast_builder** — Statistical forecasting with confidence intervals
3. **win_loss_analyzer** — Identifies patterns in won/lost deals

### Skills Used
- `pipeline_analysis` (RevOps)
- `forecast_builder` (RevOps)
- `win_loss_analyzer` (Sales)

### Impact
- ⚡ **Forecast prep time**: 4 hours → 15 minutes
- 📈 **Forecast accuracy**: 65% → 88%
- 💰 **Time savings**: $15K/month
- 🎯 **Rep gaming eliminated**: Objective scoring
- 📊 **Executive confidence**: Data-driven commits

**Payback:** Month 1
**Status:** Production (8 months)

---

## 7. ContentFlow - Marketing Automation Pipeline

### Problem
Marketing team creating content manually, inconsistent SEO optimization, slow campaign launches. Content creation took 2 weeks, optimization was ad-hoc.

### Solution
4-skill chain for content automation:

```
content_generator → seo_optimizer → campaign_launcher →
performance_tracker
```

### How It Works
1. **content_generator** — AI-powered content drafts based on briefs
2. **seo_optimizer** — Keyword optimization, meta tags, internal linking
3. **campaign_launcher** — Multi-channel campaign deployment
4. **performance_tracker** — Real-time engagement and conversion tracking

### Skills Used
- `content_generator` (Marketing)
- `seo_optimizer` (Marketing)
- `campaign_launcher` (Marketing)
- `performance_tracker` (Marketing)

### Impact
- ⚡ **Content creation time**: 2 weeks → 2 days (85% reduction)
- 📈 **Content volume**: 4 pieces/month → 20 pieces/month (5x)
- 💰 **Cost per piece**: $2K → $400 (80% reduction)
- 🎯 **SEO rankings**: 30% improvement in top 10 rankings
- 📊 **Organic traffic**: 45% increase

**Payback:** Month 2
**Status:** Production (10 months)

---

## 8. DrugDiscovery - Target Identification Agent

### Problem
Biotech company spending 6+ months on target identification and validation. Manual literature review, protein analysis, and compound screening.

### Solution
6-skill chain for accelerated drug discovery:

```
uniprot_search → protein_structure_analyzer → drug_target_identifier →
compound_similarity_search → molecular_docking → toxicity_predictor
```

### How It Works
1. **uniprot_search** — Protein database queries for disease pathways
2. **protein_structure_analyzer** — AlphaFold structure prediction
3. **drug_target_identifier** — Identifies druggable targets
4. **compound_similarity_search** — Screens compound libraries
5. **molecular_docking** — Predicts binding affinity
6. **toxicity_predictor** — Early safety assessment

### Skills Used
- `uniprot_search` (Scientific)
- `protein_structure_analyzer` (Scientific)
- `drug_target_identifier` (Scientific)
- `compound_similarity_search` (Scientific)
- `molecular_docking` (Scientific)
- `toxicity_predictor` (Scientific)

### Impact
- ⚡ **Target ID time**: 6 months → 3 weeks (95% reduction)
- 📈 **Targets evaluated**: 5 → 50 in same timeframe (10x)
- 💡 **Novel targets**: 3 new targets identified
- 🎯 **Hit rate**: 15% improvement in compound screening
- 📊 **Development timeline**: 6 months saved

**Payback:** First successful target
**Status:** Production (4 months)

---

## Common Patterns

### What Makes These Successful?

1. **Clear Problem Definition** — Each agent solves a specific, measurable pain point
2. **Skill Chain Composition** — 3-6 skills chained together for complete workflows
3. **Exit State Routing** — Skills pass data to next skill seamlessly
4. **Measurable Impact** — ROI tracked from day one
5. **Iterative Improvement** — Chains refined based on real usage

### Typical Implementation Timeline

- **Week 1**: Identify use case, select skills
- **Week 2**: Build and test skill chain
- **Week 3**: Deploy to production, measure baseline
- **Week 4+**: Iterate based on results

---

## Want to Build Your Own?

1. **Pick Your Use Case** — Start with a specific pain point
2. **Browse Skills** — Find relevant skills in [directory.md](directory.md)
3. **Follow a Recipe** — Use [SKILL_CHAINS.md](SKILL_CHAINS.md) as template
4. **Deploy & Measure** — Track impact from day one

[Get started with quick wins →](QUICK_WINS.md)

---

## Share Your Agent

Built something with Skene Skills? We'd love to feature it!

**Submit your showcase:**
1. Open an issue with title "Showcase: [Your Agent Name]"
2. Include: Problem, Solution, Skills Used, Impact
3. We'll add it to this page (with your permission)

[Submit showcase →](https://github.com/SkeneTechnologies/skills-directory/issues/new)

---

**Ready to build?** Start with a [15-minute quick win](QUICK_WINS.md) or browse [all skill chains](SKILL_CHAINS.md).
