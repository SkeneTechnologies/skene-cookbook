# Build AI Agents in Days, Not Months

<p align="left">
  <a href="https://github.com/SkeneTechnologies/skene-cookbook/actions"><img src="https://github.com/SkeneTechnologies/skene-cookbook/workflows/Lint%20&%20Build%20Documentation/badge.svg" alt="GitHub Actions"></a>
  <a href="https://codecov.io/gh/SkeneTechnologies/skene-cookbook"><img src="https://codecov.io/gh/SkeneTechnologies/skene-cookbook/branch/main/graph/badge.svg" alt="Test Coverage"></a>
  <a href="CODE_OF_CONDUCT.md"><img src="https://img.shields.io/badge/code%20of%20conduct-contributor%20covenant-green.svg" alt="Code of Conduct"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://www.npmjs.com/package/@skene/skills-directory"><img src="https://img.shields.io/npm/v/@skene/skills-directory.svg" alt="npm version"></a>
</p>

<p align="left">
  <a href="METRICS.md"><img src="https://img.shields.io/badge/skills-765%20total-blue" alt="Total Skills"></a>
  <a href="METRICS.md"><img src="https://img.shields.io/badge/executable-383%20skills-green" alt="Executable"></a>
  <a href="METRICS.md"><img src="https://img.shields.io/badge/context-382%20skills-orange" alt="Context"></a>
  <a href="METRICS.md"><img src="https://img.shields.io/badge/domains-23%20total-purple" alt="Domains"></a>
</p>

**Compose 765 AI skills into powerful AI agents** — No ML expertise required. Skene allows you to bridge the gap between "cool demo" and "production tool" using pre-built **Skill Chains**.

[**Explore the Directory**](docs/directory.md) • [**View ROI Metrics**](METRICS.md) • [**Quick Start**](#-quick-start) • [**Documentation**](#-documentation)

---

## 🎭 Choose Your Path

_Tailored guides to get you up and running based on your role._

| Role                | Focus Area                         | Get Started                                   |
| :------------------ | :--------------------------------- | :-------------------------------------------- |
| 👔 **Sales Leader** | Lead scoring & pipeline management | [View Guide →](docs/personas/sales-leader.md) |
| 🚀 **Growth PM**    | PLG activation & engagement flows  | [View Guide →](docs/personas/growth-pm.md)    |
| 🔬 **Researcher**   | Scientific tools & data analysis   | [View Guide →](docs/personas/researcher.md)   |
| 💼 **Finance/CFO**  | Financial intelligence & reporting | [View Guide →](docs/personas/cfo.md)          |

Or [browse all 765 skills →](docs/directory.md)

---

## ⚡ Why Skill Chains?

Traditional agents are built as monolithic codebases. **Skill Chains** are modular, composable sequences that significantly reduce time-to-market.

| Traditional AI Agents         | Skill Chains                   |
| ----------------------------- | ------------------------------ |
| 3-6 months development        | **1-2 weeks**                  |
| $50K-$150K cost               | **$5K-$10K**                   |
| Custom code, hard to maintain | Pre-built skills, easy updates |
| Single-purpose                | Composable, reusable           |

> [!TIP] > **Real ROI:** A standard Sales Agent built with Skene typically saves **$20K–$40K/month** by automating qualification. Finance Agents save **$50K+/month** in CFO/finance team time. Growth Agents drive **15%+ conversion lift** through automated optimization. Churn Prevention saves **$400K ARR/year** through early intervention.
>
> [Read the full Value Proposition →](docs/VALUE.md)

---

## 📦 Installation

```bash
npm install @skene/skills-directory
```

### 🛠️ Auto-Activation

Skills are automatically installed to your local environment during the npm install step. They are tailored for modern IDEs and LLM interfaces:

- **Cursor:** `~/.cursor/skills/`
- **Claude:** `~/.claude/skills/`

**Auto-install automatically skips in:**

- CI/CD environments (GitHub Actions, CircleCI, Jenkins)
- Docker containers
- When `--ignore-scripts` flag is used

To skip auto-install manually (e.g., in CI/CD or Docker):

```bash
SKIP_SKILLS_INSTALL=true npm install @skene/skills-directory
```

🎯 **Bonus:** An `ECOSYSTEM.md` file is generated with tailored recommendations for other Skene tools that complement your stack!

---

## 📂 What's Included?

<details open>
<summary><b>Executable Skills (383)</b></summary>

- **70 PLG Skills**: Product-led growth, activation, and onboarding.
- **52 Marketing Skills**: Content, SEO, campaigns, and analytics.
- **29 Customer Success**: Health scoring and churn prediction.
- **25 RevOps Skills**: Sales pipeline, forecasting, and GTM alignment.
- **20 Monetization Skills**: Pricing, billing, revenue optimization.
- **19 AI Ops Skills**: Intelligent automation and ML operations.
- **187 More Skills**: Across security, data ops, devex, finance, HR, and more.

[See all executable skills →](METRICS.md#executable-skills-breakdown)

</details>

<details>
<summary><b>Context & Infrastructure (382)</b></summary>

- **241 Cursor Rules**: Best-practice IDE guidelines for 241+ frameworks.
- **141 Scientific Skills**: Research tools, bioinformatics, and data analysis.
- **Integrations**: 40+ standardized tools (CRM, Analytics, Billing).
- **Security**: Approval gates, rollbacks, and audit trails included.

</details>

---

## 🚀 Quick Start

1. **Install the library** (as shown above).

2. **Pick a "Win" level** to deploy your first agent:

   - ⏱️ **15-Min Win**: [Lead Scoring Agent](docs/QUICK_WINS.md#15-minute-win-lead-scoring) (2 skills)
   - 🕐 **1-Hour Win**: [Churn Prevention Agent](docs/QUICK_WINS.md#1-hour-win-churn-risk-alerts) (3 skills)
   - 🌅 **Half-Day Win**: [Campaign Automation Agent](docs/QUICK_WINS.md#half-day-win-campaign-launch-automation) (5 skills)

3. **Verify installation:**

   ```bash
   npx skills-directory status
   ```

4. **Explore recipes:**
   Browse [28 ready-to-use skill chain recipes](docs/SKILL_CHAINS.md) with step-by-step instructions across 15+ domains.

---

## ⌨️ CLI Reference

| Command                                     | Description                               |
| ------------------------------------------- | ----------------------------------------- |
| `npx skills-directory status`               | Verify installation & file integrity      |
| `npx skills-directory list --domain plg`    | List all skills in a specific domain      |
| `npx skills-directory ecosystem`            | Generate tailored tool recommendations    |
| `npx skills-directory showcase`             | Show what you can build (ROI & use cases) |
| `npx skills-directory install --target all` | Manually install to Cursor + Claude       |
| `npx skills-directory stats`                | Show library statistics                   |
| `npx skills-directory uninstall`            | Remove installed skills                   |

---

## 💼 Use Cases

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

## 📚 Documentation

### 🚀 Strategy

- **[VALUE.md](docs/VALUE.md)** — ROI calculations & 5 core use cases.
- **[SKILL_CHAINS.md](docs/SKILL_CHAINS.md)** — 28 ready-to-use recipes.
- **[SHOWCASE.md](docs/SHOWCASE.md)** — Real-world case studies.
- **[QUICK_WINS.md](docs/QUICK_WINS.md)** — Deploy your first agent in 15 min to 4 hours.

### 🔧 Technical & Development

- **[Architecture](ARCHITECTURE.md)** — Deep dive into the system.
- **[Build Your First Skill](docs/BUILD_YOUR_FIRST_SKILL.md)** — Step-by-step skill creation tutorial.
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** — Solving peer dependency warnings and common issues.
- **[Metrics Methodology](METRICS.md)** — Canonical skill counts (765 total: 383 executable + 382 context).
- **[Complete Skills Directory](docs/directory.md)** — Browse all skills by domain.
- **[Visual Skill Tree](docs/skill-tree.md)** — See skills organized by domain.
- **[AI Agent Composability Analysis](docs/technical/AI_AGENT_COMPOSABILITY_ANALYSIS.md)** — Deep dive into agent composition.

### 👨‍💻 Contributing

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

Pre-commit hooks will automatically format code, lint, detect secrets, and check for common issues. To bypass hooks in emergencies: `git commit --no-verify`

See [CONTRIBUTING.md](CONTRIBUTING.md) for full contribution guidelines.

---

## 🤝 Community & Support

**Found a bug?** [Open an issue →](https://github.com/SkeneTechnologies/skene-cookbook/issues/new?template=bug_report.yml)

**Have a question?** [Start a discussion →](https://github.com/SkeneTechnologies/skene-cookbook/discussions)

**Contributing:** [Build Your First Skill](docs/BUILD_YOUR_FIRST_SKILL.md) • [Contributing Guidelines](CONTRIBUTING.md) • [Code of Conduct](CODE_OF_CONDUCT.md)

**Security:** Please report vulnerabilities via our [Security Policy](SECURITY_POLICY.md).

---

## 📌 Skill Sources

Skills curated from: Anthropic Official, Trail of Bits, obra/superpowers, K-Dense-AI, awesome-cursor-rules, Skene PLG

---

<p align="center">
  Built with ❤️ by Skene Technologies. Licensed under <a href="LICENSE">MIT</a>.
</p>
