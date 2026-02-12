# Changelog

All notable changes to the Skene Cookbook project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub issue templates (bug report, feature request, skill proposal, security)
- Pull request template with comprehensive checklists
- Code of Conduct as standalone document
- CHANGELOG.md for tracking project changes

### Changed
- Extract Code of Conduct from CONTRIBUTING.md to standalone file
- Update README.md with Code of Conduct link

## [0.1.0] - 2026-02-11

### Added - Core Infrastructure
- 760+ AI agent skills across 23 domains:
  - 156 Sales/Marketing/RevOps skills
  - 51 E-commerce/PLG skills
  - 40 Customer Success skills
  - 33 Finance/FinOps skills
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

This is the first public release of Skene Cookbook, featuring a comprehensive library of 760+ AI agent skills, complete evaluation infrastructure, and extensive documentation.

**Key Highlights:**
- Production-ready skills across 23 domains
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
