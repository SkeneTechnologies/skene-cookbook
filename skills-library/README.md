# Skene Skills Library

**The largest open-source AI skills library for Claude and Cursor**

**764 AI skills** across 23 domains: **382 executable** + **382 reference guides**

Compatible with Claude, Cursor, and SkeneFlow.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 📊 **Metrics**: See [METRICS.md](../METRICS.md) for the canonical source of all skill counts and methodology.

## Quick Start

```bash
# Install skills to Cursor
npx skene-skills install --target cursor

# Install skills to Claude
npx skene-skills install --target claude

# Install to both platforms
npx skene-skills install --target all

# View statistics
npx skene-skills stats

# List skills by domain
npx skene-skills list --domain plg
```

## What's Included

### Reference Guides (382)
| Category | Skills | Description |
|----------|--------|-------------|
| **Cursor Rules** | 241 | Technology-specific coding rules (React, Next.js, Python, etc.) |
| **Scientific** | 141 | Research, data science, bioinformatics skills |

### Executable Skills (383)
| Category | Skills | Description |
|----------|--------|-------------|
| **Marketing** | 52 | Content, campaigns, SEO, growth marketing |
| **PLG Frameworks** | 46 | Product-led growth playbooks and frameworks |
| **Customer Success** | 29 | Health scoring, churn prevention, renewals |
| **RevOps** | 25 | Pipeline, forecasting, sales automation |
| **PLG** | 24 | Activation, onboarding, viral loops |
| **Monetization** | 20 | Pricing, billing, usage metering |
| **AI Ops** | 19 | AI automation, intent classification |
| **Product Ops** | 18 | Feedback synthesis, roadmap alignment |
| **Security** | 17 | Audit, vulnerability analysis, secure coding |
| **Anthropic Official** | 16 | First-party Claude skills (PDF, DOCX, etc.) |
| **Ecosystem** | 16 | Partner programs, marketplace, co-selling |
| **DevEx** | 14 | Developer experience, docs, onboarding |
| **Superpowers** | 14 | Meta-skills for AI-assisted development |
| **FinOps** | 12 | Cloud cost optimization, budgeting |
| **Support Ops** | 12 | Ticket routing, CSAT, knowledge base |
| **Community** | 12 | Community-contributed skills |
| **Compliance** | 11 | SOC2, GDPR, security policies |
| **Data Ops** | 10 | Data pipelines, quality, governance |
| **People Ops** | 8 | Hiring, culture, performance |
| **Development** | 5 | General development practices |
| **VCF** | 3 | Venture/VC deal flow skills |

**Total: 764 skills** (382 executable + 382 reference guides) across 23 domains

See [METRICS.md](../METRICS.md) for detailed counting methodology and domain breakdown.

## Platform Compatibility

Skills work across multiple platforms:

| Platform | Format | Installation |
|----------|--------|--------------|
| **Cursor** | `.mdc` with globs | `~/.cursor/skills/` |
| **Claude** | `SKILL.md` with frontmatter | `~/.claude/skills/` |
| **SkeneFlow** | `skill.json` + `instructions.md` | Native registry |

## Skill Sources

This library aggregates skills from:

- **Anthropic Official** — First-party Claude skills
- **Trail of Bits** — Security research skills
- **obra/superpowers** — Meta-skills for AI development
- **K-Dense-AI** — Scientific and research skills
- **awesome-cursor-rules** — Technology-specific Cursor rules
- **Skene PLG Frameworks** — Product-led growth playbooks

## Usage

### Cursor

After installation, skills automatically apply based on file globs:

```
# React skills apply to .tsx files
# Python skills apply to .py files
# etc.
```

### Claude

Skills trigger based on their description. For example:

- "Help me with PDF processing" → triggers `anthropic_official/pdf`
- "Analyze my activation funnel" → triggers `plg/activation`
- "Debug this issue systematically" → triggers `superpowers/systematic-debugging`

### SkeneFlow

Skills integrate with the SkeneFlow state machine:

```typescript
import { SkillRegistry } from 'skeneflow/headless';

const registry = new SkillRegistry('./skills-library');
await registry.indexAll();

const skill = await registry.loadSkill('plg/activation');
```

## Directory Structure

```
skills-library/
├── ai_ops/           # AI-powered automation
├── anthropic_official/ # First-party Claude skills
├── community/        # Community contributions
├── compliance/       # Security & compliance
├── cursor_rules/     # Technology-specific coding rules
├── customer_success/ # Retention & expansion
├── data_ops/         # Data engineering
├── development/      # General dev practices
├── devex/           # Developer experience
├── ecosystem/       # Partner & marketplace
├── finops/          # Cloud cost optimization
├── marketing/       # Growth marketing
├── meta/            # Library management
├── monetization/    # Pricing & billing
├── people_ops/      # HR & culture
├── plg/             # Product-led growth
├── plg_frameworks/  # PLG playbooks
├── product_ops/     # Product management
├── revops/          # Revenue operations
├── scientific/      # Research & science
├── security/        # Security skills
├── skene/           # SkeneFlow skills
├── superpowers/     # Meta AI skills
├── support_ops/     # Support automation
└── vcf/             # Venture capital
```

## Skill Format

Each skill contains:

```
skill-name/
├── skill.json       # Manifest (metadata, tools, schemas)
└── instructions.md  # AI instructions (or .mdc for Cursor)
```

### skill.json Schema

```json
{
  "id": "domain/skill-name",
  "version": "1.0.0",
  "name": "Skill Name",
  "description": "What the skill does and when to use it",
  "domain": "domain",
  "source": "native|anthropic|community|external",
  "origin": "Human-readable origin (e.g. Skene PLG frameworks)",
  "attribution": "https://github.com/...",
  "license": "MIT",
  "maintainer": "Optional maintainer or org",
  "tools": [
    { "name": "tool.name", "required": true }
  ],
  "exitStates": ["success", "failure"],
  "tags": ["tag1", "tag2"]
}
```

**Metadata for open source:** `source`, `origin`, `attribution`, and `license` let developers (and the AI) answer "where did this skill come from?" and "who maintains it?".

## CLI Reference

```bash
# Installation
npx skene-skills install [options]
  --target <target>    Platform: cursor, claude, skeneflow, all (default: all)
  --domain <domain>    Only install skills from this domain
  --symlink            Use symlinks instead of copying

# Export
npx skene-skills export [options]
  --format <format>    Output format: cursor, claude, skeneflow
  --output <path>      Output directory

# Discovery
npx skene-skills stats              # Show library statistics
npx skene-skills list               # List all skills
npx skene-skills list --domain plg  # List skills by domain
npx skene-skills list --tag ai      # List skills by tag

# Management
npx skene-skills uninstall --target cursor  # Remove installed skills
```

## Contributing

### Adding a New Skill

1. Create a directory: `skills-library/{domain}/{skill-name}/`
2. Add `skill.json` with metadata
3. Add `instructions.md` with AI instructions
4. Test with: `npx skene-skills list --domain {domain}`

### Skill Guidelines

- **Be specific**: Include clear triggers and use cases
- **Be concise**: Instructions should be actionable
- **Include examples**: Show input/output patterns
- **Define exit states**: For SkeneFlow compatibility

## License

MIT — See individual skill directories for specific licensing from external sources.

## Links

- [SkeneFlow Repository](https://github.com/SkeneTechnologies/skene-flow)
- [Documentation](https://skene.dev/docs)
- [Discord Community](https://discord.gg/skene)
