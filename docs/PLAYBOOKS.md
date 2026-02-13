# Niche playbooks

Each workflow blueprint in the cookbook is a **niche-specific playbook**: it has an **ICP** (Ideal Customer Profile), an **integration reference** (exact data to wire from Salesforce, HubSpot, Stripe, etc.), and **opinionated prompts** per step so the chain is tuned for that profile.

## Recipe-to-blueprint mapping

See [registry/recipe_blueprint_index.json](../registry/recipe_blueprint_index.json) for the full mapping of recipe numbers (1–36) to blueprint ids and integration refs.

## All blueprints

| Blueprint                              | YAML                                                                                                    | ICP (summary)                            | Integration refs      | Opinionated prompts                                |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------- | --------------------- | -------------------------------------------------- |
| workflow_sales_automated               | [sales_workflow.yaml](../registry/blueprints/sales_workflow.yaml)                                       | B2B SaaS sales-led $2–10M ARR, 3–10 reps | Salesforce, HubSpot   | MEDDIC, Champion/Economic Buyer, next-best action  |
| workflow_customer_churn_prevention     | [customer_churn_prevention.yaml](../registry/blueprints/customer_churn_prevention.yaml)                 | B2B SaaS post–PMF, CS 1–5                | Salesforce (optional) | Usage + support sentiment, at-risk before renewal  |
| workflow_customer_success_automated    | [customer_success_workflow.yaml](../registry/blueprints/customer_success_workflow.yaml)                 | B2B SaaS CS, 1–10 CSMs                   | Salesforce            | Health score, churn risk, intervention playbooks   |
| workflow_marketing_automated           | [marketing_workflow.yaml](../registry/blueprints/marketing_workflow.yaml)                               | B2B SaaS growth, content-led             | None                  | Keyword research, content, SEO, distribution       |
| workflow_data_automated                | [data_workflow.yaml](../registry/blueprints/data_workflow.yaml)                                         | Data team, analytics and pipelines       | None                  | Extract/transform/analyze/visualize guidance       |
| workflow_engineering_automated         | [engineering_workflow.yaml](../registry/blueprints/engineering_workflow.yaml)                           | Engineering, velocity and quality        | None                  | Code review, tests, security scan, deploy          |
| workflow_finops_standalone             | [finops_standalone_dashboard.yaml](../registry/blueprints/finops_standalone_dashboard.yaml)             | Finance/ops, board and investor          | Stripe                | Burn, runway, scenario, investor metrics           |
| workflow_partner_onboarding_revenue    | [example_workflow.yaml](../registry/blueprints/example_workflow.yaml)                                   | Ecosystem/partner, partner-led growth    | Salesforce (optional) | Onboard, integration health, revenue attribution   |
| workflow_ai_ops_conversation           | [ai_ops_conversation_pipeline.yaml](../registry/blueprints/ai_ops_conversation_pipeline.yaml)           | Support and AI Ops                       | None                  | Triage, intent, response suggest, summarization    |
| workflow_community_advocacy            | [community_advocacy_pipeline.yaml](../registry/blueprints/community_advocacy_pipeline.yaml)             | Community and advocacy                   | None                  | Champion ID, case study finder, ambassador program |
| workflow_data_ops_experimentation      | [data_ops_experimentation_pipeline.yaml](../registry/blueprints/data_ops_experimentation_pipeline.yaml) | Data and growth ops                      | None                  | Cohorts, experiment analysis, funnel optimization  |
| workflow_people_ops_talent             | [people_ops_talent_intelligence.yaml](../registry/blueprints/people_ops_talent_intelligence.yaml)       | People ops, talent and comp              | None                  | Sourcing, skill gaps, comp benchmarks              |
| workflow_scientific_research_synthesis | [scientific_research_synthesis.yaml](../registry/blueprints/scientific_research_synthesis.yaml)         | Research and R&D                         | None                  | Literature, hypothesis, research lookup, writing   |
| workflow_skene_growth_strategy         | [skene_growth_strategy.yaml](../registry/blueprints/skene_growth_strategy.yaml)                         | PLG and growth strategy                  | None                  | Tech stack, growth hubs, manifest, template        |
| workflow_superpowers_development       | [superpowers_development_workflow.yaml](../registry/blueprints/superpowers_development_workflow.yaml)   | Structured development                   | None                  | Brainstorm, plan, execute, verify                  |

## Where opinionated prompts live

Opinionated prompts are stored **in each blueprint YAML** under `chain_sequence[].opinionated_prompts` with optional `system_context` (string) and `input_guidance` (object). At runtime, merge these with the skill’s default instructions for the chosen ICP.

## Exact data to wire (integration reference schemas)

| Schema                                                                                                               | System     | Use for chains                                                 |
| -------------------------------------------------------------------------------------------------------------------- | ---------- | -------------------------------------------------------------- |
| [salesforce_lead_qualification_chain.json](../registry/integration_schemas/salesforce_lead_qualification_chain.json) | Salesforce | Lead/Opportunity/Contact/Account for sales and churn chains    |
| [hubspot_events_lead_scoring.json](../registry/integration_schemas/hubspot_events_lead_scoring.json)                 | HubSpot    | Engagement events and properties for lead scoring              |
| [stripe_usage_expansion.json](../registry/integration_schemas/stripe_usage_expansion.json)                           | Stripe     | Subscription, usage, invoice for FinOps and usage-based chains |

See [registry/integration_schemas/README.md](../registry/integration_schemas/README.md) for format and usage in blueprints.
