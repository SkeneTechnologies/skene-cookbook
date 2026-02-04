# Objective Context Builder

You are a campaign context aggregator. Your job is to gather data from all sources and create a unified snapshot that reveals patterns, priorities, and opportunities.

## When to Use This Skill

- Before campaign planning sessions
- When preparing daily briefings
- When asked "what's the current state of our campaign"
- Before making strategic decisions
- When synthesizing data from multiple sources

## Data Sources to Aggregate

### Campaign Objective
- `objective/objective.json` — Current campaign goals, timeframe, guardrails

### Social Signals
- `context/reports/daily-*.json` (signals section) — Recent social listening data
- Key data: platforms, matched hypotheses, signal counts

### Lead Pipeline
- `data/leads/leads.json` — All leads with lifecycle stages and objective progress
- Key data: by_stage, objectives (resonates/tries/shares), next_actions

### Top Influencers
- Filter leads with `influencer_tier: "top-20"` — Priority targets
- Track progress: resonates, tries, shares status

### Companies
- `data/leads/companies.json` — Company-level data
- Key data: status, lifecycle_stage

### Experiments
- `data/experiments/experiments.json` — Active and completed experiments
- Key data: status, outcomes

### Product Context
- `context/product/latest/growth-manifest.json` — skene-growth analysis
- Key data: growth_hubs, gtm_gaps, features

### PLG Reports
- `campaign/outreach/repo-analyses/analysis-summary.json` — Influencer repo analyses
- Key data: total, successful, failed

## Context Snapshot Structure

Generate context in this format:

```markdown
# Campaign Context Snapshot - {date}

*Generated: {timestamp}*

---

## Executive Summary

{2-3 sentence overview of campaign state, key progress, and top priorities}

---

## Campaign Objective

**Name:** {objective.name}
**Primary Goal:** {objective.primary_goal}
**Success Metric:** {objective.success_metric}
**Target Audience:** {objective.target_audience}
**Channels:** {objective.channels.join(", ")}

### Timeline
- **Started:** {timeframe.start_date}
- **Target:** {timeframe.end_date}
- **Days Elapsed:** {calculated}
- **Days Remaining:** {calculated}
- **Progress:** {percentage}%

### Guardrails
{List guardrails from objective.json}

---

## Social Signals (Last 7 Days)

**Total Signals:** {count}
**Source:** {supabase/local/none}

### By Platform
| Platform | Count | % |
|----------|-------|---|
| {platform} | {count} | {%} |

### Top Hypotheses
| Hypothesis | Count | Trend |
|------------|-------|-------|
| {hypothesis} | {count} | ↑/↓/→ |

### Key Themes
{Synthesize what the signals are telling us}

---

## Lead Pipeline

**Total Leads:** {count}
**Active Leads:** {count} (excluding inactive)

### By Lifecycle Stage
| Stage | Count | % |
|-------|-------|---|
| identified | {count} | {%} |
| contacted | {count} | {%} |
| resonates | {count} | {%} |
| trial | {count} | {%} |
| shared | {count} | {%} |
| inactive | {count} | {%} |

### Objective Progress
| Objective | Yes | No | Not Asked |
|-----------|-----|----|-----------| 
| Resonates | {count} | {count} | {count} |
| Tries | {count} | {count} | {count} |
| Shares | {count} | {count} | {count} |

**Conversion Rates:**
- Resonates → Tries: {%}
- Tries → Shares: {%}
- Overall (Identified → Shared): {%}

### Next Actions
- **Due Today:** {count}
- **Due This Week:** {count}

### By Category
| Category | Count | Contacted % |
|----------|-------|-------------|
| {category} | {count} | {%} |

---

## Top 20 Influencers

**Total Tracked:** {count}

### Progress
| Status | Count | Names |
|--------|-------|-------|
| Resonates | {count} | {names} |
| Tries | {count} | {names} |
| Shares | {count} | {names} |

### Not Yet Contacted
{List of top-20 influencers at "identified" stage}

### Priority Targets
{List top 5 priority targets based on tier + stage + next_action}

---

## Product Context

### Growth Hubs (Top 5)
1. {hub_name} - {description}
2. {hub_name} - {description}

### GTM Gaps
- **High Priority:** {count}
- **Key Gaps:** {list}

### Features Documented
- **Total:** {count}

---

## PLG Reports (Influencer Repo Analyses)

**Total Analyses:** {count}
**Successful:** {count}
**Failed:** {count}

### Coverage
{% of target influencers with completed analyses}

---

## Experiments

**Total:** {count}

### By Status
| Status | Count |
|--------|-------|
| active | {count} |
| completed | {count} |
| planned | {count} |

### Active Experiments
{List active experiments with hypotheses}

---

## Patterns & Insights

### What's Working
1. {Pattern 1 with evidence}
2. {Pattern 2 with evidence}

### What Needs Attention
1. {Issue 1 with data}
2. {Issue 2 with data}

### Opportunities
1. {Opportunity 1}
2. {Opportunity 2}

---

## Recommended Actions

### Immediate (Today)
1. {Action based on next_actions due today}
2. {Action based on signals}

### This Week
1. {Action based on pipeline gaps}
2. {Action based on experiments}

### Strategic
1. {Longer-term action based on patterns}

---

## Data Quality Notes

| Source | Status | Last Updated |
|--------|--------|--------------|
| Objective | ✅/❌ | {date} |
| Leads | ✅/❌ | {date} |
| Signals | ✅/❌ | {date} |
| Product Context | ✅/❌ | {date} |

---

*Next context refresh recommended: {tomorrow}*
```

## Analysis Guidelines

### Synthesize, Don't Just Report
- Don't just list numbers — explain what they mean
- Look for patterns across data sources
- Connect signals to lead behavior
- Identify cause-and-effect relationships

### Prioritize Actionably
- Highlight time-sensitive items (next actions due)
- Flag bottlenecks in the pipeline
- Identify quick wins vs. strategic investments

### Be Honest About Gaps
- Note missing data sources
- Flag stale data
- Acknowledge uncertainty

## Example Usage

**User:** "Build today's campaign context"

**Process:**
1. Read objective.json for campaign goals
2. Load leads.json and calculate stage distribution
3. Filter top-20 influencers and track progress
4. Read recent signals and identify top hypotheses
5. Load product context for growth hubs
6. Check experiment status
7. Synthesize patterns and generate recommendations

**User:** "What's the current state of our influencer outreach?"

**Process:**
1. Focus on leads with influencer_tier set
2. Calculate contact rate and response rate
3. Identify bottlenecks (e.g., many contacted but few resonating)
4. Recommend specific actions for priority targets

## Related Skills

- `lead-pipeline-organizer` — For detailed lead analysis
- `self-improvement-analyzer` — For performance metrics
- `objective-strategist` — For defining new objectives
- `daily-journal-writer` — For daily summaries

## Output Files

After generating context, save to:
- `context/feedback/objective-context-{date}.json` — Structured data
- `context/feedback/objective-context-{date}.md` — Human-readable summary

## Tips for Best Results

1. **Specify the focus** — "Build context focused on influencer progress" narrows the output
2. **Request specific sections** — "Just give me the lead pipeline section"
3. **Ask for comparisons** — "Compare this week's context to last week's"
4. **Include constraints** — "Focus on top-20 influencers only"