# Contributing to Skills Directory

Thank you for your interest in contributing to the Skills Directory! This guide will help you add new skills, improve existing ones, and contribute to the broader ecosystem.

## Table of Contents

1. [Philosophy](#philosophy)
2. [Adding New Skills](#adding-new-skills)
3. [Security Auditing](#security-auditing)
4. [Creating Workflows](#creating-workflows)
5. [Development Setup](#development-setup)

## Philosophy

The Skills Directory is built on these principles:

- **Atomic**: Each skill does one thing well
- **Composable**: Skills chain together seamlessly
- **Secure**: Security analysis is mandatory
- **Open**: Community-driven development

## Adding New Skills

### 1. Choose the Right Domain

First, determine which domain your skill belongs to:

```
skills-library/
├── ecosystem/          # Partner, integration management
├── marketing/          # Campaigns, content, SEO
├── sales/             # Pipeline, deals, CRM
├── customer_success/  # Health, churn, onboarding
├── product_ops/       # Roadmap, releases
├── security/          # Security, compliance
├── finops/            # Billing, revenue
└── ...
```

If your skill doesn't fit existing domains, propose a new one in an issue first.

### 2. Create Skill Directory

```bash
mkdir -p skills-library/[domain]/[skill_name]
cd skills-library/[domain]/[skill_name]
```

### 3. Write `skill.json`

Follow the schema in `schemas/skill_definition.json`. Required fields:

```json
{
  "id": "domain_skill_name",
  "version": "1.0.0",
  "name": "Human Readable Name",
  "description": "Clear description of what this skill does",
  "domain": "your_domain",
  "tools": [
    {
      "name": "tool.action",
      "required": true
    }
  ],
  "inputSchema": {
    "type": "object",
    "properties": {
      // Define expected inputs
    }
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      // Define outputs
    }
  },
  "tags": ["tag1", "tag2"],
  "platforms": {
    "claude": {
      "triggers": ["help with Your Skill Name"]
    }
  }
}
```

### 4. Write `instructions.md`

Provide clear execution instructions:

```markdown
# Skill Name

## Purpose

What this skill accomplishes and when to use it.

## Prerequisites

- Required tools or access
- Dependencies on other skills

## Execution Steps

1. Step-by-step instructions
2. Expected inputs
3. Expected outputs

## Example Usage

\`\`\`
// Example invocation
\`\`\`

## Error Handling

Common errors and how to resolve them.

## Security Considerations

Any security implications or data access.
```

### 5. Run Security Analysis

```bash
python scripts/analyze_skills.py --action metadata
```

This generates `metadata.yaml` with security analysis:

- Risk level assessment
- Security requirements
- Job function categorization
- JTBD mapping

### 6. Validate Your Skill

```bash
# Validate against schema (future tool)
npm run validate:skill skills-library/[domain]/[skill_name]/skill.json
```

### 7. Test Your Skill

- Test standalone execution
- Verify input/output schemas
- Check error handling
- Test with different inputs

### 8. Submit Pull Request

```bash
git checkout -b add-skill-[skill_name]
git add skills-library/[domain]/[skill_name]
git commit -m "feat: add [skill_name] skill to [domain]"
git push origin add-skill-[skill_name]
```

**PR Description Template:**

```markdown
## Skill Addition: [Skill Name]

**Domain:** [domain]
**Risk Level:** [Low/Medium/High/Critical]
**Job Function:** [function]

### Description

Brief description of what the skill does.

### Security Analysis

- Risk factors identified
- Security requirements needed
- Data access scope

### Testing

- [ ] Tested standalone execution
- [ ] Validated input/output schemas
- [ ] Ran security analysis
- [ ] Added to appropriate workflows (if applicable)

### Checklist

- [ ] skill.json follows schema
- [ ] instructions.md is complete
- [ ] metadata.yaml generated
- [ ] No security vulnerabilities
```

## Security Auditing

### Reviewing Existing Skills

To audit skills for security issues:

1. **Run Analysis:**

   ```bash
   python scripts/analyze_skills.py --action report
   ```

2. **Review Report:**
   Check `reports/security_analysis.md` for:
   - Skills flagged for review (tier 1 or elevated)
   - Missing security requirements
   - Potential vulnerabilities

3. **Update Security Requirements:**
   Edit `metadata.yaml` to add:

   ```yaml
   security:
     risk_level: 'High'
     requirements:
       sandboxing_required: true
       human_in_loop_required: true
       audit_logging: true
       data_access_scope:
         - 'pii'
         - 'financial'
   ```

4. **Submit Security PR:**
   ```bash
   git checkout -b security-audit-[skill_name]
   git add skills-library/[domain]/[skill_name]/metadata.yaml
   git commit -m "security: add security requirements to [skill_name]"
   ```

### Security Review Criteria

When reviewing skills, check for:

- [ ] **Data Access**: Does it access sensitive data?
- [ ] **Write Operations**: Can it modify or delete data?
- [ ] **External Calls**: Does it call external APIs?
- [ ] **Credentials**: Does it handle authentication?
- [ ] **Financial**: Does it process payments or revenue data?
- [ ] **PII**: Does it access personally identifiable information?

If any are true, the skill needs appropriate security controls.

## Creating Workflows

### 1. Design Workflow

Identify:

- Skills to chain together
- Data flow between steps
- Error handling strategy
- Approval requirements

### 2. Playbook-ready blueprints (recommended)

To keep new workflows consistent with the cookbook’s **niche playbooks**, blueprints can include:

- **`icp`** — Ideal Customer Profile (e.g. company size, motion, team size, priorities). See [Playbooks](docs/PLAYBOOKS.md) and existing blueprints in `registry/blueprints/`.
- **`integration_reference`** — Optional link to reference schemas that define exact data to wire (CRM, billing). See [registry/integration_schemas/README.md](registry/integration_schemas/README.md) for format and existing Salesforce, HubSpot, and Stripe schemas.
- **`opinionated_prompts`** per step — Optional `system_context` and `input_guidance` on each `chain_sequence` item so the chain is opinionated for the target ICP.

The schema is in `schemas/workflow_blueprint.json`; all of these fields are optional. Use `scripts/recipe_to_blueprint.py --icp stub --integration-refs stub --opinionated-prompts` to generate a playbook-ready stub, or add them manually.

### 3. Write Blueprint YAML

Follow `schemas/workflow_blueprint.json`:

```yaml
id: workflow_your_workflow_name
version: 1.0.0
name: 'Your Workflow Name'
description: 'What this workflow accomplishes'

chain_sequence:
  - step_id: 'step_1'
    skill_id: 'skill_to_execute'
    action: 'action_name'
    input_mapping:
      static_values:
        key: 'value'
    error_handling:
      on_failure: 'stop'
      max_retries: 2

  - step_id: 'step_2'
    skill_id: 'next_skill'
    action: 'action_name'
    input_mapping:
      from_step: 'step_1'
      field_mappings:
        output_field: 'input.field'

logic_gates:
  parallel_groups:
    - group_id: 'parallel_tasks'
      step_ids:
        - 'step_3'
        - 'step_4'
      wait_for_all: true

security_context:
  max_risk_level: 'Medium'
  requires_approval: false
```

### 4. Validate Workflow

```bash
# Validate blueprint (future tool)
npm run validate:workflow registry/blueprints/your_workflow.yaml
```

### 5. Test Workflow

- Validate all skills exist
- Test with sample data
- Verify error handling
- Check security requirements

### 6. Submit Workflow PR

Same process as skill addition, but in `registry/blueprints/`.

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js 18+
- Git

### Install Dependencies

```bash
# Python dependencies
pip install pyyaml jsonschema

# Node dependencies
npm install
```

### Run Tests

```bash
# Validate all skills
python scripts/analyze_skills.py --action analyze

# Run schema validation (future)
npm test
```

### Pre-flight check (before pushing to the public remote)

Before pushing to the public remote (e.g. open-sourcing or publishing a release), run the full pre-flight suite so CI and open-source hygiene checks pass in one go:

```bash
./scripts/pre_release_check.sh
```

Or, if you use the npm script: `npm run preflight`

This runs metrics consistency, schema validation (skills, metadata, workflows), linting, tests, security (including optional secrets scan), documentation and community file checks, and SPDX headers. Install **trufflehog** or **gitleaks** for secrets scanning; optional **markdown-link-check** for link validation.

### Pre-commit Hooks

```bash
# Setup pre-commit hooks (future)
npm run setup:hooks
```

This will automatically:

- Validate skill.json against schema
- Run security analysis
- Check for malicious code patterns

## Code of Conduct

All contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating in the project.

## Questions?

- 📖 Read [ARCHITECTURE.md](ARCHITECTURE.md) for design details
- 🔒 Read [SECURITY_POLICY.md](SECURITY_POLICY.md) for security guidelines
- 🤝 Read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards
- 💬 Open an issue for questions
- 📧 Email: community@skene.ai

Thank you for contributing to the Skills Directory! 🎉
