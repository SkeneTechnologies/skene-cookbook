# Security Analysis Report

**Total Skills Analyzed:** 765

## Risk Distribution

- **Critical:** 432 (56.5%)
- **High:** 49 (6.4%)
- **Medium:** 49 (6.4%)
- **Low:** 235 (30.7%)

## Critical Risk Skills

### elg_mdf_tracker
- **Risk Factors:** payment, system, get, email, alert, message, analytics, track, log, list, format, calculate, show, view
- **Human-in-loop:** True

### elg_integration_health
- **Risk Factors:** credential, system, change, fetch, get, notification, alert, message, analytics, track, log, monitor, list, sort, format, calculate
- **Human-in-loop:** True

### elg_co_sell_trigger
- **Risk Factors:** execute, system, update, track, list, format, risky_tool: partner.co_sell_update
- **Human-in-loop:** True

### elg_partner_influenced_revenue
- **Risk Factors:** system, update, change, fetch, get, analytics, track, log, sort, format, calculate, aggregate, show, view, risky_tool: crm.update_deal
- **Human-in-loop:** True

### elg_eql_scoring
- **Risk Factors:** system, track, list, format, calculate
- **Human-in-loop:** True

### elg_deal_registration
- **Risk Factors:** system, update, authorize, personal, read, get, email, notification, alert, message, track, log, monitor, list, format, calculate, view
- **Human-in-loop:** True

### elg_partner_tier_manager
- **Risk Factors:** eval, system, update, change, access, fetch, get, email, notification, track, log, list, sort, format, calculate, view, risky_tool: partner.update_tier
- **Human-in-loop:** True

### elg_referral_program
- **Risk Factors:** payment, eval, system, update, get, email, analytics, track, log, list, format, calculate, view, preview
- **Human-in-loop:** True

### elg_ecosystem_intelligence
- **Risk Factors:** system, change, access, get, analytics, log, monitor, sort, format, calculate, aggregate, view
- **Human-in-loop:** True

### elg_nearbound_signal
- **Risk Factors:** system, update, fetch, get, query, email, alert, track, log, monitor, list, filter, format, calculate, risky_tool: crm.update_deal
- **Human-in-loop:** True

### elg_channel_enablement
- **Risk Factors:** system, update, access, permission, sensitive, read, fetch, get, email, analytics, track, list, filter, format, calculate, view, risky_tool: partner.update_certification
- **Human-in-loop:** True

### elg_marketplace_integration
- **Risk Factors:** system, change, get, track, monitor, list, format, view
- **Human-in-loop:** True

### elg_partner_mapping
- **Risk Factors:** system, update, get, log, list, format
- **Human-in-loop:** True

### elg_joint_marketing
- **Risk Factors:** execute, system, write, read, get, email, analytics, track, list, format, calculate, view
- **Human-in-loop:** True

### elg_tech_partner_finder
- **Risk Factors:** eval, system, permission, read, get, email, alert, analytics, log, list, search, filter, sort, format, calculate, view
- **Human-in-loop:** True

### elg_marketplace_listing_optimizer
- **Risk Factors:** system, write, update, change, fetch, get, analytics, track, monitor, list, search, sort, format, show, view, risky_tool: marketplace.update_listing
- **Human-in-loop:** True

### prodops_accessibility_auditor
- **Risk Factors:** system, update, change, access, read, get, track, log, list, format, calculate, view
- **Human-in-loop:** True

### prodops_user_interview_synthesizer
- **Risk Factors:** eval, read, query, log, list, search, format, calculate, view
- **Human-in-loop:** True

### prodops_beta_program_manager
- **Risk Factors:** drop, update, access, read, get, email, analytics, track, monitor, list, filter, format, view
- **Human-in-loop:** True

### prodops_api_deprecation
- **Risk Factors:** remove, api_key, execute, update, change, read, get, email, analytics, track, log, monitor, list, format, calculate, view
- **Human-in-loop:** True

### prodops_incident_analyzer
- **Risk Factors:** system, change, sensitive, read, get, query, alert, message, track, log, monitor, list, search, filter, format, view
- **Human-in-loop:** True

### prodops_roadmap_alignment
- **Risk Factors:** remove, update, list, format, view
- **Human-in-loop:** True

### prodops_release_notes_generator
- **Risk Factors:** remove, update, change, get, message, log, list, format
- **Human-in-loop:** True

### prodops_prioritization_engine
- **Risk Factors:** remove, update, get, analytics, log, list, search, filter, sort, format, calculate, view, risky_tool: linear.update_issue
- **Human-in-loop:** True

### prodops_performance_budget
- **Risk Factors:** remove, change, get, alert, message, analytics, track, monitor, list, format, view
- **Human-in-loop:** True

### prodops_competitive_feature_tracker
- **Risk Factors:** eval, system, update, change, alter, access, get, alert, message, track, log, monitor, list, filter, format, view
- **Human-in-loop:** True

### devex_changelog_tracker
- **Risk Factors:** remove, update, change, fetch, get, email, notification, alert, analytics, track, log, list, filter, sort, format, view, preview
- **Human-in-loop:** True

### devex_integration_health
- **Risk Factors:** credential, update, webhook, get, notification, alert, analytics, track, log, monitor, list, sort, format, calculate, view
- **Human-in-loop:** True

### devex_oauth_helper
- **Risk Factors:** secret, credential, command, change, access, authenticate, authorize, permission, read, get, track, log, list, format, display, view
- **Human-in-loop:** True

### devex_deprecation_notifier
- **Risk Factors:** remove, execute, update, read, get, notification, analytics, track, monitor, list, filter, format
- **Human-in-loop:** True

### devex_sdk_version_monitor
- **Risk Factors:** system, update, change, get, email, notification, alert, analytics, track, log, monitor, list, format, calculate
- **Human-in-loop:** True

### devex_code_sample_generator
- **Risk Factors:** secret, api_key, execute, command, update, change, read, fetch, get, message, track, log, list, format, risky_tool: code.execute_sandbox
- **Human-in-loop:** True

### devex_webhook_tester
- **Risk Factors:** secret, credential, update, authorize, webhook, get, alert, track, log, list, format, show, view
- **Human-in-loop:** True

### devex_migration_assistant
- **Risk Factors:** remove, command, update, change, personal, webhook, get, retrieve, track, log, list, format, view
- **Human-in-loop:** True

### devex_error_explainer
- **Risk Factors:** credential, update, authorize, permission, sensitive, read, get, retrieve, query, message, analytics, track, list, search, filter, format, show, view
- **Human-in-loop:** True

### devex_sandbox_manager
- **Risk Factors:** delete, remove, payment, password, credential, api_key, system, pii, webhook, get, email, analytics, track, log, list, format, show
- **Human-in-loop:** True

### devex_api_onboarding
- **Risk Factors:** credential, command, update, change, authorize, personal, fetch, get, query, analytics, track, list, filter, format, show, view
- **Human-in-loop:** True

### support_proactive_outreach
- **Risk Factors:** drop, update, personal, confidential, read, get, email, alert, message, analytics, track, list, filter, format, view
- **Human-in-loop:** True

### support_sla_monitor
- **Risk Factors:** financial, update, change, read, get, retrieve, alert, message, analytics, log, monitor, list, filter, format, calculate
- **Human-in-loop:** True

### support_queue_balancer
- **Risk Factors:** execute, update, change, get, notification, message, analytics, log, monitor, list, format, calculate
- **Human-in-loop:** True

### support_macros_optimizer
- **Risk Factors:** delete, remove, eval, system, write, update, change, alter, personal, get, retrieve, analytics, monitor, format, view, risky_tool: support.update_macro
- **Human-in-loop:** True

### support_first_response
- **Risk Factors:** eval, update, personal, sensitive, read, get, retrieve, query, list, search, filter, format, summarize, show, view
- **Human-in-loop:** True

### support_sentiment_tracker
- **Risk Factors:** drop, eval, system, update, change, personal, read, get, retrieve, alert, message, analytics, track, monitor, sort, format, calculate, view, risky_tool: crm.update_health_score
- **Human-in-loop:** True

### support_ticket_triage
- **Risk Factors:** payment, access, get, email, analytics, track, log, list, format, calculate, view
- **Human-in-loop:** True

### support_escalation_predictor
- **Risk Factors:** drop, change, get, retrieve, email, alert, message, analytics, track, log, monitor, format, calculate, view
- **Human-in-loop:** True

### support_resolution_suggester
- **Risk Factors:** system, update, change, alter, access, get, query, analytics, log, list, search, filter, format, view
- **Human-in-loop:** True

### finops_arr_waterfall
- **Risk Factors:** system, change, get, analytics, track, log, list, filter, sort, format, calculate, view
- **Human-in-loop:** True

### finops_burn_rate_monitor
- **Risk Factors:** drop, financial, update, get, alert, analytics, track, monitor, list, format, calculate
- **Human-in-loop:** True

### finops_scenario_planner
- **Risk Factors:** financial, update, change, get, analytics, track, monitor, format, calculate, view
- **Human-in-loop:** True

### finops_benchmark_comparator
- **Risk Factors:** financial, update, fetch, get, analytics, track, log, filter, format, calculate, view
- **Human-in-loop:** True

### finops_gross_margin
- **Risk Factors:** payment, third_party, get, analytics, track, log, format, calculate, compute
- **Human-in-loop:** True

### finops_investor_metrics
- **Risk Factors:** financial, update, change, read, get, analytics, track, log, format, view
- **Human-in-loop:** True

### finops_expense_allocator
- **Risk Factors:** financial, system, change, get, analytics, track, log, format, compute, view
- **Human-in-loop:** True

### security/dwarf-expert
- **Risk Factors:** command, write, modify, access, read, log, search, format, display, view
- **Human-in-loop:** True

### security/ask-questions-if-underspecified
- **Risk Factors:** command, change, read, get, list, format
- **Human-in-loop:** True

### security/audit-context-building
- **Risk Factors:** system, write, update, change, read, get, message, track, log, list, format, summarize, view
- **Human-in-loop:** True

### security/entry-point-analyzer
- **Risk Factors:** execute, system, modify, change, access, read, get, query, track, list, filter, format, view
- **Human-in-loop:** True

### security/semgrep-rule-creator
- **Risk Factors:** remove, eval, system, command, write, alter, read, fetch, get, alert, message, track, list, format, view
- **Human-in-loop:** True

### security/constant-time-analysis
- **Risk Factors:** secret, log, filter, view
- **Human-in-loop:** True

### security/property-based-testing
- **Risk Factors:** remove, write, access, read, get, message, log, list, sort, format, view
- **Human-in-loop:** True

### security/differential-review
- **Risk Factors:** remove, system, command, write, change, access, read, get, log, list, format, calculate, view
- **Human-in-loop:** True

### security/insecure-defaults
- **Risk Factors:** password, secret, credential, execute, access, authorize, permission, read, fetch, get, log, list, search, format, view
- **Human-in-loop:** True

### security/variant-analysis
- **Risk Factors:** eval, system, write, change, authenticate, read, track, log, list, search, view
- **Human-in-loop:** True

### security/firebase-apk-scanner
- **Risk Factors:** remove, password, api_key, execute, write, access, authenticate, authorize, permission, pii, sensitive, read, get, email, list, search, format, summarize
- **Human-in-loop:** True

### security/fix-review
- **Risk Factors:** delete, remove, eval, system, write, change, access, read, fetch, get, retrieve, message, log, list, format, view
- **Human-in-loop:** True

### security/spec-to-code-compliance
- **Risk Factors:** remove, write, update, change, alter, access, permission, read, get, track, log, list, format, view
- **Human-in-loop:** True

### security/sharp-edges
- **Risk Factors:** remove, password, secret, eval, command, write, permission, read, get, message, log, list, view
- **Human-in-loop:** True

### security/modern-python
- **Risk Factors:** delete, remove, secret, system, shell, command, update, alter, read, get, list, sort, format, view
- **Human-in-loop:** True

### security/semgrep-rule-variant-creator
- **Risk Factors:** command, write, update, change, read, fetch, get, query, message, log, search, show, view
- **Human-in-loop:** True

### development/playwright
- **Risk Factors:** password, execute, system, command, write, get, email, message, track, log, list, format, display, show, view
- **Human-in-loop:** True

### development/code-review-checklist
- **Risk Factors:** secret, credential, system, command, change, permission, sensitive, read, log, list, format, view
- **Human-in-loop:** True

### development/d3js
- **Risk Factors:** remove, update, change, alter, access, read, get, log, monitor, list, filter, sort, format, show, view
- **Human-in-loop:** True

### development/web-assets
- **Risk Factors:** system, update, change, access, read, get, message, log, search, format, calculate, compute, display, show, view, preview
- **Human-in-loop:** True

### development/codebase-onboarding
- **Risk Factors:** system, command, read, log, list, search, format, show, view
- **Human-in-loop:** True

### compliance_pii_detector
- **Risk Factors:** truncate, financial, payment, credential, system, update, change, access, pii, personal, sensitive, confidential, get, email, alert, analytics, log, list, format, view
- **Human-in-loop:** True

### compliance_soc2_tracker
- **Risk Factors:** remove, system, change, access, authorize, personal, confidential, read, get, alert, track, log, monitor, list, format, view
- **Human-in-loop:** True

### compliance_gdpr_manager
- **Risk Factors:** delete, financial, payment, execute, system, access, personal, read, get, email, notification, analytics, log, list, search, format, calculate, view, risky_tool: data.delete
- **Human-in-loop:** True

### compliance_privacy_policy
- **Risk Factors:** delete, remove, financial, payment, update, change, access, personal, sensitive, read, get, email, notification, analytics, track, log, list, format, view
- **Human-in-loop:** True

### compliance_consent_manager
- **Risk Factors:** system, update, change, access, personal, get, email, alert, analytics, track, log, list, format, risky_tool: consent.update_preference
- **Human-in-loop:** True

### governance_context_sync
- **Risk Factors:** payment, execute, system, command, write, update, change, access, permission, sensitive, read, get, notification, message, track, log, format, calculate, show, view, preview, risky_tool: bash.execute, risky_tool: filesystem.write
- **Human-in-loop:** True

### compliance_data_retention
- **Risk Factors:** delete, remove, financial, execute, system, update, change, access, authorize, pii, personal, read, get, email, alert, log, list, format, view, risky_tool: data.delete
- **Human-in-loop:** True

### compliance_audit_preparer
- **Risk Factors:** financial, payment, system, modify, change, access, sensitive, read, get, email, track, log, monitor, list, search, format, view
- **Human-in-loop:** True

### compliance_breach_response
- **Risk Factors:** financial, password, credential, execute, system, access, authorize, pii, sensitive, read, get, email, notification, alert, log, monitor, list, format, view
- **Human-in-loop:** True

### compliance_access_reviewer
- **Risk Factors:** delete, remove, financial, system, write, modify, change, access, permission, sensitive, read, get, alert, track, log, list, format, view
- **Human-in-loop:** True

### compliance_vendor_risk
- **Risk Factors:** financial, execute, eval, system, write, change, access, pii, personal, sensitive, confidential, read, get, email, notification, alert, analytics, track, log, monitor, list, format, view
- **Human-in-loop:** True

### cursor_rules/microsoft-teams
- **Risk Factors:** system
- **Human-in-loop:** True

### cursor_rules/crewai
- **Risk Factors:** system
- **Human-in-loop:** True

### cursor_rules/typer
- **Risk Factors:** command
- **Human-in-loop:** True

### cursor_rules/click
- **Risk Factors:** command
- **Human-in-loop:** True

### cursor_rules/tensorflow
- **Risk Factors:** system, read
- **Human-in-loop:** True

### cursor_rules/aws-ecs
- **Risk Factors:** secret
- **Human-in-loop:** True

### cursor_rules/autogen
- **Risk Factors:** system
- **Human-in-loop:** True

### cursor_rules/stripe
- **Risk Factors:** payment, webhook
- **Human-in-loop:** True

### vcf_stakeholder_mapping
- **Risk Factors:** eval, system, update, access, personal, read, get, log, list, sort, format, view, risky_tool: crm.update_record
- **Human-in-loop:** True

### vcf_value_discovery
- **Risk Factors:** eval, system, update, change, personal, read, get, email, log, list, format, calculate, view, risky_tool: crm.update_record
- **Human-in-loop:** True

### plg_habit_loop_builder
- **Risk Factors:** remove, alter, read, get, notification, message, analytics, track, list, format, calculate
- **Human-in-loop:** True

### plg_feature_request_handler
- **Risk Factors:** eval, system, update, alter, confidential, read, get, query, email, notification, analytics, track, log, list, search, filter, format, view, risky_tool: crm.update_contact
- **Human-in-loop:** True

### plg_empty_state_optimizer
- **Risk Factors:** delete, remove, alter, read, get, query, message, analytics, track, list, search, filter, format, show
- **Human-in-loop:** True

### plg_onboarding_flow
- **Risk Factors:** drop, personal, read, get, email, analytics, track, log, list, format, show
- **Human-in-loop:** True

### plg_sandbox_environment
- **Risk Factors:** delete, eval, update, pii, read, get, email, analytics, track, list, format, show, view, preview
- **Human-in-loop:** True

### plg_trial_extension_evaluator
- **Risk Factors:** execute, eval, system, update, get, email, analytics, track, list, format, calculate, show, view, risky_tool: stripe.update_subscription
- **Human-in-loop:** True

### plg_pql_scoring
- **Risk Factors:** eval, personal, read, get, query, email, alert, analytics, log, list, calculate, show, view
- **Human-in-loop:** True

### plg_viral_loop
- **Risk Factors:** drop, personal, read, get, email, analytics, track, monitor, list, format, calculate, show
- **Human-in-loop:** True

### plg_guided_setup_wizard
- **Risk Factors:** remove, drop, execute, update, personal, read, get, query, email, notification, analytics, track, list, format, show, view, preview, risky_tool: supabase.update_profile
- **Human-in-loop:** True

### plg_activation
- **Risk Factors:** drop, execute, personal, read, get, query, email, message, analytics, track, log, list, format, show
- **Human-in-loop:** True

### plg_contextual_help
- **Risk Factors:** system, access, read, get, query, message, analytics, track, list, search, filter, format, show
- **Human-in-loop:** True

### plg_progressive_disclosure
- **Risk Factors:** eval, change, access, read, get, query, analytics, track, list, filter, format, calculate, show
- **Human-in-loop:** True

### plg_aha_moment_detection
- **Risk Factors:** drop, eval, update, personal, get, query, message, analytics, track, monitor, list, filter, format, calculate
- **Human-in-loop:** True

### plg_social_proof_injector
- **Risk Factors:** eval, update, permission, personal, get, query, notification, message, analytics, track, log, list, filter, format, calculate, display, show, view, preview
- **Human-in-loop:** True

### plg_friction_detector
- **Risk Factors:** drop, system, alter, read, get, analytics, track, monitor, list, format, calculate, show
- **Human-in-loop:** True

### plg_milestone_celebration
- **Risk Factors:** eval, write, personal, read, get, email, message, analytics, track, log, list, format, show, view
- **Human-in-loop:** True

### plg_interactive_tour
- **Risk Factors:** drop, access, read, get, query, analytics, track, list, format, show
- **Human-in-loop:** True

### plg_reverse_trial
- **Risk Factors:** delete, execute, change, access, get, email, message, analytics, track, log, list, format, calculate, show, view, preview
- **Human-in-loop:** True

### plg_time_to_value
- **Risk Factors:** execute, alter, personal, get, email, alert, message, analytics, track, log, monitor, list, calculate, show
- **Human-in-loop:** True

### plg_personalized_checklist
- **Risk Factors:** remove, update, alter, personal, read, get, query, analytics, track, log, list, filter, format, show, view, preview
- **Human-in-loop:** True

### plg_network_effect_amplifier
- **Risk Factors:** execute, get, email, analytics, track, list, format, calculate, view
- **Human-in-loop:** True

### data_anomaly_alerter
- **Risk Factors:** drop, change, read, fetch, get, query, email, alert, message, track, monitor, list, filter, format, calculate, view
- **Human-in-loop:** True

### data_event_validator
- **Risk Factors:** remove, update, modify, change, pii, sensitive, fetch, get, query, alert, message, analytics, track, list, format, view
- **Human-in-loop:** True

### data_dashboard_builder
- **Risk Factors:** remove, drop, change, access, permission, pii, read, get, query, email, alert, analytics, log, list, filter, format, display, show, view
- **Human-in-loop:** True

### data_etl_monitor
- **Risk Factors:** credential, eval, update, change, permission, get, query, alert, message, track, log, monitor, list, filter, format
- **Human-in-loop:** True

### data_privacy_scanner
- **Risk Factors:** remove, financial, credit_card, update, access, permission, pii, sensitive, get, query, email, alert, analytics, track, log, list, filter, format, calculate, show, view
- **Human-in-loop:** True

### data_warehouse_optimizer
- **Risk Factors:** remove, write, modify, change, alter, read, get, query, analytics, track, monitor, list, search, filter, sort, format, calculate, compute, view
- **Human-in-loop:** True

### data_funnel_optimizer
- **Risk Factors:** drop, change, read, get, query, analytics, track, list, search, format, calculate, view
- **Human-in-loop:** True

### marketing_competitor_alternatives
- **Risk Factors:** eval, system, write, update, change, alter, read, get, log, list, search, filter, sort, format, aggregate, show, view
- **Human-in-loop:** True

### marketing_meeting_insights_analyzer
- **Risk Factors:** remove, eval, change, alter, access, personal, sensitive, get, track, list, sort, format, calculate, show, view
- **Human-in-loop:** True

### marketing_connect_apps
- **Risk Factors:** execute, authorize, permission, get, email, message, log
- **Human-in-loop:** True

### marketing_tailored_resume_generator
- **Risk Factors:** remove, system, modify, change, alter, personal, read, get, query, email, analytics, track, log, list, format, compute, view
- **Human-in-loop:** True

### marketing_self_improvement_analyzer
- **Risk Factors:** remove, drop, change, personal, read, get, email, track, monitor, search, format, calculate, view
- **Human-in-loop:** True

### marketing_connect
- **Risk Factors:** drop, api_key, execute, system, update, change, access, authorize, permission, get, query, email, message, summarize
- **Human-in-loop:** True

### marketing_interface_design
- **Risk Factors:** remove, drop, payment, execute, eval, system, command, write, update, change, alter, personal, read, get, track, list, format, display, show
- **Human-in-loop:** True

### marketing_humanization_engine
- **Risk Factors:** delete, remove, drop, change, personal, read, email, message, log, list, filter, format, view
- **Human-in-loop:** True

### marketing_social_content
- **Risk Factors:** system, write, update, change, access, personal, read, get, email, analytics, track, log, list, search, sort, format, show, view
- **Human-in-loop:** True

### marketing_copywriting
- **Risk Factors:** remove, write, update, alter, access, personal, read, get, email, message, analytics, log, list, search, format, show, view, preview
- **Human-in-loop:** True

### marketing_content_research_writer
- **Risk Factors:** eval, write, alter, personal, read, get, email, notification, log, list, search, format, show, view
- **Human-in-loop:** True

### marketing_copy_editing
- **Risk Factors:** remove, system, write, update, change, alter, personal, read, get, message, analytics, log, list, format, show, view
- **Human-in-loop:** True

### marketing_social_content_generator
- **Risk Factors:** drop, command, write, change, personal, read, get, analytics, track, log, list, format, view
- **Human-in-loop:** True

### marketing_email_sequence
- **Risk Factors:** drop, payment, update, change, alter, access, personal, read, get, email, notification, track, log, list, format, calculate, summarize, show, view, preview
- **Human-in-loop:** True

### marketing_daily_report_summarizer
- **Risk Factors:** drop, execute, write, update, change, read, email, message, analytics, track, list, format, calculate, summarize, view
- **Human-in-loop:** True

### marketing_invoice_organizer
- **Risk Factors:** remove, financial, payment, execute, system, change, personal, read, get, email, track, log, list, sort, format, show, view, preview
- **Human-in-loop:** True

### marketing_file_organizer
- **Risk Factors:** delete, remove, financial, execute, system, command, modify, change, personal, sensitive, read, get, log, list, search, sort, format, compute, summarize, display, show, view
- **Human-in-loop:** True

### marketing_daily_journal_writer
- **Risk Factors:** execute, write, update, access, personal, read, get, message, analytics, track, list, format, calculate, aggregate, summarize, view
- **Human-in-loop:** True

### marketing_signup_flow_cro
- **Risk Factors:** remove, drop, password, update, change, alter, access, personal, read, get, email, message, analytics, track, log, list, format, display, show
- **Human-in-loop:** True

### marketing_paywall_upgrade_cro
- **Risk Factors:** delete, remove, destroy, payment, system, change, alter, access, personal, read, get, email, alert, analytics, track, log, list, format, summarize, display, show, view, preview
- **Human-in-loop:** True

### marketing_page_cro
- **Risk Factors:** remove, eval, write, change, alter, personal, read, get, email, message, log, list, search, filter, format, display, show, view
- **Human-in-loop:** True

### marketing_form_cro
- **Risk Factors:** remove, drop, change, alter, personal, sensitive, get, email, message, analytics, track, log, list, search, format, summarize, display, show, view
- **Human-in-loop:** True

### marketing_popup_cro
- **Risk Factors:** command, change, alter, access, personal, sensitive, read, get, email, alert, message, track, log, list, search, format, show, view, preview
- **Human-in-loop:** True

### marketing_onboarding_cro
- **Risk Factors:** remove, drop, change, permission, personal, get, email, notification, message, analytics, track, log, monitor, list, search, format, display, show, view, preview
- **Human-in-loop:** True

### marketing_programmatic_seo
- **Risk Factors:** drop, eval, system, update, change, alter, access, read, get, email, analytics, track, log, monitor, list, search, filter, sort, format, aggregate, show, view, preview
- **Human-in-loop:** True

### marketing_schema_markup
- **Risk Factors:** eval, system, write, update, change, read, get, query, analytics, track, log, monitor, list, search, format, aggregate, display, show, view
- **Human-in-loop:** True

### marketing_seo_audit
- **Risk Factors:** truncate, credential, update, change, alter, access, read, get, analytics, track, log, search, format, view
- **Human-in-loop:** True

### marketing_outreach_personalizer
- **Risk Factors:** drop, command, write, personal, read, get, email, message, log, list, format, view, preview
- **Human-in-loop:** True

### marketing_twitter_algorithm_optimizer
- **Risk Factors:** remove, drop, eval, system, write, personal, read, get, message, track, log, search, filter, format, show, view
- **Human-in-loop:** True

### marketing_analytics_tracking
- **Risk Factors:** remove, payment, system, update, change, pii, read, query, email, analytics, track, log, monitor, list, search, format, aggregate, view, preview
- **Human-in-loop:** True

### marketing_marketing_psychology
- **Risk Factors:** drop, credential, system, write, change, alter, access, personal, read, get, email, analytics, log, list, format, show, view
- **Human-in-loop:** True

### marketing_campaign_plan_architect
- **Risk Factors:** execute, system, write, update, personal, read, get, email, message, track, log, list, format, calculate, view
- **Human-in-loop:** True

### marketing_marketing_ideas
- **Risk Factors:** remove, payment, execute, system, write, update, change, alter, access, personal, sensitive, read, get, email, message, analytics, log, list, search, format, aggregate, show, view
- **Human-in-loop:** True

### marketing_referral_program
- **Risk Factors:** drop, payment, system, write, update, access, personal, read, get, email, analytics, track, log, monitor, list, calculate, view
- **Human-in-loop:** True

### marketing_launch_strategy
- **Risk Factors:** system, update, change, access, read, get, email, notification, message, analytics, track, log, monitor, list, search, display, view, preview
- **Human-in-loop:** True

### marketing_free_tool_strategy
- **Risk Factors:** drop, financial, eval, change, access, personal, read, get, query, email, analytics, track, log, list, search, format, show, view, preview
- **Human-in-loop:** True

### marketing_pricing_strategy
- **Risk Factors:** remove, payment, eval, update, change, alter, access, read, get, email, message, analytics, track, log, monitor, list, search, show, view
- **Human-in-loop:** True

### marketing_slack_gif_creator
- **Risk Factors:** system, update, modify, read, get, message, calculate
- **Human-in-loop:** True

### people_dei_tracker
- **Risk Factors:** drop, system, update, change, access, get, retrieve, analytics, track, log, list, format, calculate, compute, aggregate, view
- **Human-in-loop:** True

### people_offboarding_manager
- **Risk Factors:** credential, execute, system, update, change, access, confidential, get, retrieve, email, notification, message, track, list, format, calculate, aggregate, view
- **Human-in-loop:** True

### people_candidate_sourcer
- **Risk Factors:** remove, eval, alter, personal, get, query, message, analytics, track, monitor, list, search, filter, sort, format, view
- **Human-in-loop:** True

### people_perf_review_generator
- **Risk Factors:** eval, change, personal, confidential, read, get, retrieve, alert, analytics, list, format, calculate, aggregate, view
- **Human-in-loop:** True

### people_onboarding_checklist
- **Risk Factors:** credential, eval, system, update, access, personal, read, get, retrieve, email, notification, alert, message, track, log, monitor, list, format, view, risky_tool: hr.update_status
- **Human-in-loop:** True

### people_pulse_analyzer
- **Risk Factors:** drop, change, access, get, retrieve, alert, analytics, track, log, monitor, list, filter, format, calculate, aggregate, show
- **Human-in-loop:** True

### anthropic_official/doc-coauthoring
- **Risk Factors:** remove, execute, write, update, change, alter, access, read, fetch, get, track, list, search, format, summarize, show, view
- **Human-in-loop:** True

### anthropic_official/xlsx
- **Risk Factors:** delete, financial, eval, system, write, update, modify, change, read, list, search, format, calculate, view, preview
- **Human-in-loop:** True

### anthropic_official/pdf
- **Risk Factors:** remove, password, command, write, read, get, view
- **Human-in-loop:** True

### anthropic_official/algorithmic-art
- **Risk Factors:** drop, system, write, update, change, read, get, format, display, show, view
- **Human-in-loop:** True

### anthropic_official/skill-creator
- **Risk Factors:** delete, remove, financial, execute, system, command, write, update, modify, change, read, get, query, message, track, log, list, search, format, show, view, preview
- **Human-in-loop:** True

### anthropic_official/canvas-design
- **Risk Factors:** system, write, read, get, log, list, search, filter, format, display, show, view
- **Human-in-loop:** True

### anthropic_official/pptx
- **Risk Factors:** delete, system, shell, write, update, modify, access, read, get, list, search, filter, format, display, show, view
- **Human-in-loop:** True

### anthropic_official/slack-gif-creator
- **Risk Factors:** remove, update, read, get, message, log, list, filter, calculate
- **Human-in-loop:** True

### anthropic_official/webapp-testing
- **Risk Factors:** execute, write, read, log, show, view
- **Human-in-loop:** True

### anthropic_official/frontend-design
- **Risk Factors:** execute, system, access, get, list, display, show, view
- **Human-in-loop:** True

### anthropic_official/mcp-builder
- **Risk Factors:** eval, change, read, fetch, message, list, search, filter, format, view
- **Human-in-loop:** True

### anthropic_official/brand-guidelines
- **Risk Factors:** system, access, read, sort, format, view
- **Human-in-loop:** True

### anthropic_official/docx
- **Risk Factors:** system, write, update, modify, change, access, read, get, track, log, format, show, view
- **Human-in-loop:** True

### anthropic_official/web-artifacts-builder
- **Risk Factors:** system, log, display, view
- **Human-in-loop:** True

### cs_health_scoring
- **Risk Factors:** drop, financial, payment, update, get, query, alert, analytics, monitor, list, format, calculate, compute, risky_tool: crm.update_account
- **Human-in-loop:** True

### cs_customer_maturity_model
- **Risk Factors:** eval, system, read, get, query, analytics, track, list, format, calculate, view, risky_tool: crm.update_account
- **Human-in-loop:** True

### cs_adoption_score
- **Risk Factors:** drop, change, read, get, query, alert, analytics, log, list, format, calculate, compute, risky_tool: crm.update_account
- **Human-in-loop:** True

### cs_contract_intelligence
- **Risk Factors:** financial, payment, change, read, get, retrieve, alert, analytics, track, monitor, list, format, view
- **Human-in-loop:** True

### cs_onboarding_health
- **Risk Factors:** execute, system, access, read, get, retrieve, query, email, alert, analytics, track, log, monitor, list, format, calculate, view
- **Human-in-loop:** True

### cs_expansion_playbook
- **Risk Factors:** execute, personal, get, track, list, format, show
- **Human-in-loop:** True

### cs_quarterly_business_review
- **Risk Factors:** financial, access, read, get, retrieve, analytics, list, format, show, view, preview
- **Human-in-loop:** True

### cs_playbook_selector
- **Risk Factors:** drop, execute, modify, change, alter, personal, get, query, message, analytics, track, list, format, view
- **Human-in-loop:** True

### cs_churn_prediction
- **Risk Factors:** drop, payment, get, query, alert, track, log, monitor, list, format, calculate
- **Human-in-loop:** True

### cs_red_flag_detector
- **Risk Factors:** drop, financial, payment, eval, change, alter, get, query, email, alert, analytics, track, log, monitor, list, format, view, risky_tool: crm.update_account
- **Human-in-loop:** True

### cs_stakeholder_mapper
- **Risk Factors:** financial, eval, update, change, access, read, get, retrieve, query, alert, analytics, track, log, monitor, list, format, view, risky_tool: crm.update_contact
- **Human-in-loop:** True

### cs_risk_mitigation_playbook
- **Risk Factors:** remove, drop, financial, execute, eval, change, get, query, alert, message, analytics, track, log, monitor, list, format, view
- **Human-in-loop:** True

### cs_escalation_manager
- **Risk Factors:** execute, update, get, email, alert, message, track, log, monitor, list, format, view
- **Human-in-loop:** True

### cs_csql_generator
- **Risk Factors:** eval, personal, read, get, retrieve, alert, analytics, track, list, format, calculate
- **Human-in-loop:** True

### cs_nps_followup
- **Risk Factors:** execute, change, personal, get, retrieve, alert, track, list, format, view
- **Human-in-loop:** True

### cs_customer_journey_orchestrator
- **Risk Factors:** drop, execute, eval, system, personal, read, get, query, email, analytics, track, monitor, list, format, view
- **Human-in-loop:** True

### cs_renewal_orchestration
- **Risk Factors:** execute, get, query, track, monitor, list, format, view
- **Human-in-loop:** True

### cs_vla_tracker
- **Risk Factors:** drop, modify, get, retrieve, alert, analytics, track, monitor, list, format, calculate, view, risky_tool: crm.update_account
- **Human-in-loop:** True

### cs_product_gap_reporter
- **Risk Factors:** eval, update, change, alter, confidential, get, query, analytics, log, monitor, list, search, format, calculate, aggregate, view
- **Human-in-loop:** True

### community_event_manager
- **Risk Factors:** credential, get, email, message, analytics, track, log, list, format, calculate, show, view, preview
- **Human-in-loop:** True

### community_ama_orchestrator
- **Risk Factors:** remove, personal, sensitive, get, email, notification, alert, analytics, track, log, list, filter, format, summarize, view, preview
- **Human-in-loop:** True

### community_user_group_manager
- **Risk Factors:** drop, update, change, access, get, email, analytics, track, list, filter, format, calculate, view, risky_tool: crm.update_contact
- **Human-in-loop:** True

### community_forum_moderator
- **Risk Factors:** remove, personal, read, get, email, notification, message, analytics, track, list, format, view, risky_tool: crm.update_contact
- **Human-in-loop:** True

### community_champion_identifier
- **Risk Factors:** drop, eval, update, access, personal, read, get, analytics, track, log, monitor, list, format, calculate, show, view, risky_tool: crm.update_contact
- **Human-in-loop:** True

### community_swag_manager
- **Risk Factors:** eval, access, get, email, notification, alert, message, analytics, track, list, format, calculate
- **Human-in-loop:** True

### community_hackathon_manager
- **Risk Factors:** execute, read, get, email, notification, analytics, track, log, list, format, show, view
- **Human-in-loop:** True

### ai_document_parser
- **Risk Factors:** financial, pii, sensitive, read, log, list, format, view, preview, risky_tool: crm.update_record
- **Human-in-loop:** True

### ai_ops/prompt-engineering
- **Risk Factors:** remove, eval, system, write, get, email, message, log, list, format, calculate, summarize, show, view
- **Human-in-loop:** True

### ai_anomaly_detector
- **Risk Factors:** drop, financial, system, change, access, alert, track, log, monitor, list, format, calculate
- **Human-in-loop:** True

### ai_chatbot_orchestrator
- **Risk Factors:** execute, eval, update, change, sensitive, read, get, message, analytics, track, log, list, format, view
- **Human-in-loop:** True

### ai_meeting_intelligence
- **Risk Factors:** financial, change, alter, authorize, confidential, get, format, view, risky_tool: crm.update_deal
- **Human-in-loop:** True

### ai_ticket_classifier
- **Risk Factors:** payment, access, sensitive, get, email, log, list, format, calculate, view
- **Human-in-loop:** True

### ai_data_quality_agent
- **Risk Factors:** system, update, change, access, permission, pii, sensitive, get, email, alert, log, monitor, list, format, calculate
- **Human-in-loop:** True

### ai_agent_performance
- **Risk Factors:** system, change, get, query, alert, track, log, monitor, list, format, calculate
- **Human-in-loop:** True

### ai_workflow_automator
- **Risk Factors:** execute, eval, system, update, personal, fetch, log, list, format, risky_tool: workflow.execute_step
- **Human-in-loop:** True

### revops_opportunity_scoring
- **Risk Factors:** eval, update, change, access, read, get, email, analytics, log, list, filter, sort, format, calculate, view, risky_tool: crm.update_deal
- **Human-in-loop:** True

### revops_deal_inspection
- **Risk Factors:** eval, system, update, change, access, confidential, read, get, email, alert, analytics, log, list, format, calculate, view, risky_tool: crm.update_deal
- **Human-in-loop:** True

### revops_activity_capture
- **Risk Factors:** delete, eval, update, authorize, personal, read, get, email, message, list, filter, sort, format, view
- **Human-in-loop:** True

### revops_cpq_quote_generator
- **Risk Factors:** remove, payment, eval, update, get, retrieve, track, log, list, format, calculate, view, risky_tool: crm.update_deal
- **Human-in-loop:** True

### revops_pricing_guidance
- **Risk Factors:** payment, update, alter, access, sensitive, get, alert, analytics, track, log, list, format, calculate
- **Human-in-loop:** True

### revops_multi_thread_tracker
- **Risk Factors:** eval, read, get, email, alert, track, list, filter, format, calculate, risky_tool: crm.update_contact
- **Human-in-loop:** True

### revops_deal_velocity
- **Risk Factors:** drop, change, get, analytics, track, list, sort, calculate
- **Human-in-loop:** True

### revops_lead_routing
- **Risk Factors:** system, alter, get, retrieve, notification, alert, analytics, log, list, format
- **Human-in-loop:** True

### revops_competitive_intel
- **Risk Factors:** eval, update, change, sensitive, read, get, alert, analytics, track, list, search, filter, sort, format, view
- **Human-in-loop:** True

### revops_stage_duration
- **Risk Factors:** drop, change, get, alert, analytics, track, list, filter, sort, format, calculate, view
- **Human-in-loop:** True

### revops_next_best_action
- **Risk Factors:** execute, alter, access, personal, read, get, email, analytics, list, search, filter, format, calculate
- **Human-in-loop:** True

### revops_pipeline_health
- **Risk Factors:** drop, update, read, get, retrieve, email, alert, track, monitor, list, search, filter, calculate, view, risky_tool: crm.update_deal
- **Human-in-loop:** True

### revops_lead_qualification
- **Risk Factors:** eval, get, query, email, analytics, track, log, list, format, view
- **Human-in-loop:** True

### revops_commit_accuracy
- **Risk Factors:** system, update, change, read, get, alert, analytics, track, list, filter, sort, format, calculate
- **Human-in-loop:** True

### mon_mrr_movement_tracker
- **Risk Factors:** system, change, get, analytics, track, log, list, filter, sort, format, calculate
- **Human-in-loop:** True

### mon_cohort_ltv_analyzer
- **Risk Factors:** drop, update, get, analytics, track, list, search, format, calculate
- **Human-in-loop:** True

### mon_dunning_automation
- **Risk Factors:** payment, execute, system, update, get, email, alert, list, format
- **Human-in-loop:** True

### mon_usage_metering
- **Risk Factors:** system, alert, track, list, format, compute, aggregate
- **Human-in-loop:** True

### mon_discount_optimizer
- **Risk Factors:** payment, eval, alter, sensitive, get, retrieve, analytics, track, log, list, format
- **Human-in-loop:** True

### mon_price_experimentation
- **Risk Factors:** execute, get, analytics, track, monitor, list, format
- **Human-in-loop:** True

### mon_packaging_optimizer
- **Risk Factors:** eval, system, change, get, analytics, track, list, format, view
- **Human-in-loop:** True

### mon_tax_compliance
- **Risk Factors:** system, update, change, read, get, alert, analytics, track, log, monitor, list, format, calculate, view, risky_tool: stripe.update_customer
- **Human-in-loop:** True

### mon_contract_value_tracker
- **Risk Factors:** drop, financial, payment, update, modify, change, read, get, retrieve, alert, analytics, track, log, list, format, calculate, view
- **Human-in-loop:** True

### mon_payment_method_optimizer
- **Risk Factors:** payment, update, get, retrieve, email, analytics, track, log, list, format, risky_tool: stripe.update_customer
- **Human-in-loop:** True

### mon_upgrade_trigger
- **Risk Factors:** execute, update, personal, email, message, list, format, show, risky_tool: stripe.update_subscription
- **Human-in-loop:** True

### superpowers/using-git-worktrees
- **Risk Factors:** system, command, change, alter, permission, read, get, track, show, view
- **Human-in-loop:** True

### superpowers/test-driven-development
- **Risk Factors:** delete, remove, system, write, change, permission, read, get, email, message, list, show, view
- **Human-in-loop:** True

### superpowers/systematic-debugging
- **Risk Factors:** secret, system, write, change, read, message, log, monitor, list, search, format, show, view
- **Human-in-loop:** True

### superpowers/dispatching-parallel-agents
- **Risk Factors:** system, change, read, get, message, track, log, view
- **Human-in-loop:** True

### superpowers/executing-plans
- **Risk Factors:** execute, write, update, change, read, show, view
- **Human-in-loop:** True

### superpowers/finishing-a-development-branch
- **Risk Factors:** delete, remove, execute, command, change, get, list, show, view
- **Human-in-loop:** True

### superpowers/brainstorming
- **Risk Factors:** remove, write, modify, alter, read, message, log, view
- **Human-in-loop:** True

### superpowers/writing-plans
- **Risk Factors:** command, write, modify, log, view
- **Human-in-loop:** True

### superpowers/receiving-code-review
- **Risk Factors:** delete, remove, drop, eval, write, change, read, get, track, log, filter, format, show, view
- **Human-in-loop:** True

### superpowers/writing-skills
- **Risk Factors:** delete, eval, system, shell, command, write, update, change, personal, read, get, query, message, log, list, search, filter, format, summarize, show, view
- **Human-in-loop:** True

### superpowers/verification-before-completion
- **Risk Factors:** execute, command, write, change, read, message, log, list, show, view
- **Human-in-loop:** True

### superpowers/subagent-driven-development
- **Risk Factors:** remove, execute, system, command, write, alter, read, get, format, view
- **Human-in-loop:** True

### plgf_expansion_revenue
- **Risk Factors:** execute, eval, update, personal, read, get, analytics, track, list, search, format, calculate, risky_tool: stripe.update_subscription, risky_tool: crm.update_account
- **Human-in-loop:** True

### plg_frameworks/plg-ideas
- **Risk Factors:** remove, drop, financial, payment, system, command, change, access, personal, webhook, read, get, email, notification, message, analytics, track, log, list, search, filter, format, summarize, display, show, view, preview
- **Human-in-loop:** True

### plgf_engagement_loops
- **Risk Factors:** remove, system, personal, get, email, notification, message, analytics, track, monitor, list, search, format
- **Human-in-loop:** True

### plgf_referral_program
- **Risk Factors:** drop, financial, payment, eval, access, personal, get, email, notification, message, analytics, track, log, monitor, list, format, calculate, view
- **Human-in-loop:** True

### plgf_activation_metrics
- **Risk Factors:** drop, payment, update, personal, read, get, message, analytics, track, list, format
- **Human-in-loop:** True

### plgf_user_segmentation
- **Risk Factors:** system, update, change, access, personal, read, get, email, alert, message, analytics, list, search, format, calculate, view, risky_tool: lifecycle.update_segment
- **Human-in-loop:** True

### plgf_mental_models
- **Risk Factors:** drop, update, access, read, get, query, message, analytics, list, filter, format, view
- **Human-in-loop:** True

### plg_frameworks/boyce
- **Risk Factors:** eval, read, log
- **Human-in-loop:** True

### boyce_growth_team_orchestrator
- **Risk Factors:** remove, update, change, read, get, analytics, track, log, list, format, calculate, show, view
- **Human-in-loop:** True

### boyce_plg_audit
- **Risk Factors:** eval, change, read, get, analytics, track, list, format, calculate, view
- **Human-in-loop:** True

### boyce_sidecar_product_builder
- **Risk Factors:** remove, payment, eval, alter, read, get, message, log, list, search, format, show
- **Human-in-loop:** True

### boyce_usage_retention_optimizer
- **Risk Factors:** system, change, get, email, notification, analytics, track, list, filter, format, calculate
- **Human-in-loop:** True

### boyce_first_impact_optimizer
- **Risk Factors:** remove, execute, eval, alter, read, get, query, analytics, track, list, format, calculate, show
- **Human-in-loop:** True

### boyce_enterprise_plg_transition
- **Risk Factors:** remove, read, get, track, log, list, format
- **Human-in-loop:** True

### boyce_ai_gtm_automator
- **Risk Factors:** payment, system, personal, get, email, track, log, monitor, list, format, show, view
- **Human-in-loop:** True

### boyce_plg_pricing_architect
- **Risk Factors:** financial, change, permission, read, get, email, message, analytics, track, log, list, format, show
- **Human-in-loop:** True

### boyce_plg_bowtie_mapper
- **Risk Factors:** remove, payment, update, get, email, analytics, track, log, list, format, calculate, view
- **Human-in-loop:** True

### boyce_product_led_sales
- **Risk Factors:** execute, eval, update, change, read, get, alert, message, analytics, track, log, monitor, list, calculate, show, risky_tool: crm.update_account
- **Human-in-loop:** True

### boyce_acquisition_loop_designer
- **Risk Factors:** eval, get, email, notification, analytics, track, list, format, calculate, view
- **Human-in-loop:** True

### plg_frameworks/plg-strategy
- **Risk Factors:** eval, system, update, change, access, read, get, email, notification, analytics, track, log, list, search, format, show, view
- **Human-in-loop:** True

### plgf_retention_analysis
- **Risk Factors:** drop, payment, system, update, access, personal, read, get, email, message, analytics, track, log, list, search, format, show
- **Human-in-loop:** True

### plgf_feature_gating
- **Risk Factors:** remove, eval, change, access, personal, read, get, query, email, analytics, log, monitor, list, filter, format, compute, show, view, preview
- **Human-in-loop:** True

### plgf_product_onboarding
- **Risk Factors:** drop, system, access, personal, read, get, analytics, track, log, list, search, format, show, view
- **Human-in-loop:** True

### plgf_trial_optimization
- **Risk Factors:** drop, payment, eval, change, access, personal, read, get, email, analytics, track, list, format, view
- **Human-in-loop:** True

### plgf_product_analytics
- **Risk Factors:** drop, payment, api_key, system, update, pii, read, get, query, email, analytics, track, list, search, filter, sort, format, calculate, view
- **Human-in-loop:** True

### plgf_self_serve_motion
- **Risk Factors:** remove, drop, payment, eval, modify, change, alter, access, read, get, email, analytics, track, monitor, list, format, calculate, display, show, view
- **Human-in-loop:** True

### plgf_paywall_upgrade_cro
- **Risk Factors:** payment, eval, change, access, sensitive, read, get, email, analytics, track, log, list, format, display, show, view, preview
- **Human-in-loop:** True

### plg_frameworks/plg-metrics
- **Risk Factors:** drop, payment, eval, system, change, read, get, notification, alert, message, analytics, track, log, list, filter, format, view
- **Human-in-loop:** True

### plgf_strategy
- **Risk Factors:** remove, eval, read, get, analytics, track, list, format, calculate
- **Human-in-loop:** True

### plgf_viral_loops
- **Risk Factors:** drop, personal, read, get, email, notification, analytics, track, list, sort, format, calculate, show, view, preview
- **Human-in-loop:** True

### plgf_growth_modeling
- **Risk Factors:** system, update, change, get, analytics, log, list, format, calculate, view
- **Human-in-loop:** True

### plg_frameworks/install-plg-skills
- **Risk Factors:** remove, system, write, update, alter, permission, personal, read, get, message, analytics, log, list
- **Human-in-loop:** True

### plg_frameworks/plg-mental-models
- **Risk Factors:** drop, eval, system, modify, change, alter, access, read, get, email, notification, message, track, log, list, search, format, show
- **Human-in-loop:** True

### plgf_ideas
- **Risk Factors:** remove, payment, system, change, alter, personal, read, get, email, notification, track, list, search, filter, format, show, view, preview
- **Human-in-loop:** True

### plgf_metrics
- **Risk Factors:** drop, system, change, read, get, alert, analytics, track, log, format, view
- **Human-in-loop:** True

### plgf_free_tool_strategy
- **Risk Factors:** eval, write, update, change, alter, personal, get, email, analytics, track, log, list, search, format, aggregate, view, preview
- **Human-in-loop:** True

### plgf_signup_flow_cro
- **Risk Factors:** remove, drop, password, system, change, alter, access, personal, get, email, analytics, monitor, list, format, show
- **Human-in-loop:** True

### plgf_product_led_sales
- **Risk Factors:** system, update, personal, read, get, email, notification, alert, analytics, track, log, monitor, list, search, format, calculate, aggregate, view, risky_tool: crm.update_record
- **Human-in-loop:** True

### plgf_growth_loops
- **Risk Factors:** system, get, analytics, track, list, search, format, view
- **Human-in-loop:** True

### plgf_in_product_messaging
- **Risk Factors:** drop, system, access, personal, read, get, alert, message, analytics, track, log, list, filter, format, calculate, display, show, view
- **Human-in-loop:** True

### plgf_feature_adoption
- **Risk Factors:** remove, access, get, email, message, analytics, track, log, list, search, format, show, view
- **Human-in-loop:** True

### plgf_usage_based_pricing
- **Risk Factors:** system, change, get, email, alert, message, analytics, track, list, format, compute, aggregate, display, show
- **Human-in-loop:** True

### plg_frameworks/growth-experimentation
- **Risk Factors:** drop, system, write, update, change, read, get, analytics, track, log, monitor, list, format, calculate, show, view
- **Human-in-loop:** True

### scientific/metabolomics-workbench-database
- **Risk Factors:** system, access, read, get, retrieve, query, log, list, search, filter, format, calculate, view
- **Human-in-loop:** True

### scientific/benchling-integration
- **Risk Factors:** remove, password, secret, credential, api_key, execute, system, write, update, change, access, permission, read, get, query, email, notification, analytics, log, monitor, list, search, filter, format, aggregate, view
- **Human-in-loop:** True

### scientific/networkx
- **Risk Factors:** remove, system, write, modify, read, get, query, log, list, search, format, compute, show, view
- **Human-in-loop:** True

### scientific/anndata
- **Risk Factors:** system, command, write, alter, access, read, get, track, log, list, search, filter, format, view
- **Human-in-loop:** True

### scientific/scikit-survival
- **Risk Factors:** eval, system, alter, read, get, list, search, format, view
- **Human-in-loop:** True

### scientific/qiskit
- **Risk Factors:** execute, eval, system, read, get, log, monitor, search, compute, display, view
- **Human-in-loop:** True

### scientific/uspto-database
- **Risk Factors:** payment, api_key, eval, system, change, access, read, get, retrieve, query, alert, track, log, monitor, search, format, view
- **Human-in-loop:** True

### scientific/scientific-brainstorming
- **Risk Factors:** remove, eval, system, modify, change, personal, read, get, log, list, search, summarize, show, view
- **Human-in-loop:** True

### scientific/kegg-database
- **Risk Factors:** remove, system, access, read, get, retrieve, query, log, list, search, format, view
- **Human-in-loop:** True

### scientific/pymc
- **Risk Factors:** system, update, alter, read, get, log, list, search, format, view
- **Human-in-loop:** True

### scientific/paper-2-web
- **Risk Factors:** remove, api_key, eval, system, write, access, personal, read, get, log, list, search, format, show, view
- **Human-in-loop:** True

### scientific/perplexity-search
- **Risk Factors:** api_key, system, change, access, sensitive, read, get, query, log, monitor, search, format, view
- **Human-in-loop:** True

### scientific/research-lookup
- **Risk Factors:** api_key, eval, system, command, write, change, alter, access, read, get, query, message, log, search, format, show, view
- **Human-in-loop:** True

### scientific/shap
- **Risk Factors:** system, change, alter, read, track, log, monitor, search, sort, format, calculate, compute, display, show, view
- **Human-in-loop:** True

### scientific/zinc-database
- **Risk Factors:** eval, system, change, alter, access, read, get, retrieve, query, email, log, list, search, filter, format, view
- **Human-in-loop:** True

### scientific/umap-learn
- **Risk Factors:** drop, eval, system, access, read, get, log, list, search, format, calculate, show, view
- **Human-in-loop:** True

### scientific/imaging-data-commons
- **Risk Factors:** execute, system, command, write, update, alter, access, read, fetch, get, query, log, list, search, filter, sort, format, aggregate, view, preview
- **Human-in-loop:** True

### scientific/sympy
- **Risk Factors:** eval, system, read, get, log, search, format, calculate, compute, show, view
- **Human-in-loop:** True

### scientific/vaex
- **Risk Factors:** financial, execute, eval, write, access, read, search, filter, format, compute, aggregate, show, view
- **Human-in-loop:** True

### scientific/alphafold-database
- **Risk Factors:** shell, command, write, update, alter, access, read, get, retrieve, query, log, list, search, filter, format, calculate, show, view
- **Human-in-loop:** True

### scientific/dask
- **Risk Factors:** delete, drop, execute, read, get, analytics, log, monitor, search, filter, format, compute, aggregate, view
- **Human-in-loop:** True

### scientific/get-available-resources
- **Risk Factors:** execute, system, change, permission, read, get, log, search, format, compute, view
- **Human-in-loop:** True

### scientific/cosmic-database
- **Risk Factors:** password, command, update, alter, access, read, fetch, get, retrieve, query, email, log, list, search, filter, format, show, view
- **Human-in-loop:** True

### scientific/iso-13485-certification
- **Risk Factors:** remove, system, write, update, change, read, get, log, monitor, list, search, format, calculate, summarize, show, view
- **Human-in-loop:** True

### scientific/gene-database
- **Risk Factors:** eval, system, alter, access, read, fetch, retrieve, query, log, list, search, filter, format, view
- **Human-in-loop:** True

### scientific/biorxiv-database
- **Risk Factors:** system, read, fetch, get, retrieve, query, track, log, monitor, list, search, filter, format, show, view
- **Human-in-loop:** True

### scientific/fred-economic-data
- **Risk Factors:** financial, api_key, eval, update, change, access, read, fetch, get, retrieve, query, message, log, monitor, search, filter, sort, format, aggregate, view
- **Human-in-loop:** True

### scientific/esm
- **Risk Factors:** remove, execute, access, read, get, track, log, monitor, list, search, view
- **Human-in-loop:** True

### scientific/scientific-schematics
- **Risk Factors:** remove, api_key, eval, system, command, write, access, read, get, log, list, search, sort, format, display, show, view
- **Human-in-loop:** True

### scientific/geniml
- **Risk Factors:** eval, system, command, access, read, query, track, log, list, search, filter, compute, view
- **Human-in-loop:** True

### scientific/geopandas
- **Risk Factors:** system, write, modify, read, get, log, search, filter, format, calculate, aggregate
- **Human-in-loop:** True

### scientific/seaborn
- **Risk Factors:** remove, change, sensitive, read, get, log, list, search, format, compute, aggregate, display, show, view
- **Human-in-loop:** True

### scientific/deeptools
- **Risk Factors:** remove, system, command, read, get, track, log, list, search, filter, format, compute, show, view
- **Human-in-loop:** True

### scientific/protocolsio-integration
- **Risk Factors:** delete, execute, update, change, access, authenticate, permission, personal, read, get, retrieve, query, notification, track, log, monitor, list, search, filter, format, view
- **Human-in-loop:** True

### scientific/medchem
- **Risk Factors:** system, access, read, get, query, alert, track, log, list, search, filter, format, calculate, view
- **Human-in-loop:** True

### scientific/fluidsim
- **Risk Factors:** execute, system, access, read, get, list, search, format, view
- **Human-in-loop:** True

### scientific/pymatgen
- **Risk Factors:** api_key, system, write, change, access, read, get, retrieve, track, list, search, filter, format, calculate, compute, show, view
- **Human-in-loop:** True

### scientific/molfeat
- **Risk Factors:** remove, eval, read, get, query, log, list, search, sort, format, compute, display, view
- **Human-in-loop:** True

### scientific/geo-database
- **Risk Factors:** api_key, write, change, access, read, fetch, get, retrieve, query, email, log, list, search, filter, format, calculate, view
- **Human-in-loop:** True

### scientific/citation-management
- **Risk Factors:** remove, eval, system, write, update, alter, access, read, fetch, get, retrieve, query, alert, track, log, list, search, filter, sort, format, view
- **Human-in-loop:** True

### scientific/scientific-critical-thinking
- **Risk Factors:** drop, eval, system, write, change, alter, access, personal, sensitive, read, get, log, list, search, sort, format, show, view
- **Human-in-loop:** True

### scientific/pydicom
- **Risk Factors:** remove, system, write, update, modify, alter, access, sensitive, read, get, log, list, search, sort, format, display, show, view
- **Human-in-loop:** True

### scientific/markitdown
- **Risk Factors:** remove, api_key, system, command, write, access, read, fetch, get, message, list, search, format, compute, view
- **Human-in-loop:** True

### scientific/hmdb-database
- **Risk Factors:** system, update, alter, access, permission, read, get, retrieve, query, track, log, list, search, filter, format, view
- **Human-in-loop:** True

### scientific/pytdc
- **Risk Factors:** eval, system, access, read, get, retrieve, log, search, filter, format, view
- **Human-in-loop:** True

### scientific/histolab
- **Risk Factors:** remove, system, access, read, get, track, log, monitor, list, search, filter, format, display, show, view, preview
- **Human-in-loop:** True

### scientific/rowan
- **Risk Factors:** api_key, eval, access, read, fetch, get, retrieve, query, message, log, monitor, list, search, filter, sort, format, calculate, compute, view
- **Human-in-loop:** True

### scientific/clinvar-database
- **Risk Factors:** eval, command, update, change, access, read, fetch, get, retrieve, query, email, track, log, list, search, filter, format, aggregate, view
- **Human-in-loop:** True

### scientific/pubchem-database
- **Risk Factors:** eval, write, alter, access, read, get, retrieve, query, log, list, search, filter, format, summarize, view
- **Human-in-loop:** True

### scientific/drugbank-database
- **Risk Factors:** password, credential, update, access, read, get, retrieve, query, log, search, filter, format, calculate, view
- **Human-in-loop:** True

### scientific/cobrapy
- **Risk Factors:** remove, secret, system, write, modify, change, access, read, get, query, log, list, search, format, calculate, show, view
- **Human-in-loop:** True

### scientific/opentrons-integration
- **Risk Factors:** remove, drop, execute, command, write, update, access, read, get, email, track, log, list, search, display, view
- **Human-in-loop:** True

### scientific/brenda-database
- **Risk Factors:** password, credential, eval, system, alter, access, read, get, retrieve, query, email, track, log, monitor, list, search, filter, sort, format, calculate, view
- **Human-in-loop:** True

### scientific/fda-database
- **Risk Factors:** api_key, access, read, get, query, email, notification, track, log, monitor, list, search, format, view
- **Human-in-loop:** True

### scientific/biopython
- **Risk Factors:** api_key, update, access, read, fetch, get, email, log, list, search, filter, format, calculate, display, view
- **Human-in-loop:** True

### scientific/gtars
- **Risk Factors:** eval, shell, command, access, read, get, query, track, log, search, filter, format, compute, view
- **Human-in-loop:** True

### scientific/scvi-tools
- **Risk Factors:** remove, system, write, change, access, read, get, log, list, search, filter, format, view
- **Human-in-loop:** True

### scientific/lamindb
- **Risk Factors:** eval, system, access, authenticate, permission, personal, read, get, query, track, log, list, search, filter, format, compute, view
- **Human-in-loop:** True

### scientific/pptx-posters
- **Risk Factors:** remove, system, command, write, update, read, get, message, log, list, search, format, display, show, view, preview
- **Human-in-loop:** True

### scientific/datamol
- **Risk Factors:** remove, system, write, access, read, get, query, log, list, search, filter, sort, format, calculate, compute, display, show, view
- **Human-in-loop:** True

### scientific/research-grants
- **Risk Factors:** eval, system, write, change, alter, access, read, get, track, log, monitor, list, search, format, calculate, summarize, show, view
- **Human-in-loop:** True

### scientific/ensembl-database
- **Risk Factors:** eval, access, read, fetch, get, retrieve, query, log, list, search, format, show, view
- **Human-in-loop:** True

### scientific/treatment-plans
- **Risk Factors:** remove, credential, eval, system, command, write, update, modify, change, alter, access, authenticate, personal, read, get, alert, track, log, monitor, list, search, format, summarize, view
- **Human-in-loop:** True

### scientific/plotly
- **Risk Factors:** drop, financial, write, update, read, log, search, display, show
- **Human-in-loop:** True

### scientific/statistical-analysis
- **Risk Factors:** system, write, change, alter, read, get, log, list, search, format, calculate, compute, summarize, show, view
- **Human-in-loop:** True

### scientific/denario
- **Risk Factors:** execute, system, alter, read, get, log, list, search, format, compute, view
- **Human-in-loop:** True

### scientific/matchms
- **Risk Factors:** remove, access, read, get, query, list, search, filter, sort, format, calculate, view
- **Human-in-loop:** True

### scientific/scientific-writing
- **Risk Factors:** remove, financial, eval, system, command, write, alter, access, read, get, message, log, list, search, sort, format, compute, display, show, view
- **Human-in-loop:** True

### scientific/clinical-decision-support
- **Risk Factors:** remove, system, write, update, alter, access, confidential, read, get, log, monitor, search, sort, format, calculate, show, view
- **Human-in-loop:** True

### scientific/diffdock
- **Risk Factors:** remove, system, command, alter, read, get, log, list, search, filter, format, compute, show, view
- **Human-in-loop:** True

### scientific/neurokit2
- **Risk Factors:** system, change, access, read, track, log, monitor, search, filter, format, compute, view
- **Human-in-loop:** True

### scientific/clinpgx-database
- **Risk Factors:** system, update, change, alter, access, personal, read, get, retrieve, query, log, monitor, list, search, filter, sort, format, calculate, show, view
- **Human-in-loop:** True

### scientific/pydeseq2
- **Risk Factors:** remove, drop, execute, system, command, change, access, read, log, list, search, filter, sort, format, calculate, compute, show, view
- **Human-in-loop:** True

### scientific/gwas-database
- **Risk Factors:** system, update, alter, access, read, get, retrieve, query, log, list, search, filter, format, aggregate, view
- **Human-in-loop:** True

### scientific/bioservices
- **Risk Factors:** execute, eval, access, read, get, retrieve, query, email, log, list, search, format, view
- **Human-in-loop:** True

### scientific/scikit-bio
- **Risk Factors:** system, write, alter, access, sensitive, read, get, log, list, search, filter, format, calculate, view
- **Human-in-loop:** True

### scientific/gget
- **Risk Factors:** password, secret, credential, api_key, eval, command, update, change, access, sensitive, read, fetch, get, retrieve, query, email, log, list, search, filter, format, display, show, view
- **Human-in-loop:** True

### scientific/string-database
- **Risk Factors:** eval, system, write, read, get, retrieve, query, log, list, search, filter, format, show, view
- **Human-in-loop:** True

### scientific/literature-review
- **Risk Factors:** remove, execute, eval, system, write, access, read, fetch, get, retrieve, query, log, list, search, filter, sort, format, aggregate, show, view
- **Human-in-loop:** True

### scientific/pyhealth
- **Risk Factors:** drop, eval, system, access, read, get, log, monitor, search, filter, sort, format, view
- **Human-in-loop:** True

### scientific/offer-k-dense-web
- **Risk Factors:** system, get, search, view
- **Human-in-loop:** True

### scientific/qutip
- **Risk Factors:** truncate, destroy, system, read, track, list, search, format, compute, show, view
- **Human-in-loop:** True

### scientific/transformers
- **Risk Factors:** eval, access, read, get, log, search, format, compute, view
- **Human-in-loop:** True

### scientific/scholar-evaluation
- **Risk Factors:** eval, system, write, alter, access, personal, read, get, track, log, list, search, format, calculate, aggregate, view
- **Human-in-loop:** True

### scientific/cirq
- **Risk Factors:** drop, system, read, get, track, log, monitor, list, search, format, calculate, compute, display
- **Human-in-loop:** True

### scientific/uniprot-database
- **Risk Factors:** eval, system, alter, access, read, get, retrieve, query, log, list, search, filter, format, view
- **Human-in-loop:** True

### scientific/market-research-reports
- **Risk Factors:** financial, eval, system, write, change, access, read, get, track, log, list, search, format, show, view
- **Human-in-loop:** True

### scientific/torch_geometric
- **Risk Factors:** remove, drop, execute, eval, system, write, update, modify, read, get, message, log, list, search, filter, format, compute, aggregate, view
- **Human-in-loop:** True

### scientific/deepchem
- **Risk Factors:** drop, eval, access, read, get, message, log, list, search, format, view
- **Human-in-loop:** True

### scientific/reactome-database
- **Risk Factors:** eval, system, access, read, get, retrieve, query, log, list, search, format, compute, view
- **Human-in-loop:** True

### scientific/matlab
- **Risk Factors:** remove, execute, system, write, change, alter, read, search, filter, format, display
- **Human-in-loop:** True

### scientific/pathml
- **Risk Factors:** eval, access, read, get, log, search, format, view
- **Human-in-loop:** True

### scientific/omero-integration
- **Risk Factors:** delete, password, credential, eval, write, modify, access, permission, read, get, retrieve, query, list, search, filter, format, view
- **Human-in-loop:** True

### scientific/latex-posters
- **Risk Factors:** remove, system, command, write, alter, access, read, get, email, message, log, monitor, list, search, format, display, show, view, preview
- **Human-in-loop:** True

### scientific/zarr-python
- **Risk Factors:** credential, system, write, update, access, read, list, search, filter, format, compute, view
- **Human-in-loop:** True

### scientific/simpy
- **Risk Factors:** eval, system, read, get, track, log, monitor, search, filter, calculate, compute, view
- **Human-in-loop:** True

### scientific/pyopenms
- **Risk Factors:** system, modify, access, read, get, search, filter, format, view
- **Human-in-loop:** True

### scientific/pysam
- **Risk Factors:** execute, system, command, write, modify, access, read, fetch, get, query, track, search, filter, sort, format, calculate, view
- **Human-in-loop:** True

### scientific/matplotlib
- **Risk Factors:** remove, access, read, get, log, list, search, format, display, show, view
- **Human-in-loop:** True

### scientific/adaptyv
- **Risk Factors:** drop, credential, api_key, eval, change, access, webhook, read, get, track, search, filter, format
- **Human-in-loop:** True

### scientific/venue-templates
- **Risk Factors:** remove, eval, system, write, update, access, read, get, retrieve, query, email, log, list, search, sort, format, compute, show, view
- **Human-in-loop:** True

### scientific/clinical-reports
- **Risk Factors:** remove, drop, payment, eval, system, shell, write, change, alter, access, sensitive, read, email, notification, log, monitor, list, search, sort, format, show, view
- **Human-in-loop:** True

### scientific/scientific-slides
- **Risk Factors:** financial, api_key, system, write, update, modify, alter, access, personal, read, get, message, log, monitor, list, search, sort, format, compute, show, view
- **Human-in-loop:** True

### scientific/scientific-visualization
- **Risk Factors:** remove, truncate, command, write, update, change, access, read, get, list, search, format, compute, display, show, view
- **Human-in-loop:** True

### scientific/neuropixels-analysis
- **Risk Factors:** remove, command, alter, access, read, get, query, log, list, search, filter, sort, format, compute, view
- **Human-in-loop:** True

### scientific/hypogenic
- **Risk Factors:** eval, system, change, read, get, log, list, search, format, compute, view
- **Human-in-loop:** True

### scientific/openalex-database
- **Risk Factors:** eval, write, change, access, read, get, query, email, track, log, list, search, filter, sort, format, display, view
- **Human-in-loop:** True

### scientific/generate-image
- **Risk Factors:** remove, api_key, system, change, read, get, message, log, list, search, sort, format, view, preview
- **Human-in-loop:** True

### scientific/torchdrug
- **Risk Factors:** eval, access, read, get, query, log, list, search, filter, format, view
- **Human-in-loop:** True

### scientific/hypothesis-generation
- **Risk Factors:** eval, system, write, alter, access, read, fetch, get, log, monitor, search, format, summarize, show, view
- **Human-in-loop:** True

### scientific/datacommons-client
- **Risk Factors:** api_key, eval, access, read, fetch, get, retrieve, query, list, search, filter, format, aggregate, view
- **Human-in-loop:** True

### scientific/rdkit
- **Risk Factors:** remove, execute, system, write, change, alter, access, read, get, query, message, log, list, search, filter, sort, format, calculate, compute, display, show, view
- **Human-in-loop:** True

### scientific/stable-baselines3
- **Risk Factors:** truncate, eval, system, update, modify, access, read, get, log, monitor, list, search, format, compute, display, view
- **Human-in-loop:** True

### scientific/pylabrobot
- **Risk Factors:** drop, system, change, access, read, get, track, monitor, search, format, view
- **Human-in-loop:** True

### scientific/aeon
- **Risk Factors:** eval, change, read, get, log, search, format, show, view
- **Human-in-loop:** True

### scientific/modal
- **Risk Factors:** secret, credential, execute, system, write, update, change, authenticate, webhook, read, get, log, monitor, list, search, compute, view
- **Human-in-loop:** True

### scientific/pubmed-database
- **Risk Factors:** payment, api_key, eval, system, access, read, fetch, get, retrieve, query, email, alert, log, monitor, list, search, filter, format, calculate, display, view, preview
- **Human-in-loop:** True

### scientific/polars
- **Risk Factors:** drop, execute, eval, system, write, modify, read, get, query, list, search, filter, format, compute, view
- **Human-in-loop:** True

### scientific/statsmodels
- **Risk Factors:** drop, eval, alter, read, get, log, search, filter, sort, format, calculate, show, view
- **Human-in-loop:** True

### scientific/scanpy
- **Risk Factors:** remove, system, write, alter, access, read, get, log, search, filter, format, calculate, compute, show, view
- **Human-in-loop:** True

### scientific/astropy
- **Risk Factors:** system, write, modify, access, read, get, query, log, list, search, filter, sort, format, calculate, compute, aggregate, display, view
- **Human-in-loop:** True

### scientific/chembl-database
- **Risk Factors:** execute, eval, access, sensitive, read, get, retrieve, query, log, list, search, filter, format, view
- **Human-in-loop:** True

### scientific/clinicaltrials-database
- **Risk Factors:** eval, write, update, access, read, get, retrieve, query, email, track, monitor, search, filter, sort, format, summarize, view
- **Human-in-loop:** True

### scientific/ena-database
- **Risk Factors:** eval, command, access, read, get, retrieve, query, list, search, filter, format, view
- **Human-in-loop:** True

### scientific/pennylane
- **Risk Factors:** execute, system, access, read, get, log, monitor, search, compute, view
- **Human-in-loop:** True

### scientific/pufferlib
- **Risk Factors:** execute, eval, system, command, read, get, track, log, monitor, search, compute, view
- **Human-in-loop:** True

### scientific/pymoo
- **Risk Factors:** eval, access, read, get, search, show, view
- **Human-in-loop:** True

### scientific/dnanexus-integration
- **Risk Factors:** remove, credential, system, write, modify, access, authenticate, permission, read, get, message, log, monitor, search, filter, format, view
- **Human-in-loop:** True

### scientific/pdb-database
- **Risk Factors:** eval, write, access, read, fetch, get, retrieve, query, log, list, search, format, compute, display, view
- **Human-in-loop:** True

### scientific/opentargets-database
- **Risk Factors:** execute, eval, system, update, modify, access, read, get, retrieve, query, log, list, search, filter, sort, format, aggregate, view
- **Human-in-loop:** True

### scientific/scikit-learn
- **Risk Factors:** drop, truncate, eval, system, sensitive, read, get, log, list, search, format, view
- **Human-in-loop:** True

### scientific/etetoolkit
- **Risk Factors:** delete, eval, system, command, write, update, access, read, get, query, log, list, search, filter, format, calculate, compute, display, show, view
- **Human-in-loop:** True

### scientific/labarchive-integration
- **Risk Factors:** password, credential, eval, system, modify, alter, access, authenticate, authorize, permission, read, get, retrieve, email, analytics, track, log, list, search, format, view
- **Human-in-loop:** True

### scientific/peer-review
- **Risk Factors:** eval, system, write, access, personal, read, get, message, log, list, search, sort, format, summarize, show, view
- **Human-in-loop:** True

### scientific/cellxgene-census
- **Risk Factors:** system, change, access, sensitive, read, get, query, log, list, search, filter, format, calculate, view
- **Human-in-loop:** True

### scientific/latchbio-integration
- **Risk Factors:** drop, credential, system, command, write, update, access, permission, read, get, query, track, log, monitor, list, search, filter, format, view
- **Human-in-loop:** True

