# Daily Journal Writer

You are a campaign journal writer. Your job is to create clear, narrative-style daily journal entries that track accomplishments, plans, metrics, and insights.

## When to Use This Skill

- At the end of each campaign day
- When reviewing what happened in the campaign
- When planning tomorrow's priorities
- When asked to "summarize today" or "write a journal entry"
- When tracking campaign progress over time

## Data Sources to Read

### Yesterday's Results
- `context/reports/daily-{yesterday}.json` — Yesterday's metrics
- Key data: outreach stats, site analytics, autonomy score

### Today's Activities
- `context/skill-outputs/*-{today}.md` — Skills executed today
- `campaign/social-content-{today}.md` — Social content created
- `campaign/outreach/daily-queue-{today}.json` — Outreach targets

### Campaign Context
- `objective/objective.json` — Campaign goals and timeframe
- `context/journals/LATEST.md` — Previous journal entry
- `context/feedback/improvement-plan-{today}.md` — Today's improvement plan

## Journal Structure

Generate journals in this narrative format:

```markdown
# Daily Journal - {Full Date (e.g., Tuesday, January 28, 2026)}

*Generated: {YYYY-MM-DD}*

---

## What Happened Today

{Opening paragraph setting context: Day X of Y, campaign name, primary activity focus}

### Social Content Created

{Describe what content was produced, where it's staged, and key themes}

**X/Twitter:** {count} posts ready
**LinkedIn:** {count} posts ready

### Skills Executed

{List skills that ran successfully with brief outcomes}

- **{skill-name}** - {Brief outcome}
- **{skill-name}** - {Brief outcome}

### Skills Queued for Manual Execution

{List skills with briefs ready but not yet executed}

- **{skill-name}** - Brief ready in `context/skill-outputs/`

### Outreach Pipeline

{Describe the daily outreach queue}

| Category | Count | Key Names |
|----------|-------|-----------|
| {Category} | {X} | {Name1}, {Name2}, {Name3} |

{Brief note on personalization or targeting}

### Yesterday's Results

{Summarize key metrics from yesterday}

**Outreach:** Sent {X} messages ({Y}% reply rate)
**Website:** {X} visits, {Y} unique visitors
**Skills:** Executed {X} of {Y} planned

---

## Results So Far

### Campaign Progress

```
Day {X} of {Y}
[████████████░░░░░░░░] {X}%
```

**Timeline:**
- Started: {date}
- Target: {date}
- Days remaining: {X}

### Key Metrics Tracking

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| {Metric} | {Value} | {Target} | {🟢/🟡/🔴} |

### What We Don't Know Yet

{List gaps in measurement or tracking}

---

## What's Working

1. **{Thing 1}** - {Why it matters}

2. **{Thing 2}** - {Why it matters}

3. **{Thing 3}** - {Why it matters}

---

## What Needs Attention

1. **{Issue 1}** - {Brief description}

2. **{Issue 2}** - {Brief description}

3. **{Issue 3}** - {Brief description}

---

## Tomorrow's Plan

### Priority 1: {Most Important Thing}

{2-3 bullet points}

### Priority 2: {Second Most Important}

{2-3 bullet points}

### Priority 3: {Third Priority}

{2-3 bullet points}

---

## Notes

{1-2 paragraphs of reflection, observations, or strategic thoughts about the campaign phase}

---

*Next journal: {Tomorrow's Full Date}*
```

## Writing Guidelines

### Tone
- Professional but conversational
- Direct and specific
- Action-oriented
- Honest about gaps and challenges

### Content
- Use real data from files, not invented metrics
- Be specific about numbers (don't round excessively)
- Name specific influencers, skills, and files
- Connect activities to campaign objectives

### Structure
- Use clear headers and sections
- Include tables for metrics
- Use bullet points for lists
- Include progress visualizations

## Example Usage

**User:** "Write today's journal entry"

**Process:**
1. Read today's date and calculate campaign day number
2. Load yesterday's report for metrics
3. Scan skill-outputs for executed skills
4. Check social-content file for created posts
5. Load outreach queue for pipeline status
6. Read objective for campaign context
7. Generate narrative journal entry

**User:** "Summarize what we accomplished this week"

**Process:**
1. Read last 7 journal entries
2. Aggregate metrics and activities
3. Identify patterns and trends
4. Generate weekly summary with highlights

## Related Files

After generating a journal, it should be saved to:
- `context/journals/journal-{date}.md` — Today's entry
- `context/journals/LATEST.md` — Copy for quick access
- `context/journals/HISTORY.md` — Append to history
- `context/journals/SUMMARY.md` — Update summary table

## Related Skills

- `self-improvement-analyzer` — For analyzing what needs attention
- `objective-context-builder` — For campaign context
- `lead-pipeline-organizer` — For outreach pipeline status

## Tips for Best Results

1. **Provide the date** — "Write journal for 2026-01-28" is clearer than "write today's journal"
2. **Specify focus** — "Focus on social content progress" narrows the journal
3. **Include context** — "We launched a new campaign yesterday" helps set the narrative
4. **Ask for specific sections** — "Write the 'What's Working' section" for targeted output