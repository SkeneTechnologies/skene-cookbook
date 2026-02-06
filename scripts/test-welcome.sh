#!/bin/bash
#
# Test script for welcome screen functionality
#

set -e

echo "================================"
echo "Testing Welcome Screen Features"
echo "================================"
echo ""

# Test 1: Help command
echo "Test 1: Help command (should show welcome screen)"
echo "---"
node bin/skills-directory.js help
echo ""

# Test 2: Stats command
echo "Test 2: Stats command (should show library statistics)"
echo "---"
node bin/skills-directory.js stats
echo ""

# Test 3: Post-install script
echo "Test 3: Post-install script"
echo "---"
node scripts/postinstall.js
echo ""

# Test 4: List command
echo "Test 4: List command with domain filter (plg)"
echo "---"
node bin/skills-directory.js list --domain plg | head -30
echo ""

echo "================================"
echo "All tests completed successfully!"
echo "================================"
