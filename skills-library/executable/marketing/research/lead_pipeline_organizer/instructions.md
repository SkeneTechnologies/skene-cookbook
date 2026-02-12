# Lead Pipeline Organizer

Organizes leads and pipeline according to campaign objectives. Analyzes lead progress against objectives, prioritizes leads based on objective alignment, creates pipeline views organized by stages, and suggests next actions to move leads through the funnel.

## When to Use This Skill

- Organizing leads according to campaign objectives
- Prioritizing leads based on objective progress
- Creating pipeline views organized by objective stages
- Identifying which leads need attention for each objective
- Planning outreach based on objective alignment
- Analyzing pipeline health against objectives
- Finding leads stuck at specific stages

## What This Skill Does

1. **Reads Campaign Objectives**: Loads `objective/objective.json` to understand campaign goals
2. **Analyzes Lead Progress**: Reviews `data/leads/leads.json` to see current objective status
3. **Organizes by Objectives**: Groups leads by objective progress (resonates, tries, shares)
4. **Prioritizes Leads**: Ranks leads based on:
   - Objective alignment
   - Lifecycle stage
   - Influencer tier
   - Next action timing
   - Engagement signals
5. **Creates Pipeline Views**: Organizes leads by lifecycle stages and objective progress
6. **Suggests Next Actions**: Recommends specific actions to advance leads toward objectives

## How to Use

### Basic Usage

```
Organize my leads according to the current objective
```

```
Show me the pipeline organized by objective progress
```

### With Specific Focus

```
Prioritize leads that haven't resonated yet
```

```
Show me leads ready to try but haven't shared
```

```
Find leads stuck at the contacted stage
```

### Advanced Usage

```
Analyze pipeline health against objectives and suggest top 10 actions
```

```
Create a prioritized outreach list for the resonates objective
```

## Instructions

When a user requests lead/pipeline organization:

1. **Load Campaign Objective**
   - Read `objective/objective.json` to understand:
     - Primary goal and success metrics
     - Target audience
     - Objectives (resonates, tries, shares)
     - Timeframe and deadlines
   - If objective.json doesn't exist, check for `data/leads/lifecycle.json` for default objectives

2. **Load Lead Data**
   - Read `data/leads/leads.json` to get all leads
   - Read `data/leads/lifecycle.json` to understand stage definitions
   - Read `data/leads/companies.json` if company context is needed

3. **Analyze Objective Progress**
   - For each objective (resonates, tries, shares), count leads:
     - Status: "yes", "no", "not_asked", or undefined
     - Lifecycle stage alignment
     - Time since last action
   - Calculate conversion rates between objectives
   - Identify bottlenecks in the funnel

4. **Organize by Pipeline Stages**
   - Group leads by lifecycle_stage:
     - identified: Not yet contacted
     - contacted: Initial outreach sent
     - resonates: Confirmed message resonates
     - trial: Tried the product/tool
     - shared: Shared publicly
     - inactive: Not responsive or opted out
   - Within each stage, sort by:
     - Priority rank (if exists)
     - Influencer tier (top-20 first)
     - Next action timing (soonest first)
     - Last engagement date

5. **Prioritize Leads**
   - High Priority:
     - Top-20 influencers not yet contacted
     - Leads with next_action_at in next 1-2 days
     - Leads at "resonates" but not "tries"
     - Leads at "tries" but not "shares"
   - Medium Priority:
     - Leads contacted but no response
     - Leads with partial objective progress
   - Low Priority:
     - Inactive leads
     - Leads with all objectives complete

6. **Create Pipeline Views**

   Organize output in clear sections:

   ```markdown
   # Pipeline Overview: [Objective Name]
   
   ## Objective Progress
   - Resonates: [X] yes | [Y] no | [Z] not_asked
   - Tries: [X] yes | [Y] no | [Z] not_asked  
   - Shares: [X] yes | [Y] no | [Z] not_asked
   
   Conversion Rates:
   - Resonates → Tries: [X%]
   - Tries → Shares: [X%]
   - Overall: [X%]
   
   ## Pipeline by Stage
   
   ### Identified ([X] leads)
   [List top priority leads with next actions]
   
   ### Contacted ([X] leads)
   [Leads awaiting response or follow-up]
   
   ### Resonates ([X] leads)
   [Leads who resonated but haven't tried]
   
   ### Trial ([X] leads)
   [Leads who tried but haven't shared]
   
   ### Shared ([X] leads)
   [Leads who completed all objectives]
   
   ### Inactive ([X] leads)
   [Leads marked inactive]
   
   ## Priority Actions
   
   ### High Priority (Next 1-2 Days)
   [List with next_action, next_action_at, reason]
   
   ### Medium Priority (This Week)
   [List with suggested actions]
   
   ## Recommendations
   - Focus areas for this week
   - Bottlenecks to address
   - Quick wins available
   ```

7. **Suggest Next Actions**
   - For each priority lead, suggest:
     - Specific action (e.g., "follow_up_value", "ask_to_try", "ask_to_share")
     - Timing (based on next_action_at or last touch)
     - Channel (email, LinkedIn, X)
     - Reason for the action
   - Consider:
     - Last outreach date and response
     - Objective gaps
     - Influencer tier
     - Category/segment

8. **Identify Opportunities**
   - Find leads ready to advance:
     - Resonates=yes but tries=not_asked → Ask to try
     - Tries=yes but shares=not_asked → Ask to share
     - Contacted but no engagement → Follow up with value
   - Find stuck leads:
     - Long time at same stage
     - No next_action set
     - Missing objective progress

## Output Format

Provide results in this structure:

```markdown
# Lead Pipeline: [Campaign Name]

**Objective**: [Primary goal from objective.json]
**Timeframe**: [Start date] to [End date]
**Target**: [Success metric]

---

## Pipeline Health

**Total Leads**: [X]
**Active Leads**: [Y] (excluding inactive)

### Objective Progress
| Objective | Yes | No | Not Asked | Conversion |
|-----------|-----|----|-----------|-----------| 
| Resonates | [X] | [Y] | [Z] | [%] |
| Tries     | [X] | [Y] | [Z] | [%] |
| Shares    | [X] | [Y] | [Z] | [%] |

**Bottlenecks**: [Identify where leads are getting stuck]

---

## Pipeline by Stage

### 🎯 Identified ([X] leads)
*Not yet contacted*

**Top Priority**:
1. [Name] - [Company] - [Category]
   - Next: [Action] by [Date]
   - Reason: [Why]
   - Notes: [Key context]

[Repeat for top 5-10]

---

### 📧 Contacted ([X] leads)
*Initial outreach sent*

**Needs Follow-up**:
1. [Name] - Last contacted: [Date]
   - Status: [Opened/Clicked/No engagement]
   - Next: [Action] by [Date]
   - Suggested: [Specific action]

---

### ✅ Resonates ([X] leads)
*Confirmed message resonates*

**Ready to Try**:
1. [Name] - Resonated on [Date]
   - Next: Ask to try
   - Suggested timing: [Date]
   - Channel: [Email/LinkedIn/X]

---

### 🚀 Trial ([X] leads)
*Tried the product*

**Ready to Share**:
1. [Name] - Tried on [Date]
   - Next: Ask to share
   - Suggested timing: [Date]
   - Channel: [Email/LinkedIn/X]

---

### 🎉 Shared ([X] leads)
*Completed all objectives*

[Optional: List champions for reference]

---

## Priority Actions (Next 7 Days)

### Today/Tomorrow
1. **[Name]** - [Action]
   - Objective: [resonates/tries/shares]
   - Channel: [Email/LinkedIn/X]
   - Reason: [Why now]
   - Template: [Suggested approach]

### This Week
[Additional priority actions]

---

## Recommendations

### Focus Areas
- [Specific area 1]: [Why and what to do]
- [Specific area 2]: [Why and what to do]

### Quick Wins
- [Opportunity 1]: [Action and expected outcome]
- [Opportunity 2]: [Action and expected outcome]

### Bottlenecks
- [Bottleneck 1]: [Issue and solution]
- [Bottleneck 2]: [Issue and solution]
```

## Examples

### Example 1: Basic Organization

**User**: "Organize my leads according to the current objective"

**Output**: 
- Reads objective.json (10k GitHub stars goal)
- Analyzes 2,685 leads
- Groups by lifecycle stage
- Shows objective progress (resonates: 12 yes, tries: 5 yes, shares: 2 yes)
- Prioritizes top-20 influencers not yet contacted
- Suggests next actions for each priority group

### Example 2: Focused Analysis

**User**: "Show me leads ready to try but haven't shared"

**Output**:
- Filters leads where tries=yes but shares≠yes
- Lists each lead with context
- Suggests personalized ask-to-share messages
- Recommends timing based on when they tried

### Example 3: Pipeline Health

**User**: "Analyze pipeline health and suggest top 10 actions"

**Output**:
- Calculates conversion rates
- Identifies bottlenecks (e.g., low resonates→tries conversion)
- Lists 10 highest-impact actions
- Prioritizes by objective alignment and timing

## Tips for Best Results

- **Run regularly**: Pipeline changes as outreach progresses
- **Focus on objectives**: Always tie actions back to campaign objectives
- **Consider timing**: Respect next_action_at dates
- **Prioritize influencers**: Top-20 tier leads get highest priority
- **Track conversions**: Monitor objective conversion rates over time
- **Update after outreach**: Run after sending messages to see new priorities

## Related Files

- `objective/objective.json` - Campaign objectives and goals
- `data/leads/leads.json` - All lead records with objective progress
- `data/leads/lifecycle.json` - Stage definitions
- `data/leads/companies.json` - Company context (optional)
- `scripts/leads/update-leads-from-outreach.ts` - Updates leads from analytics

## Related Skills

- **lead-research-assistant**: For finding new leads
- **email-sequence**: For creating follow-up sequences