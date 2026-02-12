# Recipe Audit: Skill Chains Coverage

**Date:** 2026-02-12  
**Purpose:** Map existing recipes to domains and identify under-served domains for new skill chains.

## Existing 36 Recipes (Domain + Skill IDs)

(28 original + 8 new: 29 Scientific, 30 Superpowers, 31 Skene, 32 AI Ops, 33 FinOps, 34 Community, 35 People Ops, 36 Data Ops.)

| #   | Recipe                              | Primary domain           | Example skills in chain                                                                                                                  |
| --- | ----------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Sales Deal Qualification Pipeline   | revops                   | lead_qualification, opportunity_scoring, deal_inspection, next_best_action, content_recommender                                          |
| 2   | Customer Churn Prevention Pipeline  | customer_success         | health_scoring, churn_prediction, risk_mitigation_playbook, escalation_manager                                                           |
| 3   | Financial Intelligence Dashboard    | finops                   | burn_rate_monitor, arr_waterfall, scenario_planner, investor_metrics                                                                     |
| 4   | Growth Optimization Engine          | plg / marketing          | ab_test_setup, experiment_analyzer, funnel_optimizer, analytics_tracking                                                                 |
| 5   | Content Marketing Automation        | marketing                | content_research_writer, copywriting, social_content, schema_markup                                                                      |
| 11  | Freemium Conversion Optimization    | plg / monetization       | trial_extension_evaluator, paywall_upgrade_cro, activation_metrics                                                                       |
| 12  | Usage-Based Pricing Engine          | monetization             | usage_metering, overage_predictor, limit_notification, pricing_optimization                                                              |
| 13  | Product-Led Sales Handoff           | plg / revops             | pql_scoring, lead_qualification, handoff_orchestration                                                                                   |
| 14  | AI Support Deflection System        | support_ops / ai_ops     | ticket_triage, intent_classifier, response_suggester, kb_gap_finder                                                                      |
| 15  | Developer Experience Onboarding     | devex                    | api_onboarding, sandbox_manager, code_sample_generator                                                                                   |
| 16  | Employee Onboarding Automation      | people_ops               | onboarding_checklist, pulse_analyzer, perf_review_generator                                                                              |
| 17  | Data Quality Automation             | data_ops                 | data_anomaly_alerter, data_event_validator, data_cohort_builder, data_funnel_optimizer, data_experiment_analyzer, data_dashboard_builder |
| 18  | Community-Led Growth Engine         | community                | champion_identifier, case_study_finder, content_curator, event_manager                                                                   |
| 19  | Multi-Platform Content Distribution | marketing                | content_research_writer, social_content, social_content_generator                                                                        |
| 20  | Product Experimentation Engine      | product_ops              | experimentation, experiment_analyzer, feature_adoption                                                                                   |
| 21  | API Lifecycle Management            | devex                    | changelog_tracker, deprecation_notifier, migration_assistant                                                                             |
| 22  | Competitive Intelligence Automation | revops / marketing       | competitive_intel, competitive_ads_extractor, competitor_alternatives                                                                    |
| 23  | Brand Consistency Engine            | marketing / anthropic    | brand-guidelines, copy_editing, humanization_engine                                                                                      |
| 24  | Customer Education Platform         | plg / customer_success   | onboarding_flow, milestone_celebration, contextual_help                                                                                  |
| 25  | Security Code Review Automation     | security                 | semgrep-rule-creator, entry-point-analyzer, variant-analysis, differential-review, fix-review, property-based-testing                    |
| 26  | Compliance Automation Hub           | compliance               | gdpr_manager, pii_detector, audit_preparer, data_retention                                                                               |
| 27  | E-commerce Revenue Optimization     | monetization / marketing | pricing_optimization, consumption_analyzer, discount_optimizer                                                                           |
| 28  | Partnership Ecosystem Automation    | ecosystem                | partner_mapping, co_sell_trigger, deal_registration, referral_program                                                                    |

## Under-Served Domains (executable skills, no or minimal recipe)

| Domain             | Executable skills               | Has recipe?         | Notes                                                                                                                   |
| ------------------ | ------------------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| scientific         | 141 (context) / some executable | No                  | Literature, hypothesis, protocols; data pipelines. Add research/lab chain.                                              |
| superpowers        | 14                              | No                  | brainstorming → writing-plans → executing-plans → verification. Add dev workflow chain.                                 |
| skene / meta       | 6 + 6                           | No                  | analyze_tech_stack → analyze_growth_hubs → generate_growth_manifest → generate_growth_template. Add PLG strategy chain. |
| ai_ops             | 19                              | Partial (Recipe 14) | Dedicated AI Ops chain: ticket_classifier → response_suggester → summarization or intent → chatbot_orchestrator.        |
| anthropic_official | 16                              | Partial (Recipe 23) | Doc/deck chain: docx + pptx + brand-guidelines.                                                                         |

Domains already covered by at least one recipe: revops, customer_success, finops, plg, marketing, monetization, support_ops, devex, people_ops, data_ops, community, product_ops, security, compliance, ecosystem.

## Recommendations

- **Batch 1 (new recipes):** Scientific (research/literature pipeline), Superpowers (plan → execute → verify), Skene/Meta (tech stack → growth hubs → manifest → template). Security already has Recipe 25.
- **Batch 2 (new recipes):** Community (second recipe optional), People Ops (second optional), Data Ops (second optional), AI Ops (dedicated chain), FinOps standalone (e.g. burn_rate → scenario_planner → investor_metrics).
- **Recipe index:** Add domain tags to Quick Navigation in SKILL_CHAINS.md for filter-by-domain discovery.
