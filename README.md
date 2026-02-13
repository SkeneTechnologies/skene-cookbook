# When you need an AI workflow without building it from scratch

<p align="left">
  <a href="https://github.com/SkeneTechnologies/skene-cookbook/actions"><img src="https://github.com/SkeneTechnologies/skene-cookbook/workflows/Lint%20&%20Build%20Documentation/badge.svg" alt="GitHub Actions"></a>
  <a href="https://codecov.io/gh/SkeneTechnologies/skene-cookbook"><img src="https://codecov.io/gh/SkeneTechnologies/skene-cookbook/branch/main/graph/badge.svg" alt="Test Coverage"></a>
  <a href="CODE_OF_CONDUCT.md"><img src="https://img.shields.io/badge/code%20of%20conduct-contributor%20covenant-green.svg" alt="Code of Conduct"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://www.npmjs.com/package/@skene/skills-directory"><img src="https://img.shields.io/npm/v/@skene/skills-directory.svg" alt="npm version"></a>
</p>

<p align="left">
  <a href="docs/SKILL_CHAINS.md"><img src="https://img.shields.io/badge/recipes-36%20Skill%20Chains-blue" alt="Skill Chain Recipes"></a>
  <a href="METRICS.md"><img src="https://img.shields.io/badge/skills-764%20ingredients-green" alt="Skills (ingredients)"></a>
  <a href="METRICS.md"><img src="https://img.shields.io/badge/executable-382-orange" alt="Executable"></a>
  <a href="METRICS.md"><img src="https://img.shields.io/badge/domains-23-purple" alt="Domains"></a>
</p>

If you're trying to ship something like lead scoring, churn alerts, or a content pipeline without months of custom agent code, this repo is a **cookbook of 36 recipes** (skill chains) and **764 skills** you can copy and adapt. Pre-built workflows and skills for Cursor and Claude; install via npm, pick a recipe, and wire your data. New to skills? [What are skills?](docs/WHAT_ARE_SKILLS.md)

[**Browse Skill Chain Recipes**](docs/SKILL_CHAINS.md) • [**Playbooks & Data to Wire**](docs/PLAYBOOKS.md) • [**Explore the Directory**](docs/directory.md) • [**View Metrics**](METRICS.md) • [**Quick Start**](#-quick-start)

---

## Choose your path

_Guides by role — pick the one that matches your situation._

| Role                | When this fits you                                                      | Get started                                   |
| :------------------ | :---------------------------------------------------------------------- | :-------------------------------------------- |
| 👔 **Sales Leader** | You own pipeline and want AI qualification without a big build          | [View guide →](docs/personas/sales-leader.md) |
| 🚀 **Growth PM**    | You're improving activation and want flows for onboarding or engagement | [View guide →](docs/personas/growth-pm.md)    |
| 🔬 **Researcher**   | You need scientific tools and data analysis in your workflow            | [View guide →](docs/personas/researcher.md)   |
| 💼 **Finance/CFO**  | You need financial intelligence and reporting, not custom models        | [View guide →](docs/personas/cfo.md)          |

Or [browse the Skill Chain Cookbook (36 recipes) →](docs/SKILL_CHAINS.md) · [browse 764 skills →](docs/directory.md)

---

## When this helps

You want a **multi-step workflow** (e.g. qualify → score → route) but don't want to design and maintain each step yourself. The cookbook gives you recipes; you copy one, point it at your CRM or data, and adjust. Skills are the building blocks; chains are the workflows that combine them.

- **Single steps vs workflows:** If you only need one-off prompts or single skills, you can use the skills library. If you need a repeatable flow (e.g. lead in → score → route → notify), the recipes are for that.
- **Starting from zero vs from a recipe:** Many teams build custom agents over several months. Here you start from a recipe and ship in days or weeks by wiring your data and tweaking prompts.
- **Generic vs domain:** Recipes are organized by domain (sales, churn, PLG, compliance, growth, etc.) so you can find something that matches what you're trying to do.

> **Example outcomes:** Teams use the sales recipe to automate lead scoring and routing (fewer manual touches). Finance recipes are used for burn and scenario modeling. Churn recipes flag at-risk accounts early. Growth recipes drive conversion and onboarding flows. [Full breakdown and numbers →](docs/VALUE.md)

---

## Installation

```bash
npm install @skene/skills-directory
```

### Auto-activation

Skills are installed to your environment during `npm install` and work with:

- **Cursor:** `~/.cursor/skills/`
- **Claude:** `~/.claude/skills/`

Install is skipped automatically in:

- CI/CD (e.g. GitHub Actions, CircleCI, Jenkins)
- Docker
- When you use `--ignore-scripts`

To skip manually (e.g. in CI or Docker):

```bash
SKIP_SKILLS_INSTALL=true npm install @skene/skills-directory
```

An `ECOSYSTEM.md` file is generated with suggestions for other Skene tools that fit your stack.

---

## What's included

If you'd rather **copy a recipe and plug in your CRM/Stripe/playbook** than build from scratch, start with the [Skill Chain Cookbook (36 recipes)](docs/SKILL_CHAINS.md). Each recipe chains 2–7 skills and is backed by a playbook (workflow blueprint) with ICP, integration references, and prompts — see [Playbooks](docs/PLAYBOOKS.md) and [registry/blueprints](registry/blueprints/).

<details open>
<summary><b>Skills library (764 total: 382 executable + 382 reference guides)</b></summary>

- **70 PLG:** Product-led growth, activation, onboarding.
- **52 Marketing:** Content, SEO, campaigns, analytics.
- **29 Customer Success:** Health scoring, churn prediction.
- **25 RevOps:** Sales pipeline, forecasting, GTM alignment.
- **20 Monetization:** Pricing, billing, revenue optimization.
- **19 AI Ops:** Automation and ML operations.
- **187 more:** Security, data ops, devex, finance, HR, and others.

[Executable skills breakdown →](METRICS.md#executable-skills-breakdown)

</details>

<details>
<summary><b>Reference guides & infrastructure (382)</b></summary>

- **241 Cursor rules:** IDE guidelines for 241+ frameworks.
- **141 Scientific:** Research tools, bioinformatics, data analysis.
- **Integrations:** 40+ standardized tools (CRM, analytics, billing).
- **Security:** Approval gates, rollbacks, audit trails.

</details>

<details>
<summary><b>Workflow blueprints & integration schemas</b></summary>

- **Blueprints:** Each recipe maps to [registry/blueprints/](registry/blueprints/) with optional ICP, integration references, and per-step prompts.
- **Data to wire:** [registry/integration_schemas/](registry/integration_schemas/) has reference schemas for Salesforce, HubSpot, Stripe so you can wire CRM and billing without reinventing. See [Playbooks](docs/PLAYBOOKS.md).

</details>

---

## Quick start

1. **Install** (see above).

2. **See a working flow quickly** — pick one by time you have:
   - ⏱️ **15 min:** [Lead scoring agent](docs/QUICK_WINS.md#15-minute-win-lead-scoring) (2 skills)
   - 🕐 **1 hour:** [Churn prevention agent](docs/QUICK_WINS.md#1-hour-win-churn-risk-alerts) (3 skills)
   - 🌅 **Half day:** [Campaign automation agent](docs/QUICK_WINS.md#half-day-win-campaign-launch-automation) (5 skills)

3. **Check installation:**

   ```bash
   npx skills-directory status
   ```

4. **Deploy from a recipe:** Browse the [Skill Chain Cookbook](docs/SKILL_CHAINS.md) — 36 recipes with step-by-step instructions across 15+ domains.

---

## CLI reference

| Command                                     | Description                            |
| ------------------------------------------- | -------------------------------------- |
| `npx skills-directory status`               | Verify installation and file integrity |
| `npx skills-directory list --domain plg`    | List skills in a domain                |
| `npx skills-directory ecosystem`            | Generate tool recommendations          |
| `npx skills-directory showcase`             | Show what you can build (use cases)    |
| `npx skills-directory install --target all` | Manually install to Cursor + Claude    |
| `npx skills-directory stats`                | Library statistics                     |
| `npx skills-directory uninstall`            | Remove installed skills                |

---

## Use cases (by situation)

### Sales & RevOps

You already use a CRM and want leads scored and routed without writing the pipeline yourself. Recipes cover qualification, deal health, and forecasting.

### Customer Success

You want to spot churn risk and trigger playbooks instead of building models from scratch. Recipes cover health monitoring, at-risk accounts (60–90 days early), and expansion/upsell triggers.

### Finance & FinOps

You need burn, scenarios, and board-ready numbers without building everything in-house. Recipes cover ARR, burn rate, investor metrics, scenario planning, and board reporting.

### Marketing & Growth

You want content or experiments wired into a workflow. Recipes cover content creation and distribution, conversion optimization, and programmatic SEO.

[Detailed outcomes and calculations →](docs/VALUE.md)

---

## Documentation

### Strategy and value

- **[VALUE.md](docs/VALUE.md)** — Outcomes and calculations for core use cases.
- **[SKILL_CHAINS.md](docs/SKILL_CHAINS.md)** — Skill Chain Cookbook: 36 recipes.
- **[SHOWCASE.md](docs/SHOWCASE.md)** — Case studies and examples.
- **[QUICK_WINS.md](docs/QUICK_WINS.md)** — First agent in 15 min to 4 hours.

### Technical and development

- **[Architecture](ARCHITECTURE.md)** — How the system works.
- **[Build Your First Skill](docs/BUILD_YOUR_FIRST_SKILL.md)** — Create a skill step-by-step.
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** — Peer dependency warnings and common issues.
- **[Metrics methodology](METRICS.md)** — Skill counts (764 total: 382 executable + 382 reference guides).
- **[Skills directory](docs/directory.md)** — Browse all skills by domain.
- **[Skill tree](docs/skill-tree.md)** — Skills by domain (visual).
- **[AI Agent composability](docs/technical/AI_AGENT_COMPOSABILITY_ANALYSIS.md)** — Agent composition.

### Contributing

To contribute to skene-cookbook, set up your environment:

```bash
git clone https://github.com/SkeneTechnologies/skene-cookbook.git
cd skene-cookbook

pip install -r requirements-test.txt
npm install
pre-commit install
pre-commit run --all-files
```

Pre-commit runs formatting, linting, secret checks. Bypass in emergencies: `git commit --no-verify`.

Before pushing to the public remote, run: `./scripts/pre_release_check.sh` or `npm run preflight`. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Community and support

**Bug or question:** [Open an issue →](https://github.com/SkeneTechnologies/skene-cookbook/issues/new)

**Contributing:** [Build Your First Skill](docs/BUILD_YOUR_FIRST_SKILL.md) · [CONTRIBUTING.md](CONTRIBUTING.md) · [Code of Conduct](CODE_OF_CONDUCT.md)

**Security:** [Security Policy](SECURITY_POLICY.md)

---

## Skill sources

Skills curated from: Anthropic Official, Trail of Bits, obra/superpowers, K-Dense-AI, awesome-cursor-rules, Skene PLG

---

<p align="center">
  Built by Skene Technologies. Licensed under <a href="LICENSE">MIT</a>.
</p>
