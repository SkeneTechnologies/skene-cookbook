# Skene Cookbook Metrics

**Last Updated:** 2026-02-12
**Version:** 0.1.1
**Canonical Source of Truth** — All documentation must reference this file for accuracy

---

## Official Numbers

### Skill Chain Cookbook

- **Ready-to-use recipes**: 36 (Skill Chains — the primary product)
- **Each recipe** chains 2–7 skills from the library below; see [SKILL_CHAINS.md](docs/SKILL_CHAINS.md).

### Skill Counts (ingredients for recipes)

- **Total Skills**: 765
- **Executable Skills**: 383
- **Context Skills**: 382
  - Cursor Rules: 241
  - Scientific Computing: 141

### Domain Counts

- **Executable Domains**: 21
- **Context Domains**: 2
- **Total Unique Domains**: 23

---

## Executable Skills Breakdown

### By Domain

| Domain                 | Skills | Description                                     |
| ---------------------- | ------ | ----------------------------------------------- |
| **marketing**          | 52     | Content creation, SEO, campaigns, analytics     |
| **plg_frameworks**     | 46     | Product-led growth frameworks and patterns      |
| **customer_success**   | 29     | Health scoring, churn prediction, retention     |
| **revops**             | 25     | Sales pipeline, forecasting, GTM alignment      |
| **plg**                | 24     | User activation, onboarding, viral growth       |
| **monetization**       | 20     | Pricing, billing, revenue optimization          |
| **ai_ops**             | 19     | AI model operations and management              |
| **product_ops**        | 18     | Product analytics and operations                |
| **security**           | 17     | Security analysis, compliance, threat detection |
| **anthropic_official** | 16     | Official Anthropic skills and tools             |
| **ecosystem**          | 16     | Ecosystem-led growth and partnerships           |
| **devex**              | 14     | Developer experience and tooling                |
| **superpowers**        | 14     | Power user workflows and automations            |
| **finops**             | 12     | Financial operations and reporting              |
| **support_ops**        | 12     | Customer support operations                     |
| **community**          | 12     | Community management and engagement             |
| **compliance**         | 11     | Regulatory compliance and governance            |
| **data_ops**           | 10     | Data pipelines and analytics operations         |
| **people_ops**         | 8      | HR, recruiting, people management               |
| **development**        | 5      | Software development workflows                  |
| **vcf**                | 3      | Value creation frameworks                       |

**Total Executable:** 383 skills across 21 domains

### By Job Function

_Mapping domains to typical job functions:_

| Job Function         | Skill Count | Primary Domains                                                                          |
| -------------------- | ----------- | ---------------------------------------------------------------------------------------- |
| **Engineering**      | 77          | development (5), devex (14), ai_ops (19), data_ops (10), security (17), superpowers (14) |
| **Marketing**        | 52          | marketing (52)                                                                           |
| **Product**          | 88          | plg (24), plg_frameworks (46), product_ops (18)                                          |
| **Sales**            | 25          | revops (25)                                                                              |
| **Customer Success** | 41          | customer_success (29), support_ops (12)                                                  |
| **Finance**          | 12          | finops (12)                                                                              |
| **Operations**       | 49          | monetization (20), ecosystem (16), compliance (11), vcf (3)                              |
| **People/HR**        | 8           | people_ops (8)                                                                           |
| **Community**        | 28          | community (12), anthropic_official (16)                                                  |

_Note: Some domains serve multiple functions. Total exceeds 383 due to overlapping categorization._

---

## Context Skills Breakdown

### Cursor Rules (241 skills)

Technology-specific coding guidelines and best practices for Cursor IDE:

- Web frameworks (React, Vue, Angular, etc.)
- Backend frameworks (Flask, Django, Express, etc.)
- Cloud platforms (AWS, GCP, Azure)
- Databases (PostgreSQL, MongoDB, Redis, etc.)
- DevOps tools (Docker, Kubernetes, Terraform, etc.)
- Languages (Python, JavaScript, TypeScript, Go, Rust, etc.)
- And 200+ more specialized tools and frameworks

**Location:** `skills-library/context/cursor_rules/`

### Scientific Computing (141 skills)

Domain-specific knowledge for research and scientific workflows:

- Bioinformatics tools (BLAST, UniProt, PDB, etc.)
- Data analysis libraries (NumPy, Pandas, SciPy, etc.)
- Visualization tools (Matplotlib, Seaborn, Plotly, etc.)
- Machine learning frameworks (scikit-learn, TensorFlow, PyTorch, etc.)
- Research databases and APIs
- Academic workflow tools

**Location:** `skills-library/context/scientific/`

---

## Counting Methodology

### What Counts as "One Skill"?

A skill is defined by the presence of a `skill.json` file in a skill directory.

**Example skill directory structure:**

```
skills-library/executable/marketing/seo-optimizer/
├── skill.json          ← This defines the skill
├── metadata.yaml       ← Additional metadata
├── instructions.md     ← Human-readable docs
└── references/         ← Optional reference materials
    ├── api_docs.md
    └── examples.md
```

**Counting Command:**

```bash
# Count executable skills
find skills-library/executable -name "skill.json" | wc -l

# Count context skills
find skills-library/context -name "skill.json" | wc -l

# Count all skills
find skills-library -name "skill.json" | wc -l
```

### Executable vs Context Skills

**Executable Skills** (`skills-library/executable/`):

- AI agent skills with tools and execution logic
- Invokable by Claude/Cursor to perform actions
- Include tool definitions, parameters, error handling
- Production-ready with security gates
- **Count: 383 skills**

**Context Skills** (`skills-library/context/`):

- Reference materials and domain knowledge
- Cursor rules for IDE-specific guidance
- Scientific computing documentation
- Not directly executable, but provide context for AI
- **Count: 382 skills**

### Why Multiple Numbers?

You may see different numbers referenced in different contexts:

| Context                 | Number Used           | Reasoning                                  |
| ----------------------- | --------------------- | ------------------------------------------ |
| Marketing materials     | "760+ skills"         | Total skills (765), rounded for simplicity |
| Technical documentation | "383 executable"      | Precise count of action-taking skills      |
| User-facing features    | "765 total resources" | All skills including context               |
| Domain browsing         | "21 domains"          | Executable domains only                    |
| Complete catalog        | "23 domains"          | All domains including context              |

**All of these are correct** for their respective audiences. When in doubt:

- **User-facing claims:** Use "760+ skills" (total)
- **Technical accuracy:** Use "383 executable + 382 context = 765 total"
- **Marketing copy:** Use "760+ skills across 23 domains"

---

## Single Source of Truth

### For All Documentation

When writing or updating documentation:

1. **Reference this file** for canonical numbers
2. **Link to METRICS.md** rather than hardcoding numbers
3. **Use consistent terminology:**
   - "760+ skills" or "765 total skills" for general use
   - "383 executable skills" for technical precision
   - "23 domains" for domain count (21 executable + 2 context)

### Verification

To verify these numbers match the actual repository:

```bash
# Navigate to repository
cd /Users/teemukinos/skene-primary/skene-cookbook

# Count executable skills by domain
for dir in skills-library/executable/*/; do
  echo "$(basename "$dir"): $(find "$dir" -name 'skill.json' | wc -l | tr -d ' ')"
done

# Count context skills
echo "cursor_rules: $(find skills-library/context/cursor_rules -name 'skill.json' | wc -l | tr -d ' ')"
echo "scientific: $(find skills-library/context/scientific -name 'skill.json' | wc -l | tr -d ' ')"

# Count totals
echo "Total executable: $(find skills-library/executable -name 'skill.json' | wc -l | tr -d ' ')"
echo "Total context: $(find skills-library/context -name 'skill.json' | wc -l | tr -d ' ')"
echo "Grand total: $(find skills-library -name 'skill.json' | wc -l | tr -d ' ')"
```

### Automated Verification

A verification script ensures documentation stays aligned:

```bash
# Run verification
npm run verify:metrics

# This checks all documentation files against actual filesystem counts
# Fails with exit code 1 if any mismatches are found
```

See `scripts/sync_metrics.js` for implementation details.

---

## Historical Context

### Why This File Exists

Prior to v0.1.2, skill counts were inconsistent across documentation:

- README.md claimed "760+ skills"
- index.json showed different numbers
- Various docs had conflicting domain counts
- No clear definition of "what is a skill"

**This file solves that problem** by establishing:

1. Clear counting methodology
2. Single canonical source
3. Automated verification
4. Consistent terminology across all docs

### Version History

| Version | Total Skills | Executable | Context | Domains |
| ------- | ------------ | ---------- | ------- | ------- |
| 0.1.2   | 765          | 383        | 382     | 23      |
| 0.1.1   | ~760         | ~383       | ~382    | 23      |
| 0.1.0   | ~760         | ~383       | ~382    | 23      |

_Note: Counts for 0.1.0 and 0.1.1 are retroactive estimates based on git history._

---

## Maintenance

### When Skills Are Added/Removed

1. **Update METRICS.md first** with new counts
2. **Run verification script** to ensure accuracy:
   ```bash
   npm run verify:metrics
   ```
3. **Update other docs** if categories/domains change
4. **Commit with clear message** indicating metric changes

### Quarterly Reviews

Every quarter, verify:

- [ ] Skill counts match filesystem
- [ ] Domain categorization is accurate
- [ ] Job function mappings are current
- [ ] All documentation references METRICS.md
- [ ] Verification script is working

---

## Quick Reference

**For Copy/Paste:**

```
Total Skills: 765
Executable: 383 (across 21 domains)
Context: 382 (cursor_rules: 241, scientific: 141)
Total Domains: 23
```

**Marketing Tagline:**

> "760+ AI skills for Claude and Cursor across 23 domains"

**Technical Description:**

> "383 executable AI agent skills + 382 context skills = 765 total resources"

**Domain Breakdown:**

> "21 executable domains (marketing, PLG, RevOps, etc.) + 2 context domains (cursor_rules, scientific)"

---

## Links

- [README.md](README.md) — Main repository documentation
- [skills-library/README.md](skills-library/README.md) — Skills library overview
- [SKILLS_CATALOG.md](skills-library/SKILLS_CATALOG.md) — Complete skill catalog
- [index.json](skills-library/index.json) — Machine-readable skill index
- [CHANGELOG.md](CHANGELOG.md) — Version history

---

_This file is the canonical source of truth for all skill metrics. When in doubt, reference this file._
