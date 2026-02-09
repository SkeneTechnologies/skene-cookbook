# Skills Directory Architecture

## Atomic Skill Philosophy

The Skills Directory is built on the principle of **atomic, composable skills** — small, focused units of work that can be executed independently or chained together to form complex workflows.

### Core Principles

1. **Atomicity**: Each skill performs one job well
2. **Composability**: Skills can be chained together seamlessly
3. **Security First**: Every skill is analyzed for security risks
4. **Machine Readable**: All definitions follow strict JSON schemas
5. **Human Understandable**: Clear documentation and metadata

## Architecture Overview

```
skene-skills-directory/
├── core/                          # System logic
│   ├── analyzer/                  # Security and categorization analysis
│   ├── validator/                 # Schema validation
│   └── orchestrator/              # Workflow execution engine
├── registry/                      # Organized skill registry
│   ├── job_functions/             # Skills organized by job function
│   │   ├── index.json            # Job function → skills mapping
│   │   └── [function]/           # Individual function directories
│   ├── blueprints/               # Workflow chain definitions
│   │   └── *.yaml                # Workflow blueprint files
│   └── skills/                    # (Future: normalized skill storage)
├── skills-library/               # Raw skill library (800+ skills)
│   ├── [domain]/                 # Domain-based organization
│   │   └── [skill]/
│   │       ├── skill.json        # Skill definition
│   │       ├── instructions.md   # Execution instructions
│   │       └── metadata.yaml     # Security & categorization metadata
│   └── index.json                # Master index
├── schemas/                       # JSON Schema definitions
│   ├── skill_definition.json     # Skill structure schema
│   └── workflow_blueprint.json   # Workflow chain schema
└── scripts/                       # Automation tooling
    └── analyze_skills.py         # Security & categorization analyzer
```

## Data Layer

### Skill Definition (`skill.json`)

Every skill has a `skill.json` file containing:
- **Identity**: id, version, name, description
- **Categorization**: domain, job_function, JTBD
- **Security**: risk level, requirements, data access scope
- **Interface**: input/output schemas (JSON Schema)
- **Dependencies**: required tools and other skills
- **Composability**: which skills it can chain with
- **Execution**: temperature, platforms, triggers

See `schemas/skill_definition.json` for the complete schema.

### Workflow Blueprint (`*.yaml`)

Workflows define how skills are chained together:
- **Chain Sequence**: ordered steps with input/output mapping
- **Logic Gates**: conditional branching, parallel execution
- **Error Handling**: retries, fallbacks, rollbacks
- **Security Context**: approval requirements, risk limits

See `schemas/workflow_blueprint.json` and `registry/blueprints/example_workflow.yaml`.

## Security Framework

### Risk Levels

- **Low**: Read-only operations, public data access
- **Medium**: Write operations, internal data, external APIs
- **High**: Modify/delete operations, PII access, sensitive data
- **Critical**: Financial data, credential access, destructive operations

### Security Requirements

Based on risk level, skills may require:
- **Sandboxing**: Execute in isolated environment
- **Human-in-loop**: Require approval before execution
- **Audit Logging**: Log all executions for compliance
- **Data Access Scope**: Explicit declaration of data types accessed

### Analysis Process

The `analyze_skills.py` script:
1. Parses skill definitions and instructions
2. Identifies security keywords and risky operations
3. Assigns risk levels and generates requirements
4. Creates `metadata.yaml` with security analysis
5. Generates security reports and indices

## Jobs to be Done (JTBD) Framework

Every skill is mapped to a JTBD structure:
- **Job**: The functional job the skill performs
- **Context**: When/where the job occurs
- **Outcome**: Desired outcome/success criteria

This enables:
- Discovery by user intent rather than technical implementation
- Better skill recommendations
- Workflow optimization based on outcome alignment

## Job Functions

Skills are categorized by primary job function:
- Engineering, Marketing, Sales, Customer Success
- Product, Finance, Legal, HR
- Operations, Executive, Security, Data, Design

This enables role-based filtering and recommendations.

## Composability System

Skills declare how they can be composed:
- **Exit States**: Named states that trigger other skills
- **Output Schema**: Structured data other skills can consume
- **Dependencies**: Skills that must run first
- **Compatibility**: Explicit "can chain with" declarations

Workflows use this metadata to:
- Validate chain sequences
- Map data between steps
- Suggest optimal skill combinations

## Execution Model

### Standalone Execution
Single skill execution with direct input/output.

### Workflow Execution
Multi-skill chain with:
- Sequential steps with data flow
- Parallel execution groups
- Conditional branching (decision points)
- Error handling and retries

### Orchestration
The orchestrator (future):
- Validates workflow blueprints
- Manages execution state
- Handles failures and retries
- Enforces security requirements
- Logs audit trail

## Extension Points

### Adding New Skills
1. Create skill directory in appropriate domain
2. Write `skill.json` following schema
3. Add `instructions.md` with execution details
4. Run analyzer to generate `metadata.yaml`
5. Test skill independently
6. Add to appropriate workflow blueprints

### Creating Workflows
1. Identify skill sequence
2. Write blueprint YAML following schema
3. Define input/output mappings
4. Add error handling
5. Set security context
6. Validate against schema
7. Test end-to-end

### Security Auditing
1. Run `analyze_skills.py --action analyze`
2. Review security report
3. Identify high-risk skills
4. Add human-in-loop requirements
5. Update security requirements
6. Re-validate workflows

## Design Philosophy

### Scannability
- Clear file structure
- Consistent naming
- Rich metadata
- Self-documenting schemas

### Modularity
- Loose coupling between skills
- Well-defined interfaces
- Independent testing
- Incremental deployment

### Security by Design
- Risk analysis automation
- Explicit security requirements
- Approval workflows
- Audit logging

### Open Source Ready
- Clear contribution guidelines
- Schema-driven development
- Automated validation
- Comprehensive documentation

## Next Steps

See `CONTRIBUTING.md` for contribution guidelines.
