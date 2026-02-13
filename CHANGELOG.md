# Changelog

All notable changes to the Skene Cookbook project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- METRICS.md - Canonical source of truth for all skill counts and methodology
- Metric badges in README.md (total skills, executable, context, domains)
- Automated verification for documentation accuracy (sync_metrics.cjs)
- GitHub Action for documentation verification in CI/CD
- **Niche playbooks**: Workflow blueprints with ICP, integration references, and opinionated prompts per step (schemas and all 15 blueprints)
- PLAYBOOKS.md and recipe-to-blueprint index (registry/recipe_blueprint_index.json)
- Integration reference schemas (registry/integration_schemas/): Salesforce, HubSpot, Stripe for exact data to wire
- Pre-flight test suite (scripts/pre_release_check.sh): metrics, schema validation, lint, tests, security, secrets scan, doc/link check; `npm run preflight`
- scripts/validate_docs.py for documentation and link validation (E2E/pre-flight)

### Changed

- **Documentation Accuracy Update**: All documentation now uses accurate skill counts
  - Total: 764 resources (382 executable + 382 reference guides)
  - Domains: 23 (21 executable + 2 context)
  - Context breakdown: 241 cursor rules + 141 scientific
- README.md - "What's Included" with playbooks, blueprints, and integration schemas; pre-flight note
- skills-library/README.md - Updated to reflect accurate counts and link to METRICS.md
- SKILLS_CATALOG.md - Updated all domain counts and added context/executable separation
- index.json - Rebuilt with complete metrics section and accurate totals
- Skill chain recipe count: **36 recipes** (SKILL_CHAINS.md, README, PLAYBOOKS); 15 workflow blueprints
- CI and pre-flight: Critical risk skills no longer fail the build (warn only; catalog retained)

### Fixed

- Documentation discrepancies across multiple files (README, SKILLS_CATALOG, index.json)
- Inconsistent skill counting methodology (now documented in METRICS.md)
- Missing reference guides in summary counts (cursor_rules: 241, scientific: 141)
- E2E README reference to validate_docs.py (script added and wired)

## [0.1.1] - 2026-02-12

### Added

- GitHub issue templates (bug report, feature request, skill proposal, security)
- Pull request template with comprehensive checklists
- Code of Conduct as standalone document
- LICENSES.txt with dependency license documentation
- Pre-commit hooks configuration (.pre-commit-config.yaml)
- Python linting configuration (Black, Flake8, isort)
- JavaScript linting configuration (ESLint, Prettier)

### Changed

- Extract Code of Conduct from CONTRIBUTING.md to standalone file
- Update README.md with Code of Conduct link and setup instructions

### Fixed

- CI/CD quality gates now properly fail on issues (not just warnings)

## [0.1.0] - 2026-02-11

### Added - Core Infrastructure

- 764 AI agent resources across 23 domains (382 executable + 382 reference guides):
  - 52 Marketing skills (content, SEO, campaigns)
  - 70 PLG skills (product-led growth, activation)
  - 29 Customer Success skills (health scoring, churn prevention)
  - 25 RevOps skills (sales pipeline, forecasting)
  - 241 Cursor rules (technology-specific IDE guidelines)
  - 141 Scientific computing skills (research, bioinformatics)
  - 40+ standardized tool integrations
- Eval harness infrastructure for skill validation and testing
  - Automated test data generation
  - Schema validation framework
  - Decision engine for skill evaluation
  - Batch evaluation capabilities
  - Security analysis and risk assessment
- Security analysis framework with risk level classification
- 20+ ready-to-use skill chain recipes
- CLI for skill management (`npx skills-directory`)
- Auto-activation during npm install (Cursor + Claude)
- Ecosystem generator for tailored recommendations

### Added - Documentation

- Comprehensive README with value proposition and ROI
- Architecture guide (ARCHITECTURE.md)
- Security policy (SECURITY_POLICY.md)
- Contributing guidelines (CONTRIBUTING.md)
- Quick wins guide (QUICK_WINS.md)
- Skill chains cookbook (SKILL_CHAINS.md)
- Persona-specific guides (Sales, Growth PM, Researcher, CFO)
- Complete skills directory documentation
- Troubleshooting guide
- Build your first skill tutorial

### Added - Testing & Quality

- Unit test framework with pytest
- Test coverage reporting
- Schema validation tests
- GitHub Actions CI/CD workflow (lint-and-build.yml)
- Security scanning for skills

### Added - Features

- Skills installed to `~/.cursor/skills/` and `~/.claude/skills/`
- Skills persist between sessions
- Installation status verification
- File integrity checking
- Auto-skip installation in CI/CD environments
- Manual installation controls

### Changed

- Rebranded from "Skills Directory" to "Skene Cookbook"
- Updated repository name to `skene-cookbook`
- Improved postinstall welcome message
- Enhanced error handling and logging

### Fixed

- Peer dependency warnings for zod and react
- Postinstall visibility in GitHub installations
- Skill count discrepancies (accurate 764 count)
- Broken documentation links
- GitHub workflow test failures

### Security

- Risk level classification for all skills (Low/Medium/High/Critical)
- Security requirements analysis
- Sandboxing recommendations for high-risk skills
- Human-in-the-loop requirements for critical operations
- Audit logging capabilities

## [0.0.1] - 2024-02-XX (Initial Development)

### Added

- Initial project structure
- First skill definitions
- Basic CLI implementation
- Initial documentation

---

## Release Notes

### Version 0.1.0 - Initial Public Release

This is the first public release of Skene Cookbook, featuring a comprehensive library of 764 AI agent resources (382 executable skills + 382 reference guides), complete evaluation infrastructure, and extensive documentation.

**Key Highlights:**

- Production-ready skills across 23 domains
- 382 executable AI agent skills + 382 reference guides
- 241 cursor rules for IDE-specific guidance
- 141 scientific computing skills
- Comprehensive evaluation harness for quality assurance
- Security-first approach with risk classification
- Extensive documentation and quick-start guides
- Auto-activation for seamless developer experience

**Breaking Changes:** None (initial release)

**Upgrade Notes:** This is the initial public release. Future releases will include upgrade instructions here.

**Known Issues:**

- Test coverage is currently 7.76% (target: 60%+) - improvements planned for v0.2.0
- Some skills lack comprehensive integration tests
- CI/CD warnings don't fail builds (will be addressed in v0.2.0)

**Roadmap for v0.2.0:**

- Increase test coverage to 60%+
- Add Python linting (Black, Flake8, isort)
- Add JavaScript linting (ESLint, Prettier)
- Add pre-commit hooks
- Implement branch protection
- Expand integration tests

---

[Unreleased]: https://github.com/SkeneTechnologies/skene-cookbook/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/SkeneTechnologies/skene-cookbook/releases/tag/v0.1.0
[0.0.1]: https://github.com/SkeneTechnologies/skene-cookbook/releases/tag/v0.0.1
