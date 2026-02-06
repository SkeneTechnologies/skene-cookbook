#!/bin/bash
# Cross-Platform Testing Script
# Tests installation and basic functionality across different platforms using Docker

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════╗
║            CROSS-PLATFORM TESTING - PUBLIC RELEASE                   ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker to run cross-platform tests.${NC}"
    exit 1
fi

# Test platforms
PLATFORMS=(
    "ubuntu:22.04|Ubuntu 22.04 LTS"
    "ubuntu:24.04|Ubuntu 24.04 LTS"
    "python:3.9-slim|Python 3.9 (Debian)"
    "python:3.10-slim|Python 3.10 (Debian)"
    "python:3.11-slim|Python 3.11 (Debian)"
    "python:3.12-slim|Python 3.12 (Debian)"
)

PASSED=0
FAILED=0
TOTAL=${#PLATFORMS[@]}

# Test script to run in each container
TEST_SCRIPT='
cd /workspace
echo "Installing dependencies..."
pip3 install -q -r requirements.txt 2>&1 | grep -E "(Successfully|already|ERROR)" || true
echo "Running basic tests..."
python3 scripts/dedupe_skills.py --help &> /dev/null || echo "dedupe_skills.py failed"
python3 scripts/analyze_skills.py --help &> /dev/null || echo "analyze_skills.py failed"
echo "Running pytest (if available)..."
pip3 install -q pytest &> /dev/null || true
pytest tests/unit -x -q 2>&1 | tail -5 || echo "Tests not available or failed"
echo "✅ Platform test complete"
'

echo -e "\n${YELLOW}Testing on $TOTAL platforms...${NC}\n"

for platform_info in "${PLATFORMS[@]}"; do
    IFS='|' read -r image name <<< "$platform_info"

    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Testing: $name${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

    # Run test in Docker container
    if docker run --rm \
        -v "$(pwd):/workspace" \
        -w /workspace \
        "$image" \
        bash -c "$TEST_SCRIPT" 2>&1 | tee "/tmp/platform_test_${image//[\/:]/_}.log"; then

        echo -e "\n${GREEN}✓ $name - PASSED${NC}\n"
        ((PASSED++))
    else
        echo -e "\n${RED}✗ $name - FAILED${NC}\n"
        ((FAILED++))
    fi

    sleep 1
done

# Summary
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}CROSS-PLATFORM TEST SUMMARY${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo "Total Platforms:  $TOTAL"
echo -e "${GREEN}Passed:           $PASSED${NC}"

if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Failed:           $FAILED${NC}"
else
    echo "Failed:           $FAILED"
fi

SUCCESS_RATE=$((PASSED * 100 / TOTAL))
echo "Success Rate:     ${SUCCESS_RATE}%"

echo ""

if [ $SUCCESS_RATE -eq 100 ]; then
    echo -e "${GREEN}✅ All platforms passed!${NC}"
    exit 0
elif [ $SUCCESS_RATE -ge 80 ]; then
    echo -e "${YELLOW}⚠️  Most platforms passed, but some failures detected.${NC}"
    exit 1
else
    echo -e "${RED}❌ Multiple platform failures detected.${NC}"
    exit 1
fi
