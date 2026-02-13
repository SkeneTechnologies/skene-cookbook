# End-to-End (E2E) Testing Guide

Complete guide for E2E testing before public release of Skills Directory.

## Quick Start

```bash
# Run all E2E tests
pytest tests/e2e -v

# Run full E2E validation suite
./scripts/run_e2e_tests.sh

# Run cross-platform tests (requires Docker)
./scripts/test_cross_platform.sh
```

## E2E Test Categories

### 1. Fresh Installation Tests

**File**: `test_fresh_install.py`

Simulates new user installation experience:

- Dependency installation
- Script execution
- Skills library accessibility
- Registry structure validation
- Documentation availability

**Run**: `pytest tests/e2e/test_fresh_install.py -v`

### 2. User Workflow Tests

**File**: `test_user_workflows.py`

Tests complete user journeys:

- First-time user experience
- Data analyst workflow (deduplication)
- Security auditor workflow (risk analysis)
- Workflow engineer (chaining)

**Run**: `pytest tests/e2e/test_user_workflows.py -v`

### 3. Security Readiness Tests

**File**: `test_fresh_install.py::TestSecurityReadiness`

Pre-release security validation:

- No .env files committed
- .gitignore comprehensive
- No hardcoded secrets
- Cross-file consistency

**Run**: `pytest tests/e2e/test_fresh_install.py::TestSecurityReadiness -v`

## Automated Test Scripts

### Full E2E Test Suite

```bash
./scripts/run_e2e_tests.sh
```

**Tests**:

- ✅ Environment & dependencies
- ✅ Project structure
- ✅ Automated test suite (unit, integration, E2E)
- ✅ Security scanning
- ✅ Performance benchmarks
- ✅ Documentation quality
- ✅ CLI functionality

**Output**: Pass/fail with detailed report

### Cross-Platform Testing

```bash
./scripts/test_cross_platform.sh
```

**Platforms tested**:

- Ubuntu 22.04 LTS
- Ubuntu 24.04 LTS
- Python 3.9 (Debian)
- Python 3.10 (Debian)
- Python 3.11 (Debian)
- Python 3.12 (Debian)

**Requirements**: Docker installed

## Pre-Release Checklist

### Pre-flight (single command before pushing to public remote)

Run the full pre-flight suite so the first post-push CI run stays green and open-source hygiene is verified:

```bash
./scripts/pre_release_check.sh
# or: npm run preflight
```

This covers metrics consistency, schema validation, linting, unit and integration tests, coverage, security (including optional secrets scan), docs and community files, and SPDX headers. Optional: install **trufflehog** or **gitleaks** for secrets scanning.

### Phase 1: Local Validation (Day -7)

```bash
# 1. Run full test suite
pytest tests/ -v --cov

# 2. Check coverage
pytest --cov=scripts --cov-report=html
open htmlcov/index.html

# 3. Run E2E tests
pytest tests/e2e -v

# 4. Run full E2E validation
./scripts/run_e2e_tests.sh
```

**Gate**: All tests pass, coverage ≥ 80%

### Phase 2: Security Audit (Day -6)

```bash
# 1. Scan for secrets
trufflehog filesystem . --only-verified

# 2. Check dependencies
pip-audit

# 3. Security linting
bandit -r scripts/ -ll

# 4. Validate .gitignore
grep -E "\.env|__pycache__|\.pyc" .gitignore
```

**Gate**: No secrets, no critical vulnerabilities

### Phase 3: Cross-Platform (Day -5)

```bash
# Test on multiple platforms
./scripts/test_cross_platform.sh
```

**Gate**: ≥ 80% platform success rate

### Phase 4: Performance Validation (Day -4)

```bash
# Run performance tests with full dataset
pytest tests/performance -v

# Profile memory usage
python -m memory_profiler scripts/dedupe_skills.py
```

**Gate**: Meets performance benchmarks

### Phase 5: Documentation Review (Day -3)

```bash
# Verify required docs exist and check markdown links
python3 scripts/validate_docs.py
python3 scripts/validate_docs.py --links
```

Doc and link validation are also run as part of the pre-flight suite (`./scripts/pre_release_check.sh`).

**Gate**: All required docs present, no broken links

### Phase 6: Beta Testing (Day -2 to Day 0)

```bash
# Create RC tag
git tag v1.0.0-rc1

# Deploy to beta testers
# Collect feedback
# Fix critical issues
```

**Gate**: No critical bugs, positive feedback

### Phase 7: Final Validation (Day 0)

```bash
# Run complete validation
./scripts/run_e2e_tests.sh

# Verify all gates passed
# Tag release
git tag v1.0.0

# Push to GitHub
git push origin main --tags
```

**Gate**: All previous gates passed

## Manual Testing Scenarios

### Scenario 1: Fresh Ubuntu Install

```bash
# On fresh Ubuntu 22.04 system
sudo apt update
sudo apt install -y python3 python3-pip git

git clone https://github.com/username/skene-cookbook.git
cd skene-cookbook

pip3 install -r requirements.txt
python3 scripts/dedupe_skills.py --help

# Expected: Help message displays without errors
```

### Scenario 2: First-Time User

```bash
# User reads README and follows quick start
cat README.md

# User explores skills
python3 skill-loom-cli.py

# User runs analysis
python3 scripts/analyze_skills.py
python3 scripts/dedupe_skills.py
python3 scripts/generate_blueprints.py

# Expected: All commands work, reports generated
```

### Scenario 3: Data Analyst

```bash
# Analyst wants to find duplicate skills
python3 scripts/dedupe_skills.py

# Review report
cat reports/dedupe_report.json | jq '.summary'

# Analyst wants to see high-similarity pairs
cat reports/dedupe_report.json | jq '.similar_pairs | length'

# Expected: Clear, actionable insights
```

### Scenario 4: Security Auditor

```bash
# Auditor runs security analysis
python3 scripts/analyze_skills.py

# Review critical risks
cat reports/security_analysis.md | grep "Critical"

# Check security requirements
grep -A5 "security_requirements" registry/job_functions/index.json

# Expected: Clear risk levels, security guidance
```

## Troubleshooting E2E Tests

### Tests Fail on Import

```bash
# Add project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd):$(pwd)/scripts"

# Retry tests
pytest tests/e2e -v
```

### Docker Tests Fail

```bash
# Check Docker is running
docker ps

# Test Docker access
docker run hello-world

# Check volume mounting
docker run -v $(pwd):/test ubuntu ls /test
```

### Performance Tests Too Slow

```bash
# Skip slow tests during development
pytest tests/e2e -m "not slow"

# Run performance tests separately
pytest tests/performance -v
```

### Coverage Below Threshold

```bash
# Identify uncovered code
pytest --cov=scripts --cov-report=term-missing

# Focus on critical paths first
pytest tests/unit/test_dedupe_skills.py --cov=scripts/dedupe_skills.py
```

## Best Practices

### 1. Test Early, Test Often

- Run E2E tests before every commit
- Use pre-commit hooks for quick validation
- CI/CD runs full suite on every PR

### 2. Isolate Test Environments

- Use Docker for clean-room testing
- Don't test on development machines
- Use temporary directories

### 3. Document Failures

- Capture logs for failed tests
- Document workarounds
- Create issues for recurring failures

### 4. Monitor Real Usage

- After release, track real usage patterns
- Compare to E2E test scenarios
- Update tests based on user feedback

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: E2E Tests

on:
  pull_request:
    branches: [main]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements-test.txt

      - name: Run E2E tests
        run: pytest tests/e2e -v

      - name: Run full validation
        run: ./scripts/run_e2e_tests.sh
```

## Success Metrics

### Release Readiness Score

| Category       | Weight | Target           | Status |
| -------------- | ------ | ---------------- | ------ |
| Functionality  | 20%    | 100% pass        | ⏳     |
| Security       | 20%    | 0 critical       | ⏳     |
| Performance    | 15%    | Meets benchmarks | ⏳     |
| Documentation  | 15%    | Complete         | ⏳     |
| Cross-platform | 15%    | ≥80% platforms   | ⏳     |
| User testing   | 15%    | ≥80% approval    | ⏳     |

**Minimum Score**: 85/100 for release approval

## Resources

- **E2E Testing Strategy**: [docs/internal/E2E_TESTING_STRATEGY.md](../../docs/internal/E2E_TESTING_STRATEGY.md) (maintainers)
- **Unit Testing Guide**: `tests/README.md`
- **CI/CD Configuration**: `.github/workflows/lint-and-build.yml`
- **Security Policy**: `SECURITY.md`

## Support

For E2E testing issues:

1. Check troubleshooting section above
2. Review test logs in `/tmp/`
3. Run with verbose output: `pytest -vv`
4. Create GitHub issue with logs

---

**Status**: E2E Testing Framework Ready
**Last Updated**: February 5, 2025
