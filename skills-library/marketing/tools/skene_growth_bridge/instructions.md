# Skene Growth Bridge

You bridge skene-growth analysis outputs to practical marketing execution. Use this skill when a skene-growth manifest, template, or product docs exist, or when a user wants marketing output informed by skene-growth data.

## Inputs to Look For

- `skene-context/growth-manifest.json`
- `skene-context/growth-template.json`
- `skene-context/product-docs.md`
- `skene-context/growth-objectives.md` (optional)
- `skene-context/skene-growth-plan.md` (optional)

If these files do not exist, recommend running:

```
uvx skene-growth analyze . --product-docs
```

## Workflow

1. **Summarize the product and audience**
   - Use product overview and features if available.
   - Clarify the primary user, job-to-be-done, and key outcome.

2. **Extract growth signals**
   - Top growth hubs (sorted by confidence).
   - High-priority GTM gaps.
   - Missing acquisition, activation, retention, or monetization loops.

3. **Map signals to skills**
   - Choose the most relevant marketing skills for the gaps and hubs.
   - Call the chosen skills directly (for example: `/copywriting`, `/page-cro`).

4. **Produce a marketing brief**
   - Provide a concise brief with recommended actions.
   - Include suggested experiments or content topics.

## Output Format

Provide the result in this structure:

```
## Skene Growth Summary
- Product:
- Audience:
- Top growth hubs:
- High-priority gaps:

## Recommended Skills
- Skill name: Why it applies

## Marketing Brief
- Objectives:
- Key messages:
- Experiments or content:
```

## Guardrails

- Do not invent data. If a field is missing, ask for it or state the assumption.
- Keep outputs actionable and scoped to the requested task.