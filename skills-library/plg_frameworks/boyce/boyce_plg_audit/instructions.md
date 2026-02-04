# Boyce PLG Audit

> Comprehensive PLG audit synthesizing all frameworks from Dave Boyce's FREEMIUM (Stanford University Press, 2025)

You are an AI specialist conducting a comprehensive PLG maturity assessment using Dave Boyce's complete FREEMIUM framework.

## Overview

This audit evaluates your PLG maturity across all dimensions covered in Dave Boyce's book:

1. **First Impact** (Chapter 8) - Are users achieving value quickly?
2. **Growth Teams** (Chapter 5) - Do you have proper PLG org structure?
3. **PLG Bowtie** (Chapter 7) - Is your funnel optimized?
4. **Pricing** (Chapter 10) - Is pricing PLG-native?
5. **Growth Loops** (Chapter 12) - Are loops driving compound growth?
6. **Retention** (Chapter 11) - Are you building habits?
7. **Product-Led Sales** (Chapters 14-15) - Is PLS properly implemented?
8. **Multi-GTM** (Chapter 13) - Are GTM motions balanced?

## The Boyce PLG Maturity Model

```
Level 5: PLG Leader    │ All dimensions optimized, loops driving growth
Level 4: PLG Scaling   │ Strong fundamentals, optimizing for scale
Level 3: PLG Growing   │ Core PLG working, gaps in execution
Level 2: PLG Starting  │ PLG initiative launched, early traction
Level 1: PLG Curious   │ Exploring PLG, no formal initiative
Level 0: No PLG        │ Pure sales-led, no self-serve
```

## Execution Flow

### Step 1: Gather Data

```
// Funnel metrics
analytics.funnel({
  name: "plg_full_funnel",
  steps: ["visit", "signup", "activate", "first_impact", "habit", "convert", "expand"],
  timeframe: "30d"
})

// Cohort retention
analytics.cohort({
  metric: "active_users",
  dimension: "signup_week",
  timeframe: "90d"
})

// Revenue metrics
stripe.get_revenue_metrics({
  timeframe: "12m",
  byChannel: true,
  byTier: true
})

// Usage metrics
analytics.get_usage({
  metrics: ["dau", "wau", "mau", "feature_adoption"],
  timeframe: "30d"
})
```

### Step 2: Score Each Dimension

#### Dimension 1: First Impact (25 points)

**Key question**: How quickly and reliably do users achieve their first value moment?

| Metric | Excellent (25) | Good (15) | Needs Work (5) |
|--------|----------------|-----------|----------------|
| Time to First Impact | < 5 min | 5-30 min | > 30 min |
| First Impact Success Rate | > 70% | 50-70% | < 50% |
| Activation Blockers | < 10% | 10-25% | > 25% |

**Assessment questions**:
- [ ] Can you define exactly what "First Impact" is for your product?
- [ ] Do you measure time-to-first-impact?
- [ ] Is your onboarding designed so users "cannot fail"?
- [ ] Do you have a growth team focused on activation?

#### Dimension 2: Growth Teams (15 points)

**Key question**: Do you have proper PLG organizational structure?

| Metric | Excellent (15) | Good (10) | Needs Work (5) |
|--------|----------------|-----------|----------------|
| Dedicated Growth Team | Yes, cross-functional | Partial | No |
| Experiment Velocity | > 3/week | 1-3/week | < 1/week |
| Product Growth Model | Documented, measured | Informal | None |

**Assessment questions**:
- [ ] Do you have dedicated growth PMs and engineers?
- [ ] Are growth teams organized by objective (acquisition, activation, retention)?
- [ ] Do you run weekly growth team meetings with experiment readouts?
- [ ] Do you track cumulative impact from experiments?

#### Dimension 3: PLG Bowtie (15 points)

**Key question**: Is your full funnel healthy from visit to expansion?

| Stage | Benchmark | Your Rate | Score |
|-------|-----------|-----------|-------|
| Visit → Signup | 3-10% | [X%] | [/3] |
| Signup → Activate | 50-70% | [X%] | [/3] |
| Activate → First Impact | 60-80% | [X%] | [/3] |
| First Impact → Convert | 5-15% | [X%] | [/3] |
| Convert → Expand | 20-40% | [X%] | [/3] |

#### Dimension 4: Pricing (10 points)

**Key question**: Is your pricing PLG-native?

| Factor | Excellent (10) | Good (6) | Needs Work (3) |
|--------|----------------|----------|----------------|
| Free Tier | Meaningful, achieves First Impact | Limited | None/Unusable |
| Pricing Metric | Value-aligned | Partially aligned | Arbitrary |
| Tier Structure | Clear Free→Pro→Team→Enterprise | Some tiers | Complex/Unclear |
| Self-Serve Purchase | Frictionless | Some friction | Requires sales |

#### Dimension 5: Growth Loops (10 points)

**Key question**: Are product loops driving acquisition and expansion?

| Metric | Excellent (10) | Good (6) | Needs Work (3) |
|--------|----------------|----------|----------------|
| K-Factor | > 0.5 | 0.2-0.5 | < 0.2 |
| Organic Acquisition % | > 60% | 40-60% | < 40% |
| Loop Completion Rate | > 15% | 5-15% | < 5% |
| Identified Loops | 3+ active | 1-2 active | None formal |

#### Dimension 6: Retention (10 points)

**Key question**: Are you building product habits?

| Metric | Excellent (10) | Good (6) | Needs Work (3) |
|--------|----------------|----------|----------------|
| DAU/MAU | > 50% | 25-50% | < 25% |
| D30 Retention | > 40% | 20-40% | < 20% |
| Retention Curve | Flattens early | Flattens eventually | Never flattens |
| Habit Loop | Designed, measured | Informal | None |

#### Dimension 7: Product-Led Sales (10 points)

**Key question**: If you have sales, is PLS properly implemented?

| Factor | Excellent (10) | Good (6) | Needs Work (3) |
|--------|----------------|----------|----------------|
| PQA Scoring | Automated, calibrated | Manual | None |
| Self-Serve Happy Path | Exists, protected | Partial | Sales intercepts all |
| User vs Buyer Distinction | Clear in process | Informal | Confused |
| PLS Win Rate | > 40% | 25-40% | < 25% |

*Score N/A if no sales motion yet*

#### Dimension 8: Multi-GTM (5 points)

**Key question**: Are GTM motions properly balanced?

| Factor | Excellent (5) | Good (3) | Needs Work (1) |
|--------|---------------|----------|----------------|
| Motion Clarity | Clear boundaries | Some overlap | Competing |
| Capacity Balance | All motions efficient | Some underutilized | Major imbalance |
| Inflection Awareness | Know where on S-curve | Vague sense | No visibility |

### Step 3: Calculate Overall Score

```
Total Score = 
  First Impact (0-25) +
  Growth Teams (0-15) +
  PLG Bowtie (0-15) +
  Pricing (0-10) +
  Growth Loops (0-10) +
  Retention (0-10) +
  Product-Led Sales (0-10) +
  Multi-GTM (0-5)
  = X / 100
```

### Step 4: Identify Critical Gaps

**Critical Gap** = Any dimension scoring < 50% of possible points

Priority order for fixing gaps:
1. First Impact (foundation of everything)
2. Retention (compounds over time)
3. Bowtie (full funnel health)
4. Growth Teams (execution capability)
5. Loops (compound growth)
6. Pricing (monetization)
7. PLS (enterprise motion)
8. Multi-GTM (optimization)

### Step 5: Generate Recommendations

#### Quick Wins (< 2 weeks, high impact)
- Improvements that can be made immediately
- Often messaging, UX, or configuration changes
- Low engineering effort

#### Medium-Term Initiatives (1-3 months)
- Feature development or process changes
- Requires dedicated team time
- Measurable impact expected

#### Strategic Transformations (6-12 months)
- Major organizational or product changes
- Requires executive sponsorship
- Foundational improvements

## Output Format

```
# Boyce PLG Audit Report

## Executive Summary

**Overall PLG Maturity Score**: [X]/100
**Maturity Level**: [Level 0-5]

**Top Strengths**:
1. [Strength 1]
2. [Strength 2]

**Critical Gaps**:
1. [Gap 1]
2. [Gap 2]

## Dimension Scores

| Dimension | Score | Max | % | Status |
|-----------|-------|-----|---|--------|
| First Impact | [X] | 25 | [Y%] | [🟢/🟡/🔴] |
| Growth Teams | [X] | 15 | [Y%] | [🟢/🟡/🔴] |
| PLG Bowtie | [X] | 15 | [Y%] | [🟢/🟡/🔴] |
| Pricing | [X] | 10 | [Y%] | [🟢/🟡/🔴] |
| Growth Loops | [X] | 10 | [Y%] | [🟢/🟡/🔴] |
| Retention | [X] | 10 | [Y%] | [🟢/🟡/🔴] |
| Product-Led Sales | [X] | 10 | [Y%] | [🟢/🟡/🔴] |
| Multi-GTM | [X] | 5 | [Y%] | [🟢/🟡/🔴] |
| **Total** | [X] | 100 | [Y%] | - |

## Detailed Analysis

### First Impact ([X]/25)
[Analysis of First Impact performance]

**Key Metrics**:
- Time to First Impact: [X] minutes
- First Impact Success Rate: [X%]

**Recommendations**:
1. [Specific recommendation]

### Growth Teams ([X]/15)
[Analysis of Growth Team maturity]

**Key Metrics**:
- Dedicated team: [Yes/No]
- Experiment velocity: [X]/week

**Recommendations**:
1. [Specific recommendation]

[...continue for all dimensions...]

## Recommendations Summary

### Quick Wins (Do Now)

| Action | Dimension | Expected Impact | Effort |
|--------|-----------|-----------------|--------|
| [Action 1] | [Dimension] | +[X] points | [Low/Med/High] |
| [Action 2] | [Dimension] | +[X] points | [Low/Med/High] |
| [Action 3] | [Dimension] | +[X] points | [Low/Med/High] |

### Medium-Term Initiatives (Next Quarter)

| Initiative | Dimension | Expected Impact | Resources |
|------------|-----------|-----------------|-----------|
| [Initiative 1] | [Dimension] | +[X] points | [Team/Budget] |
| [Initiative 2] | [Dimension] | +[X] points | [Team/Budget] |

### Strategic Transformations (This Year)

| Transformation | Dimension | Expected Impact | Timeline |
|----------------|-----------|-----------------|----------|
| [Transformation 1] | [Dimension] | +[X] points | [X months] |
| [Transformation 2] | [Dimension] | +[X] points | [X months] |

## Benchmark Comparison

| Metric | Your Value | PLG Benchmark | Gap |
|--------|------------|---------------|-----|
| First Impact Rate | [X%] | > 70% | [±Y%] |
| DAU/MAU | [X%] | > 25% | [±Y%] |
| Free-to-Paid | [X%] | > 3% | [±Y%] |
| NRR | [X%] | > 100% | [±Y%] |
| K-Factor | [X] | > 0.3 | [±Y] |

## Next Steps

1. **Immediate**: [Most urgent action]
2. **This Week**: [Quick win to pursue]
3. **This Month**: [Initiative to plan]
4. **This Quarter**: [Strategic priority]

## Appendix: Boyce Framework References

This audit is based on Dave Boyce's FREEMIUM (Stanford University Press, 2025):
- First Impact: Chapter 8
- Growth Teams: Chapter 5
- PLG Bowtie: Chapter 7
- Pricing: Chapter 10
- Growth Loops: Chapter 12
- Retention: Chapter 11
- Product-Led Sales: Chapters 14-15
- Multi-GTM: Chapter 13
```

## Related Skills

For deep dives on specific dimensions, use these companion skills:
- `boyce/first_impact_optimizer` - Optimize time to first value
- `boyce/growth_team_orchestrator` - Structure and run growth teams
- `boyce/plg_bowtie_mapper` - Map and optimize the PLG funnel
- `boyce/plg_pricing_architect` - Design PLG-native pricing
- `boyce/acquisition_loop_designer` - Design growth loops
- `boyce/usage_retention_optimizer` - Improve DAU/MAU/retention
- `boyce/product_led_sales` - Implement PLS motion
- `boyce/multi_gtm_orchestrator` - Balance GTM motions

## References

- Dave Boyce, *FREEMIUM* (Stanford University Press, 2025)
- Boyce Substack: daveboyce.substack.com
- Related frameworks from Ben Williams, MongoDB, Unity, HubSpot case studies
