#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# Functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_check() {
    echo -e "${BLUE}[CHECK]${NC} $1"
}

print_pass() {
    echo -e "${GREEN}[✓]${NC} $1"
    PASSED=$((PASSED + 1))
}

print_fail() {
    echo -e "${RED}[✗]${NC} $1"
    FAILED=$((FAILED + 1))
}

print_warn() {
    echo -e "${YELLOW}[!]${NC} $1"
    WARNINGS=$((WARNINGS + 1))
}

# Main checks
print_header "Skene Cookbook Pre-Release Verification"

# 1. Check if we're in the right directory
print_check "Verifying repository structure..."
if [ ! -f "package.json" ] || [ ! -f "README.md" ]; then
    print_fail "Not in skene-cookbook root directory"
    exit 1
fi
print_pass "Repository structure verified"

# 2. Check for uncommitted changes
print_check "Checking for uncommitted changes..."
if [[ -n $(git status --porcelain) ]]; then
    print_warn "Uncommitted changes found - should commit before release"
else
    print_pass "Working tree is clean"
fi

# 3. Metrics consistency (README/directory counts and badges)
print_header "Registry & Metrics Consistency"

print_check "Verifying metrics consistency (skill counts, badges)..."
if npm run verify:metrics &> /dev/null; then
    print_pass "Metrics consistent with registry"
else
    print_fail "Metrics out of sync - run: npm run verify:metrics"
fi

# 4. Schema validation (skills, metadata, workflows)
print_check "Validating schemas (skills, metadata, workflows)..."
if python3 scripts/validate_schemas.py &> /dev/null; then
    print_pass "All schemas valid"
else
    print_fail "Schema validation failed - run: python3 scripts/validate_schemas.py"
fi

# 5. Check Python linting
print_header "Python Code Quality"

print_check "Running Black (formatting)..."
if (black --check . &> /dev/null) || (python3 -m black --check . &> /dev/null); then
    print_pass "Black formatting check passed"
else
    print_fail "Black formatting issues found - run: black . or python3 -m black ."
fi

print_check "Running Flake8 (linting)..."
if (flake8 . &> /dev/null) || (python3 -m flake8 . &> /dev/null); then
    print_pass "Flake8 linting passed"
else
    print_fail "Flake8 linting issues found - run: flake8 ."
fi

print_check "Running isort (import sorting)..."
if (isort --check-only . &> /dev/null) || (python3 -m isort --check-only . &> /dev/null); then
    print_pass "isort check passed"
else
    print_fail "isort issues found - run: isort . or python3 -m isort ."
fi

# 6. Check JavaScript linting
print_header "JavaScript Code Quality"

print_check "Running ESLint..."
if npm run lint:js &> /dev/null; then
    print_pass "ESLint passed"
else
    print_fail "ESLint issues found - run: npm run lint:js:fix"
fi

print_check "Running Prettier (formatting)..."
if npm run format:check &> /dev/null; then
    print_pass "Prettier formatting check passed"
else
    print_fail "Prettier formatting issues found - run: npm run format"
fi

# 7. Check tests
print_header "Test Suite"

print_check "Running unit tests..."
if (pytest tests/unit -v --tb=short -m "not slow" --no-cov &> /dev/null) || (python3 -m pytest tests/unit -v --tb=short -m "not slow" --no-cov &> /dev/null); then
    print_pass "Unit tests passed"
else
    print_fail "Unit tests failed - run: pytest tests/unit -v --no-cov"
fi

print_check "Running integration tests..."
if (pytest tests/integration -v --tb=short -m "not slow" --no-cov &> /dev/null) || (python3 -m pytest tests/integration -v --tb=short -m "not slow" --no-cov &> /dev/null); then
    print_pass "Integration tests passed"
else
    print_fail "Integration tests failed - run: pytest tests/integration -v --no-cov"
fi

print_check "Checking test coverage..."
COVERAGE=$(pytest --cov --cov-report=term-missing -q 2>/dev/null | grep "TOTAL" | awk '{print $4}' | sed 's/%//')
if [ -z "$COVERAGE" ]; then
    COVERAGE=$(python3 -m pytest --cov --cov-report=term-missing -q 2>/dev/null | grep "TOTAL" | awk '{print $4}' | sed 's/%//')
fi
if [ -n "$COVERAGE" ]; then
    if (( $(echo "$COVERAGE >= 60" | bc -l 2>/dev/null || echo 0) )); then
        print_pass "Test coverage: ${COVERAGE}% (meets 60% target)"
    elif (( $(echo "$COVERAGE >= 30" | bc -l 2>/dev/null || echo 0) )); then
        print_pass "Test coverage: ${COVERAGE}% (meets 30% minimum)"
    else
        print_warn "Test coverage: ${COVERAGE}% (below 30% minimum)"
    fi
else
    print_warn "Could not determine test coverage"
fi

# 8. Check security
print_header "Security Checks"

print_check "Checking for skills flagged for review (tier 1)..."
if python3 scripts/analyze_skills.py --action analyze &> /dev/null; then
    if grep -q "Critical" reports/security_analysis.md 2>/dev/null; then
        print_warn "Skills flagged for review present - see reports/security_analysis.md (warn only)"
    else
        print_pass "No skills flagged for review (tier 1)"
    fi
else
    print_warn "Could not run security analysis"
fi

print_check "Checking npm dependencies for vulnerabilities..."
if npm audit --audit-level=moderate &> /dev/null; then
    print_pass "No moderate or higher npm vulnerabilities"
else
    print_fail "npm vulnerabilities found - run: npm audit"
fi

print_check "Scanning for secrets (trufflehog/gitleaks)..."
if command -v trufflehog &> /dev/null; then
    if trufflehog filesystem . --only-verified &> /dev/null; then
        print_pass "No verified secrets detected (trufflehog)"
    else
        print_fail "Potential secrets detected - run: trufflehog filesystem . --only-verified"
    fi
elif command -v gitleaks &> /dev/null; then
    if gitleaks detect --no-git --source . --verbose &> /dev/null; then
        print_pass "No secrets detected (gitleaks)"
    else
        print_fail "Potential secrets detected - run: gitleaks detect --source ."
    fi
else
    print_warn "No secrets scanner found (install trufflehog or gitleaks for open-source push)"
fi

# 9. Check documentation
print_header "Documentation"

print_check "Verifying key documentation (validate_docs.py)..."
if python3 scripts/validate_docs.py &> /dev/null; then
    print_pass "All required docs present"
else
    print_fail "Missing required docs - run: python3 scripts/validate_docs.py"
fi

print_check "Checking markdown links (validate_docs.py --links)..."
if python3 scripts/validate_docs.py --links &> /dev/null; then
    print_pass "Markdown links checked"
else
    print_warn "Link check skipped or failed (run: python3 scripts/validate_docs.py --links)"
fi

# 10. Check community infrastructure
print_header "Community Infrastructure"

print_check "Verifying issue templates..."
TEMPLATE_COUNT=$(find .github/ISSUE_TEMPLATE -name "*.yml" 2>/dev/null | wc -l | tr -d ' ')
if [ "$TEMPLATE_COUNT" -ge 4 ]; then
    print_pass "Issue templates exist ($TEMPLATE_COUNT files)"
else
    print_fail "Missing issue templates (found $TEMPLATE_COUNT, expected ≥4)"
fi

print_check "Verifying pull request template..."
if [ -f ".github/pull_request_template.md" ]; then
    print_pass "Pull request template exists"
else
    print_fail "Pull request template not found"
fi

# 11. Check SPDX headers
print_header "License Headers"

print_check "Checking SPDX headers in source files..."
PYTHON_FILES=$(find scripts eval_harness -name "*.py" -not -path "*/__pycache__/*" 2>/dev/null | wc -l | tr -d ' ')
PYTHON_HEADERS=$(grep -r "SPDX-License-Identifier" scripts eval_harness --include="*.py" 2>/dev/null | wc -l | tr -d ' ')
JS_FILES=$(find bin -name "*.js" 2>/dev/null | wc -l | tr -d ' ')
JS_HEADERS=$(grep -r "SPDX-License-Identifier" bin --include="*.js" 2>/dev/null | wc -l | tr -d ' ')

if [ "$PYTHON_HEADERS" -ge "$PYTHON_FILES" ] && [ "$JS_HEADERS" -ge "$JS_FILES" ]; then
    print_pass "SPDX headers present in source files"
else
    print_fail "Missing SPDX headers (Python: $PYTHON_HEADERS/$PYTHON_FILES, JS: $JS_HEADERS/$JS_FILES)"
fi

# 12. Final summary
print_header "Summary"

echo -e "${GREEN}Passed:${NC}   $PASSED checks"
echo -e "${RED}Failed:${NC}   $FAILED checks"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS checks"
echo ""

if [ $FAILED -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}✓ All checks passed! Ready for release.${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠ All critical checks passed, but review warnings before release.${NC}"
        exit 0
    fi
else
    echo -e "${RED}✗ $FAILED check(s) failed. Fix issues before release.${NC}"
    exit 1
fi
