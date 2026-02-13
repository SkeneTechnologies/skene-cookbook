# What are skills?

## The problem skills solve

When you ask an AI assistant (like Claude in your terminal, or the AI in Cursor) to do something — say, "score this lead" or "write a churn-risk summary" — the AI does its best with whatever it already knows. Sometimes that's fine. But if you need it to follow a specific method, use particular criteria, or produce a consistent format every time, you're stuck re-explaining the same instructions over and over. And the results vary.

A **skill** fixes that. It's a written-down method — a file the AI reads — so it knows _how_ you want something done before you even ask. Instead of explaining "here's how we score leads, here are the five criteria, here's the format" every session, that method lives in a skill file. The AI picks it up automatically.

Think of it this way: without a skill, the AI is improvising. With a skill, it's following your playbook.

---

## What a skill actually is

A skill is a small folder containing a few plain files:

```
churn_prediction/
├── skill.json          # name, description, when to use it
├── instructions.md     # the step-by-step method the AI follows
└── metadata.yaml       # optional: tags, security notes, integrations
```

**`instructions.md`** is the important one. It's a Markdown file that tells the AI what to do, step by step. It might say: "When someone asks about churn risk, gather these data points, apply these criteria, and produce a summary in this format." The AI reads it and follows it.

**`skill.json`** is metadata — the skill's name, a short description, and triggers (keywords or situations that tell the AI "this skill applies here").

**`metadata.yaml`** is optional. It adds things like security classification or integration references if the skill connects to external tools.

That's it. A skill is just instructions in a file, organized so the AI can find and follow them.

---

## How you actually use one

### 1. Install

```bash
npm install @skene/skills-directory
```

This places skill files where your AI tool looks for them:

- **Cursor** reads from `~/.cursor/skills/`
- **Claude** reads from `~/.claude/skills/`

After install, the skills are there. You don't need to configure anything else.

### 2. Ask the AI to do something the skill covers

If you installed a lead-scoring skill and you say "score this lead," the AI recognizes the situation, reads the skill's instructions, and follows the method described there. You get consistent output — the same criteria, the same format — every time.

You don't need to reference the skill by name. The AI matches your request to the right skill based on the triggers and description in `skill.json`.

### 3. That's it

There's no runtime, no API, no deployment step. Skills are files the AI reads. If the file is in the right folder, the AI uses it. If you remove the file, it stops.

---

## A concrete example

Say you work in customer success and you want the AI to help you spot accounts that might churn.

Without a skill, you'd type something like: "Look at this account data and tell me if they're at risk of churning. Consider usage trends, support tickets, NPS, contract renewal date..." — and you'd do this every time, slightly differently, getting slightly different results.

With the **churn_prediction** skill installed, you just say: "Is this account at risk?" The AI reads the skill's instructions, which define exactly which signals to look at (usage drop, support volume, NPS trend, days to renewal), how to weight them, and what format to return. You get the same structured assessment every time.

---

## Skills vs recipes

A **skill** handles one task. A **recipe** (also called a skill chain) combines several skills into a multi-step workflow.

|            | What it is                     | Example                            |
| :--------- | :----------------------------- | :--------------------------------- |
| **Skill**  | Instructions for one task      | "Score this lead"                  |
| **Recipe** | A workflow chaining 2–7 skills | "Qualify → score → route → notify" |

If you need one thing done, use a skill. If you need a sequence of steps that flow into each other, use a recipe. The [Skill Chain Cookbook](SKILL_CHAINS.md) has 36 recipes ready to copy.

You can also build your own recipe by picking skills from the [directory](directory.md) and deciding the order.

---

## When skills help and when they don't

### Skills help when…

- **You repeat the same kind of task** — lead scoring, ticket classification, churn checks, content drafts — and want consistent results without re-explaining the method each time.
- **You want the AI to follow your process**, not just its general training. For example, your company scores leads on five specific criteria; a skill encodes those criteria.
- **Multiple people need the same method.** Install the skills library and everyone's AI follows the same playbook.
- **You're building a workflow** and want to combine defined steps. Skills are composable — you can chain them.

### Skills probably don't help when…

- **You have a one-off question** that doesn't need a repeatable method. Just ask the AI directly.
- **You need something the AI can't do** (like access a live database). Skills are instructions, not integrations — though they can reference integrations.
- **You want a complete, ready-to-run workflow** — in that case, start with a [recipe](SKILL_CHAINS.md) instead of assembling skills yourself.

---

## What's in the library

This repo includes **764 skills** across 23 domains:

- **Sales & RevOps** — lead scoring, deal inspection, pipeline forecasting
- **Customer Success** — health scoring, churn prediction, expansion triggers
- **Marketing & Growth** — content, SEO, campaigns, A/B testing, onboarding
- **Finance** — ARR tracking, burn rate, scenario planning
- **Product & Engineering** — experimentation, security review, API management
- **Compliance & Security** — GDPR, SOC 2, access review, PII detection
- **And more** — HR, data ops, developer experience, research tools

[Browse the full directory →](directory.md)

---

## Where to go from here

| You want to…                        | Go here                                              |
| :---------------------------------- | :--------------------------------------------------- |
| See a working workflow right away   | [Skill Chain Cookbook (36 recipes)](SKILL_CHAINS.md) |
| Browse all 764 skills by domain     | [Skills Directory](directory.md)                     |
| Get something running in 15 minutes | [Quick Wins](QUICK_WINS.md)                          |
| Create your own skill               | [Build Your First Skill](BUILD_YOUR_FIRST_SKILL.md)  |
| Understand how the system is built  | [Architecture](../ARCHITECTURE.md)                   |
