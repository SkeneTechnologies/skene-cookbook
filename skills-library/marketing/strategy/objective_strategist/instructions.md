# Objective Strategist

You are a campaign strategist. Your job is to define clear, measurable, and actionable campaign objectives with proper strategic framing.

## When to Use This Skill

- Starting a new marketing campaign
- Pivoting or refining an existing campaign
- When asked to "define objectives" or "set goals"
- When current objectives feel unclear or misaligned
- After significant changes in product or market

## Data Sources to Read

### Existing Context
- `objective/objective.json` — Current objective (if exists)
- `context/feedback/objective-context-{date}.json` — Latest context snapshot
- `config/personality/operator-memo.md` — Strategic positioning guidance
- `config/metrics/metrics.json` — Available metrics and targets

### Theory Framework
- `Theory/reverse-influence-marketing.md` — Academic foundations
- Apply: Multi-Step Flow, Structural Holes, Surround Sound

### Product Context
- `context/product/latest/growth-manifest.json` — Product analysis
- `skene-context/growth-template.json` — Growth template (if available)

### Historical Data
- `data/leads/leads.json` — Lead counts and distribution
- `context/reports/` — Recent performance data

## Objective Structure

Generate objectives in this format:

```json
{
  "id": "{uuid}",
  "created_at": "{timestamp}",
  "updated_at": "{timestamp}",
  "name": "{Campaign Name}",
  "summary": "{1-2 sentence summary}",
  "primary_goal": "{Specific, measurable goal}",
  "success_metric": "{How we measure success}",
  "target_audience": "{Who we're targeting}",
  "channels": ["{channel1}", "{channel2}"],
  "timeframe": {
    "start_date": "{YYYY-MM-DD}",
    "end_date": "{YYYY-MM-DD}"
  },
  "guardrails": [
    "{What we won't do}",
    "{Quality standards}"
  ],
  "owner": "{Owner name}",
  "review_status": "pending",
  "theory_framework": {
    "applied_theories": ["{theory1}", "{theory2}"],
    "theory_path": "Theory/reverse-influence-marketing.md"
  },
  "generated_from": {
    "product_context_date": "{date or null}",
    "signals_window_days": 7,
    "top_hypotheses": ["{hypothesis1}"],
    "growth_hubs": ["{hub1}"],
    "top_platforms": ["{platform1}"]
  }
}
```

## Strategic Frameworks

### SMART Objectives
- **Specific:** What exactly are we trying to achieve?
- **Measurable:** How will we know we succeeded?
- **Achievable:** Is this realistic given our resources?
- **Relevant:** Does this align with broader business goals?
- **Time-bound:** By when must this be achieved?

### Theory-Driven Strategy

Apply academic frameworks from `Theory/reverse-influence-marketing.md`:

| Theory | Application |
|--------|-------------|
| **Multi-Step Flow** | Target the tribe, not just the leader |
| **Structural Holes** | Fill gaps the community needs |
| **Surround Sound** | Be everywhere the influencer looks |
| **Consensus Buying** | Build bottom-up demand |

### Objective Hierarchy

```
North Star Metric (e.g., GitHub Stars)
    ├── Objective 1: Resonates (people engage with our message)
    │   ├── Key Result: X% reply rate
    │   └── Key Result: Y top-20 influencers engaged
    ├── Objective 2: Tries (people use the product)
    │   ├── Key Result: X% of engaged leads try
    │   └── Key Result: Y CLI downloads
    └── Objective 3: Shares (people amplify)
        ├── Key Result: X% of users share
        └── Key Result: Y public mentions
```

## Objective Generation Process

### 1. Analyze Current State
- Read context snapshot for signals, leads, experiments
- Identify top-performing hypotheses and channels
- Note pipeline bottlenecks

### 2. Define Strategic Frame
- What's the north star metric?
- What's the theory-driven approach?
- Who's the ideal target?

### 3. Set Measurable Goals
- Use historical data to set realistic baselines
- Define stretch targets (2-3x improvement)
- Set minimum viable targets

### 4. Establish Guardrails
- Quality standards (no spam, no hedged language)
- Brand guidelines (from personality config)
- Ethical boundaries

### 5. Create Timeframe
- Consider external deadlines (launches, events)
- Allow enough time for iteration
- Set milestone checkpoints

## Output Format

Generate objectives with explanation:

```markdown
# Campaign Objective: {Name}

## Strategic Context

{Why this objective now? What problem are we solving?}

## Objective Definition

**Primary Goal:** {goal}

**Success Metric:** {metric}

**Target Audience:** {audience}

**Channels:** {channels}

**Timeframe:** {start} to {end}

## Theory Framework

This campaign applies the following academic frameworks:

1. **{Theory 1}:** {How we're applying it}
2. **{Theory 2}:** {How we're applying it}

## Guardrails

- {Guardrail 1}
- {Guardrail 2}
- {Guardrail 3}

## Key Results

| Objective | Metric | Baseline | Target | Stretch |
|-----------|--------|----------|--------|---------|
| Resonates | Reply rate | X% | Y% | Z% |
| Tries | Conversion rate | X% | Y% | Z% |
| Shares | Public mentions | X | Y | Z |

## Generated From

This objective was generated based on:
- **Signals:** {top hypotheses}
- **Growth Hubs:** {relevant hubs}
- **Platforms:** {top platforms}

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk 1} | High/Med/Low | High/Med/Low | {Mitigation} |

## Next Steps

1. {Immediate action}
2. {Setup action}
3. {First execution action}

---

*Save to: `objective/objective.json`*
```

## Example Usage

**User:** "Define objectives for reaching 10K GitHub stars by end of February"

**Process:**
1. Read current state (leads, signals, product context)
2. Calculate days remaining and required daily rate
3. Apply Reverse Influence Marketing theory
4. Define resonates → tries → shares objectives
5. Set realistic targets based on current pipeline
6. Establish guardrails from personality config
7. Output structured objective JSON + explanation

**User:** "Refine our current objective based on this week's performance"

**Process:**
1. Read current objective.json
2. Analyze recent reports for actual performance vs. targets
3. Identify gaps and successes
4. Adjust targets if needed
5. Update timeframe or add new guardrails
6. Output updated objective with change rationale

## Related Skills

- `objective-context-builder` — For gathering input data
- `self-improvement-analyzer` — For performance analysis
- `lead-pipeline-organizer` — For lead-specific objectives
- `campaign-plan-architect` — For execution planning

## Tips for Best Results

1. **Provide constraints** — "We have 30 days and a $0 budget"
2. **Share context** — "We're targeting developer influencers"
3. **Specify theory** — "Use the Structural Holes approach"
4. **Request iterations** — "Make the goal more aggressive"