---
name: install-plg-skills
description: Installs all 27 PLG skills from SkeneTechnologies/plg-skills repository. Clones the repository and copies all skills to the target location (personal or project). Use when the user wants to install PLG skills, add skills from the plg-skills repository, or set up Product-Led Growth skills for Cursor.
---

# Install PLG Skills

Installs all 27 Product-Led Growth skills from the SkeneTechnologies/plg-skills repository into Cursor.

## Quick Start

When the user wants to install PLG skills:

1. Determine installation location (personal vs project)
2. Clone the repository
3. Copy all skills from `skills/` directory to target location
4. Verify installation

## Installation Workflow

### Step 1: Determine Target Location

Ask the user or infer from context:

- **Personal** (`~/.cursor/skills/`): Available across all projects
- **Project** (`.cursor/skills/`): Shared with repository users

Default to project location if working in a project directory.

### Step 2: Clone Repository

Clone to a temporary location:

```bash
cd /tmp
git clone https://github.com/SkeneTechnologies/plg-skills.git plg-skills-temp
```

Or use a project-specific temp directory:

```bash
cd /path/to/project
git clone https://github.com/SkeneTechnologies/plg-skills.git .temp-plg-skills
```

### Step 3: Copy Skills

**For project installation:**
```bash
# Ensure target directory exists
mkdir -p .cursor/skills

# Copy all skills
cp -r .temp-plg-skills/skills/* .cursor/skills/
```

**For personal installation:**
```bash
# Ensure target directory exists
mkdir -p ~/.cursor/skills

# Copy all skills
cp -r /tmp/plg-skills-temp/skills/* ~/.cursor/skills/
```

### Step 4: Cleanup

Remove temporary clone:

```bash
# For project temp
rm -rf .temp-plg-skills

# For system temp
rm -rf /tmp/plg-skills-temp
```

### Step 5: Verify Installation

List installed skills:

```bash
# For project
ls -la .cursor/skills/

# For personal
ls -la ~/.cursor/skills/
```

Expected: 27 skill directories, each containing a `SKILL.md` file.

## Skills Included

The repository contains 27 PLG skills:

**Strategy & Frameworks:**
- `plg-strategy` - PLG readiness, Four Fits, Racecar framework
- `growth-loops` - Loop design and modeling
- `plg-mental-models` - 42 mental models
- `product-led-sales` - PQL/PQA scoring, sales handoff
- `self-serve-motion` - Friction audit, checkout optimization

**Activation & Onboarding:**
- `activation-metrics` - Setup/Aha/Habit moments
- `product-onboarding` - Onboarding architecture
- `signup-flow-cro` - Signup optimization

**Retention & Engagement:**
- `engagement-loops` - Trigger-Action-Reward-Investment
- `retention-analysis` - Retention curves, churn prediction
- `feature-adoption` - Adoption lifecycle

**Monetization & Expansion:**
- `pricing-strategy` - 5 Ps framework, value metrics
- `feature-gating` - Gate types, reverse trials
- `trial-optimization` - Trial types, conversion
- `expansion-revenue` - NRR framework
- `usage-based-pricing` - Consumption models

**Conversion Optimization:**
- `paywall-upgrade-cro` - Paywall types, copy frameworks
- `in-product-messaging` - Message types, targeting

**Acquisition:**
- `viral-loops` - Loop types, K-factor math
- `referral-program` - Referral loop design

**Measurement & Experimentation:**
- `plg-metrics` - PLG metrics stack
- `growth-modeling` - Quantitative models
- `product-analytics` - Event taxonomy, tool setup
- `growth-experimentation` - ICE/RICE prioritization

**Growth Engineering:**
- `free-tool-strategy` - Engineering-as-marketing
- `user-segmentation` - Behavioral cohorts

**Reference:**
- `plg-ideas` - 108 PLG tactics

## Alternative Installation Methods

If the user prefers different methods:

**Git Submodule (for project):**
```bash
git submodule add https://github.com/SkeneTechnologies/plg-skills.git .cursor/plg-skills
# Then symlink or copy skills
cp -r .cursor/plg-skills/skills/* .cursor/skills/
```

**Manual Download:**
1. Download repository as ZIP
2. Extract to temp location
3. Copy `skills/` contents to target

## Error Handling

- **Clone fails**: Check network, verify repository URL, ensure git is installed
- **Copy fails**: Verify permissions, ensure target directory exists
- **Skills not appearing**: Check Cursor restart required, verify skill structure (each skill needs `SKILL.md`)

## Notes

- Skills are plain Markdown files - no compilation needed
- Each skill directory must contain a `SKILL.md` file with YAML frontmatter
- Installation is immediate - no restart required (but may help with discovery)
- Skills can be updated by re-running installation (will overwrite existing)

