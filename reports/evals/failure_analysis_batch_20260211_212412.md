# Evaluation Failure Analysis

**Generated**: 2026-02-11 21:24:18

## Summary Statistics

- **Total Failures**: 16

### Failures by Category

| Category | Count | Percentage |
|----------|-------|------------|
| unknown | 14 | 87.5% |
| skill_not_found | 2 | 12.5% |

### Failures by Domain

| Domain | Count |
|--------|-------|
| customer_success | 7 |
| ai_ops | 5 |
| product_ops | 4 |

## Action Plan (Prioritized)

### 1. Unknown

**Priority**: 1/5 | **Effort**: Medium | **Affected Skills**: 14

**Fix**: Manual investigation required

**Domains**: ai_ops, customer_success, product_ops

**Skills**: cs_health_scoring, cs_expansion_playbook, cs_churn_prediction, cs_nps_followup, cs_renewal_orchestration, cs_value_realization, ai_conversation_intelligence, ai_personalization_engine, ai_autonomous_outreach, ai_predictive_lead_scoring (and 4 more)

### 2. Skill Not Found

**Priority**: 5/5 | **Effort**: Low | **Affected Skills**: 2

**Fix**: Verify skill directory structure and skill.json exists

**Domains**: ai_ops, customer_success

**Skills**: customer_success/feedback_collection, ai_ops/prompt-engineering


## Detailed Failure List

| Skill ID | Domain | Category | Error (first 50 chars) |
|----------|--------|----------|------------------------|
| cs_health_scoring | customer_success | unknown | No metrics collected |
| cs_expansion_playbook | customer_success | unknown | No metrics collected |
| customer_success/feedback_collection | customer_success | skill_not_found | Skill not found: customer_success/feedback_collect |
| cs_churn_prediction | customer_success | unknown | No metrics collected |
| ai_ops/prompt-engineering | ai_ops | skill_not_found | Skill not found: ai_ops/prompt-engineering |
| cs_nps_followup | customer_success | unknown | No metrics collected |
| cs_renewal_orchestration | customer_success | unknown | No metrics collected |
| cs_value_realization | customer_success | unknown | No metrics collected |
| ai_conversation_intelligence | ai_ops | unknown | No metrics collected |
| ai_personalization_engine | ai_ops | unknown | No metrics collected |
| ai_autonomous_outreach | ai_ops | unknown | No metrics collected |
| ai_predictive_lead_scoring | ai_ops | unknown | No metrics collected |
| prodops_feedback_synthesis | product_ops | unknown | No metrics collected |
| prodops_feature_adoption | product_ops | unknown | No metrics collected |
| prodops_voc_aggregation | product_ops | unknown | No metrics collected |
| prodops_roadmap_alignment | product_ops | unknown | No metrics collected |
