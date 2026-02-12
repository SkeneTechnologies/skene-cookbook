# Build AI Agents in Days, Not Months

[![GitHub Actions](https://github.com/SkeneTechnologies/skene-cookbook/workflows/Lint%20&%20Build%20Documentation/badge.svg)](https://github.com/SkeneTechnologies/skene-cookbook/actions)
[![Test Coverage](https://codecov.io/gh/SkeneTechnologies/skene-cookbook/branch/main/graph/badge.svg)](https://codecov.io/gh/SkeneTechnologies/skene-cookbook)
[![Code of Conduct](https://img.shields.io/badge/code%20of%20conduct-contributor%20covenant-green.svg)](CODE_OF_CONDUCT.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![npm version](https://img.shields.io/npm/v/@skene/skills-directory.svg)](https://www.npmjs.com/package/@skene/skills-directory)

[![Total Skills](https://img.shields.io/badge/skills-765%20total-blue)](METRICS.md)
[![Executable](https://img.shields.io/badge/executable-383%20skills-green)](METRICS.md)
[![Context](https://img.shields.io/badge/context-382%20skills-orange)](METRICS.md)
[![Domains](https://img.shields.io/badge/domains-23%20total-purple)](METRICS.md)

**Compose 765 AI skills into powerful AI agents** — No ML expertise required

- **383 executable skills** across 21 domains (marketing, PLG, sales, etc.)
- **382 context skills** (241 cursor rules + 141 scientific computing)

Install once. Build unlimited agents. Deploy in days.

📊 [See detailed metrics →](METRICS.md)

---

## Who Are You?

Choose your path to get started:

👔 [**Sales Leader**](docs/personas/sales-leader.md) — Automate lead scoring & pipeline management


🚀 [**Growth PM**](docs/personas/growth-pm.md) — Build PLG activation & engagement flows

🔬 [**Researcher**](docs/personas/researcher.md) — Scientific tools & data analysis

💼 [**CFO/Finance**](docs/personas/cfo.md) — Financial intelligence & reporting

Or [browse all 765 skills →](docs/directory.md) | [See metrics →](METRICS.md)

---

## Why Skill Chains?

| Traditional AI Agents | Skill Chains |
|----------------------|--------------|
| 3-6 months development | 1-2 weeks |
| $50K-$150K cost | $5K-$10K |
| Custom code, hard to maintain | Pre-built skills, easy updates |
| Single-purpose | Composable, reusable |

## Real ROI

🎯 **Sales Agent**: Saves $20K-$40K/month by automating lead qualification

📊 **Finance Agent**: Saves $50K+/month in CFO/finance team time

🚀 **Growth Agent**: Drives 15%+ conversion lift through automated optimization

💰 **Churn Prevention**: Saves $400K ARR/year through early intervention

[See full value proposition →](docs/VALUE.md)

---

## Install

```bash
npm install @skene/skills-directory
```

✨ **Skills are automatically activated** during install!
They're installed to both Cursor (`~/.cursor/skills/`) and Claude (`~/.claude/skills/`)

🎯 **Bonus:** An `ECOSYSTEM.md` file is generated with tailored recommendations for other Skene tools that complement your stack!

### Auto-Activation Behavior

**Auto-install runs on first install** for local development environments.

**Automatically skips in:**
- CI/CD environments (GitHub Actions, CircleCI, Jenkins, etc.)
- Docker containers
- When `--ignore-scripts` flag is used

**To manually skip:**
```bash
SKIP_SKILLS_INSTALL=true npm install @skene/skills-directory
```

### Manual Installation

To install or reinstall skills manually:

```bash
# Install to Cursor and Claude
npx skills-directory install --target all

# Cursor only
npx skills-directory install --target cursor

# Claude only
npx skills-directory install --target claude
```

## What's Included

### Executable Skills (383)
✅ **70 PLG skills** — Product-led growth, activation, onboarding (plg + plg_frameworks)
✅ **52 Marketing skills** — Content, SEO, campaigns, analytics
✅ **29 Customer Success skills** — Health scoring, churn prediction, retention
✅ **25 RevOps skills** — Sales pipeline, forecasting, GTM alignment
✅ **20 Monetization skills** — Pricing, billing, revenue optimization
✅ **19 AI Ops skills** — Intelligent automation and ML operations
✅ **187 more skills** — Across security, data ops, devex, finance, HR, and more

### Context Skills (382)
✅ **241 Cursor Rules** — IDE guidelines for 241+ frameworks and tools
✅ **141 Scientific Computing** — Research tools, bioinformatics, data analysis

### Infrastructure
✅ **40+ standardized tools** — CRM, analytics, messaging, billing integrations
✅ **Production-ready security** — Approval gates, rollback, audit trails

[Browse all skills by domain →](docs/directory.md) | [See detailed metrics →](METRICS.md)

## Quick Start

### 1. Install (Skills Auto-Activate!)

```bash
npm install @skene/skills-directory
```

Skills are automatically installed to Cursor and Claude during this step.

### 2. Start Building

- **15-minute win:** [Lead Scoring Agent](docs/QUICK_WINS.md#15-minute-win-lead-scoring) (2 skills)
- **1-hour win:** [Churn Prevention Agent](docs/QUICK_WINS.md#1-hour-win-churn-risk-alerts) (3 skills)
- **Half-day win:** [Campaign Automation Agent](docs/QUICK_WINS.md#half-day-win-campaign-launch-automation) (5 skills)

[See all quick wins →](docs/QUICK_WINS.md)

### 3. Explore Recipes

Browse [28 ready-to-use skill chain recipes](docs/SKILL_CHAINS.md) with step-by-step instructions across 15+ domains.

---

## Use Cases

### Sales & RevOps
- **Lead qualification pipeline** — Qualify, score, and route leads automatically
- **Deal inspection engine** — Analyze deal health and identify risks
- **Pipeline forecasting** — Predict revenue and commit accuracy

### Customer Success
- **Health monitoring** — Real-time customer health tracking
- **Churn prediction** — Identify at-risk accounts 60-90 days early
- **Expansion playbooks** — Trigger upsell opportunities automatically

### Finance & FinOps
- **CFO dashboard** — Real-time ARR, burn rate, and investor metrics
- **Scenario planning** — Model growth scenarios instantly
- **Board reporting** — Auto-generate board decks and reports

### Marketing & Growth
- **Content automation** — End-to-end content creation and distribution
- **A/B testing engine** — Continuous conversion optimization
- **SEO optimization** — Programmatic SEO at scale

[See detailed ROI calculations →](docs/VALUE.md)

---

## How It Works

Skills are installed to:

- **Cursor:** `~/.cursor/skills/`
- **Claude:** `~/.claude/skills/`

Cursor and Claude automatically pick the right skill based on your prompt. Chain skills together by routing exit states to next skill inputs. No ML expertise required.

## CLI Commands

| Command                              | Description                |
| ------------------------------------ | -------------------------- |
| `npx skills-directory install --target all` | Install to Cursor + Claude |
| `npx skills-directory status`        | Check installation status & verify files |
| `npx skills-directory showcase`     | Show what you can build (ROI & use cases) |
| `npx skills-directory ecosystem`     | Generate tailored ecosystem recommendations |
| `npx skills-directory list --domain plg` | List skills by domain |
| `npx skills-directory stats`         | Show library statistics   |
| `npx skills-directory uninstall`     | Remove installed skills    |

---

## Documentation

### 🚀 Getting Started
- **[VALUE.md](docs/VALUE.md)** — Why skill chains? ROI calculations & 5 use cases
- **[QUICK_WINS.md](docs/QUICK_WINS.md)** — Deploy your first agent in 15 min to 4 hours
- **[SKILL_CHAINS.md](docs/SKILL_CHAINS.md)** — 28 ready-to-use recipes with step-by-step instructions (PLG, RevOps, Marketing, HR, Security, Data Ops, and more)
- **[SHOWCASE.md](docs/SHOWCASE.md)** — Real-world agent examples and case studies

### 📚 Reference
- **[Metrics](METRICS.md)** — Canonical skill counts and methodology (765 total: 383 executable + 382 context)
- [Complete Skills Directory](docs/directory.md) — Browse all skills by domain
- [Visual Skill Tree](docs/skill-tree.md) — See skills organized by domain
- [Browse by Job Function](docs/functions/) — Find skills for your role
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md) — Common issues and solutions
- [Welcome Screen Features](docs/WELCOME_SCREEN.md) — Beautiful terminal UI

### 🔧 Technical
- [Architecture Guide](ARCHITECTURE.md) — How the system works
- [Ecosystem Generator](scripts/ecosystem-generator/README.md) — Tailored recommendations system
- [AI Agent Composability Analysis](docs/technical/AI_AGENT_COMPOSABILITY_ANALYSIS.md) — Deep dive into agent composition
- [Security Policy](SECURITY_POLICY.md) — Security best practices

### 👨‍💻 Development Setup

If you're contributing to skene-cookbook, set up your development environment:

```bash
# Clone the repository
git clone https://github.com/SkeneTechnologies/skene-cookbook.git
cd skene-cookbook

# Install Python dependencies
pip install -r requirements-test.txt

# Install Node.js dependencies
npm install

# Install pre-commit hooks (runs linting and security checks automatically)
pre-commit install

# Verify installation
pre-commit run --all-files
```

**Pre-commit hooks will automatically:**
- Format Python code (Black, isort)
- Lint Python code (Flake8)
- Format JavaScript/JSON/YAML (Prettier)
- Lint JavaScript (ESLint)
- Detect secrets and credentials
- Check for common issues (trailing whitespace, merge conflicts, etc.)

To bypass hooks in emergencies: `git commit --no-verify`

See [CONTRIBUTING.md](CONTRIBUTING.md) for full contribution guidelines.

### 🤝 Community
- **[Build Your First Skill](docs/BUILD_YOUR_FIRST_SKILL.md)** — Step-by-step skill creation tutorial
- [Contributing Guidelines](CONTRIBUTING.md) — How to contribute to the library
- [Code of Conduct](CODE_OF_CONDUCT.md) — Community standards and expectations
- [GitHub Discussions](https://github.com/SkeneTechnologies/skene-cookbook/discussions) — Ask questions and share ideas

---

## Troubleshooting

### Peer Dependency Warnings

If you see peer dependency warnings for `zod` or `react` when installing `@skene/skills-directory`, these are **safe to ignore**. They come from other packages in your project, not from skills-directory itself.

**Why this happens:**
- Skills Directory has no zod or react dependencies
- Warnings appear when your project has version conflicts with other installed packages
- Common culprits: AI SDK packages requiring zod v3 vs v4, or React 18 vs 19

**To resolve (optional):**
```bash
# Check which packages have conflicts
npm ls zod
npm ls react

# Update conflicting packages or use --legacy-peer-deps
npm install --legacy-peer-deps
```

**Note:** These warnings don't affect Skills Directory functionality at all.

### Post-install Message Not Showing

If you don't see the "What can you build today?" message after installation:
- The message may have been hidden by npm warnings
- You can manually verify installation: `npx skills-directory install --target all`
- Check that the package installed correctly: `npm ls @skene/skills-directory`

### Verifying Installation

To check if skills are installed and verify file integrity:

```bash
npx skills-directory status
```

This will show:
- ✅ Whether Claude and Cursor skills are installed
- 📊 Number of skills installed
- 📅 Installation date
- 🔍 File integrity check (all files present)

**Example output:**
```
📊 Skills Installation Status

✅ Claude Skills Installed
   Skills: 773
   Generated: 2/5/2026, 12:14:02 PM
   Location: /Users/username/.claude/skills
   Files intact: 773/773

✅ Cursor Skills Installed
   Skills: 773
   Generated: 2/6/2026, 12:36:21 AM
   Location: /Users/username/.cursor/skills
   Files intact: 773/773
```

**Skills persist between sessions** — Once installed, skills remain in `~/.claude/skills/` and `~/.cursor/skills/` permanently. You don't need to reinstall them between sessions or terminal restarts.

---

## What's a Skill Chain?

A **skill chain** is a sequence of skills connected together to automate an entire workflow:

```
Example: Sales Qualification Pipeline

lead_qualification → opportunity_scoring → deal_inspection →
next_best_action → content_recommender

Result: Complete automation from first touch to meeting booked
```

**Benefits:**
- ⚡ **Faster:** Build in days vs months
- 💰 **Cheaper:** 10x lower cost than custom development
- 🔄 **Reusable:** Compose skills in unlimited ways
- 🛡️ **Production-ready:** Security, rollback, and monitoring built-in

[Learn more about skill chains →](docs/VALUE.md#the-power-of-composition)

---

## Skill Sources

Skills curated from: Anthropic Official, Trail of Bits, obra/superpowers, K-Dense-AI, awesome-cursor-rules, Skene PLG

## License

MIT
