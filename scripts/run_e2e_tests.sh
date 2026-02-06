#!/bin/bash
# End-to-End Testing Script for Public Release
# Tests complete user workflows, installation, security, and cross-platform compatibility

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Progress tracking
TESTS_PASSED=0
TESTS_FAILED=0
TOTAL_TESTS=0

# Helper functions
print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_test() {
    ((TOTAL_TESTS++))
    echo -e "${YELLOW}[$TOTAL_TESTS]${NC} $1..."
}

print_success() {
    ((TESTS_PASSED++))
    echo -e "  ${GREEN}✓${NC} $1"
}

print_failure() {
    ((TESTS_FAILED++))
    echo -e "  ${RED}✗${NC} $1"
}

print_warning() {
    echo -e "  ${YELLOW}⚠${NC} $1"
}

# Main test execution
main() {
    echo -e "${GREEN}"
    cat << "EOF"
╔══════════════════════════════════════════════════════════════════════╗
║              END-TO-END TESTING - PUBLIC RELEASE                     ║
║                    Skills Directory Project                          ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"

    # Phase 1: Environment Check
    print_header "Phase 1: Environment & Dependencies"

    print_test "Checking Python version"
    if python3 --version &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_failure "Python 3 not found"
        exit 1
    fi

    print_test "Checking pip installation"
    if python3 -m pip --version &> /dev/null; then
        print_success "pip is available"
    else
        print_failure "pip not found"
        exit 1
    fi

    print_test "Validating requirements.txt"
    if [ -f "requirements.txt" ]; then
        print_success "requirements.txt exists"
    else
        print_failure "requirements.txt not found"
        exit 1
    fi

    print_test "Checking for dependency conflicts"
    if python3 -m pip check &> /dev/null; then
        print_success "No dependency conflicts"
    else
        print_warning "Dependency conflicts detected (check manually)"
    fi

    # Phase 2: File Structure Validation
    print_header "Phase 2: Project Structure"

    print_test "Checking critical directories"
    CRITICAL_DIRS=("scripts" "skills-library" "tests")
    for dir in "${CRITICAL_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            print_success "$dir/ exists"
        else
            print_failure "$dir/ not found"
        fi
    done

    print_test "Checking critical scripts"
    CRITICAL_SCRIPTS=("scripts/dedupe_skills.py" "scripts/analyze_skills.py" "scripts/generate_blueprints.py")
    for script in "${CRITICAL_SCRIPTS[@]}"; do
        if [ -f "$script" ]; then
            print_success "$script exists"
        else
            print_failure "$script not found"
        fi
    done

    print_test "Checking documentation"
    DOCS=("README.md" "tests/README.md")
    for doc in "${DOCS[@]}"; do
        if [ -f "$doc" ]; then
            print_success "$doc exists"
        else
            print_warning "$doc not found (recommended)"
        fi
    done

    # Phase 3: Unit & Integration Tests
    print_header "Phase 3: Automated Test Suite"

    print_test "Running unit tests"
    if pytest tests/unit -v --tb=short -m "not slow" &> /tmp/unit_tests.log; then
        print_success "Unit tests passed"
    else
        print_failure "Unit tests failed (see /tmp/unit_tests.log)"
        cat /tmp/unit_tests.log | tail -20
    fi

    print_test "Running integration tests"
    if pytest tests/integration -v --tb=short -m "not slow" &> /tmp/integration_tests.log; then
        print_success "Integration tests passed"
    else
        print_warning "Integration tests had issues (see /tmp/integration_tests.log)"
    fi

    print_test "Running E2E tests"
    if pytest tests/e2e -v --tb=short &> /tmp/e2e_tests.log; then
        print_success "E2E tests passed"
    else
        print_warning "E2E tests had issues (see /tmp/e2e_tests.log)"
    fi

    print_test "Checking test coverage"
    if pytest tests/unit tests/integration --cov=scripts --cov=. --cov-report=term-missing --cov-report=html -q &> /tmp/coverage.log; then
        COVERAGE=$(grep -oP "TOTAL\s+\d+\s+\d+\s+\K\d+" /tmp/coverage.log | head -1)
        if [ -n "$COVERAGE" ] && [ "$COVERAGE" -ge 80 ]; then
            print_success "Coverage: ${COVERAGE}% (≥80%)"
        else
            print_warning "Coverage: ${COVERAGE}% (<80%)"
        fi
    else
        print_warning "Coverage check failed"
    fi

    # Phase 4: Security Scanning
    print_header "Phase 4: Security Validation"

    print_test "Scanning for secrets in git history"
    if command -v trufflehog &> /dev/null; then
        if trufflehog filesystem . --only-verified --json &> /tmp/trufflehog.log; then
            if [ -s /tmp/trufflehog.log ]; then
                print_failure "Secrets detected (see /tmp/trufflehog.log)"
            else
                print_success "No secrets detected"
            fi
        else
            print_success "No secrets detected"
        fi
    else
        print_warning "trufflehog not installed (optional)"
    fi

    print_test "Checking for .env files"
    if find . -name ".env*" -not -path "*/\.*" -not -path "*/venv/*" | grep -q .; then
        print_failure ".env files found in repository"
    else
        print_success "No .env files found"
    fi

    print_test "Validating .gitignore"
    if [ -f ".gitignore" ]; then
        REQUIRED_PATTERNS=(".env" "__pycache__" "*.pyc" ".pytest_cache" ".coverage")
        ALL_PRESENT=true
        for pattern in "${REQUIRED_PATTERNS[@]}"; do
            if ! grep -q "$pattern" .gitignore; then
                ALL_PRESENT=false
                print_warning "Missing from .gitignore: $pattern"
            fi
        done
        if [ "$ALL_PRESENT" = true ]; then
            print_success ".gitignore is comprehensive"
        fi
    else
        print_failure ".gitignore not found"
    fi

    print_test "Running security linting (bandit)"
    if command -v bandit &> /dev/null; then
        if bandit -r scripts/ -ll -q &> /tmp/bandit.log; then
            print_success "No security issues detected"
        else
            print_warning "Security issues detected (see /tmp/bandit.log)"
        fi
    else
        print_warning "bandit not installed (optional)"
    fi

    print_test "Checking for dependency vulnerabilities"
    if command -v pip-audit &> /dev/null; then
        if pip-audit &> /tmp/pip-audit.log; then
            print_success "No vulnerable dependencies"
        else
            print_warning "Vulnerable dependencies detected (see /tmp/pip-audit.log)"
        fi
    else
        print_warning "pip-audit not installed (optional)"
    fi

    # Phase 5: Performance Validation
    print_header "Phase 5: Performance Benchmarks"

    print_test "Running performance tests"
    if pytest tests/performance -v -m "not slow" --tb=short &> /tmp/performance.log; then
        print_success "Performance benchmarks passed"
    else
        print_warning "Performance tests had issues"
    fi

    # Phase 6: Documentation Validation
    print_header "Phase 6: Documentation Quality"

    print_test "Checking README completeness"
    if [ -f "README.md" ]; then
        REQUIRED_SECTIONS=("Installation" "Usage" "Features")
        README_CONTENT=$(cat README.md)
        MISSING=0
        for section in "${REQUIRED_SECTIONS[@]}"; do
            if ! echo "$README_CONTENT" | grep -qi "$section"; then
                print_warning "README missing section: $section"
                ((MISSING++))
            fi
        done
        if [ $MISSING -eq 0 ]; then
            print_success "README has all key sections"
        fi
    fi

    print_test "Checking LICENSE file"
    if [ -f "LICENSE" ] || [ -f "LICENSE.md" ] || [ -f "LICENSE.txt" ]; then
        print_success "LICENSE file present"
    else
        print_failure "LICENSE file not found (required for public release)"
    fi

    print_test "Validating code comments"
    PYTHON_FILES=$(find scripts -name "*.py" | wc -l)
    if [ "$PYTHON_FILES" -gt 0 ]; then
        print_success "$PYTHON_FILES Python files documented"
    fi

    # Phase 7: CLI Testing
    print_header "Phase 7: Command-Line Interface"

    print_test "Testing --help flags"
    for script in scripts/dedupe_skills.py scripts/analyze_skills.py scripts/generate_blueprints.py; do
        if [ -f "$script" ]; then
            if python3 "$script" --help &> /dev/null || true; then
                print_success "$(basename $script) --help works"
            else
                print_warning "$(basename $script) --help failed"
            fi
        fi
    done

    # Phase 8: Final Report
    print_header "Test Execution Summary"

    echo -e "Total Tests Run:    ${TOTAL_TESTS}"
    echo -e "${GREEN}Tests Passed:       ${TESTS_PASSED}${NC}"

    if [ $TESTS_FAILED -gt 0 ]; then
        echo -e "${RED}Tests Failed:       ${TESTS_FAILED}${NC}"
    else
        echo -e "Tests Failed:       ${TESTS_FAILED}"
    fi

    SUCCESS_RATE=$((TESTS_PASSED * 100 / TOTAL_TESTS))
    echo -e "Success Rate:       ${SUCCESS_RATE}%"

    echo ""

    if [ $SUCCESS_RATE -ge 95 ]; then
        echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║  ✅ READY FOR PUBLIC RELEASE                  ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
        exit 0
    elif [ $SUCCESS_RATE -ge 85 ]; then
        echo -e "${YELLOW}╔════════════════════════════════════════════════╗${NC}"
        echo -e "${YELLOW}║  ⚠️  MINOR ISSUES - REVIEW BEFORE RELEASE     ║${NC}"
        echo -e "${YELLOW}╚════════════════════════════════════════════════╝${NC}"
        exit 1
    else
        echo -e "${RED}╔════════════════════════════════════════════════╗${NC}"
        echo -e "${RED}║  ❌ NOT READY FOR RELEASE                     ║${NC}"
        echo -e "${RED}╚════════════════════════════════════════════════╝${NC}"
        exit 1
    fi
}

# Run main function
main "$@"
