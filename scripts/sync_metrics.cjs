#!/usr/bin/env node

/**
 * Documentation Metrics Verification Script
 *
 * Verifies that all documentation files have accurate skill counts
 * that match the actual filesystem.
 *
 * Usage:
 *   node scripts/sync_metrics.js
 *
 * Exit codes:
 *   0 - All documentation is accurate
 *   1 - Documentation mismatches found
 */

const fs = require('fs');
const { execSync } = require('child_process');

// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// Count actual skills by finding skill.json files
function countActualSkills() {
  log('\n📊 Counting actual skills from filesystem...', 'cyan');

  try {
    // Count executable skills
    const executableCmd = 'find skills-library/executable -name "skill.json" 2>/dev/null | wc -l';
    const executableCount = parseInt(execSync(executableCmd, { encoding: 'utf8' }).trim(), 10);

    // Count context skills
    const contextCmd = 'find skills-library/context -name "skill.json" 2>/dev/null | wc -l';
    const contextCount = parseInt(execSync(contextCmd, { encoding: 'utf8' }).trim(), 10);

    // Count domains
    const executableDomainsCmd = 'ls -d skills-library/executable/*/ 2>/dev/null | wc -l';
    const executableDomains = parseInt(execSync(executableDomainsCmd, { encoding: 'utf8' }).trim(), 10);

    const contextDomainsCmd = 'ls -d skills-library/context/*/ 2>/dev/null | wc -l';
    const contextDomains = parseInt(execSync(contextDomainsCmd, { encoding: 'utf8' }).trim(), 10);

    const totals = {
      executable: executableCount,
      context: contextCount,
      total: executableCount + contextCount,
      domains: {
        executable: executableDomains,
        context: contextDomains,
        total: executableDomains + contextDomains,
      }
    };

    log(`   Executable: ${totals.executable}`, 'green');
    log(`   Context: ${totals.context}`, 'green');
    log(`   Total: ${totals.total}`, 'green');
    log(`   Domains: ${totals.domains.total} (${totals.domains.executable} executable + ${totals.domains.context} context)`, 'green');

    return totals;
  } catch (error) {
    log(`❌ Error counting skills: ${error.message}`, 'red');
    process.exit(1);
  }
}

// Extract skill counts from documentation files
function extractCountsFromFile(filePath, patterns) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const findings = {};

    for (const [key, regex] of Object.entries(patterns)) {
      const match = content.match(regex);
      if (match) {
        findings[key] = parseInt(match[1].replace(/,/g, ''), 10);
      }
    }

    return findings;
  } catch (error) {
    log(`   ⚠️ Could not read ${filePath}: ${error.message}`, 'yellow');
    return {};
  }
}

// Verify documentation files
function verifyDocumentation(actual) {
  log('\n🔍 Verifying documentation files...', 'cyan');

  const checks = [
    {
      file: 'README.md',
      patterns: {
        total: /Compose (\d+) AI skills/,
        executable: /(\d+) executable skills/,
        context: /(\d+) context skills/,
      },
    },
    {
      file: 'package.json',
      patterns: {
        total: /(\d+) AI skills/,
      },
    },
    {
      file: 'skills-library/README.md',
      patterns: {
        total: /\*\*(\d+) AI skills\*\*/,
        executable: /\*\*(\d+) executable\*\*/,
        context: /\*\*(\d+) context skills\*\*/,
      },
    },
    {
      file: 'skills-library/SKILLS_CATALOG.md',
      patterns: {
        total: /> \*\*(\d+) AI skills\*\*/,
        executable: /\*\*(\d+) executable skills\*\*/,
        context: /\*\*(\d+) context skills\*\*/,
      },
    },
  ];

  let hasErrors = false;

  for (const check of checks) {
    log(`\n   Checking: ${check.file}`, 'blue');
    const found = extractCountsFromFile(check.file, check.patterns);

    for (const [metric, expected] of Object.entries(found)) {
      const actualValue = actual[metric];

      if (actualValue !== undefined) {
        if (actualValue === expected) {
          log(`      ✅ ${metric}: ${expected} (correct)`, 'green');
        } else {
          log(`      ❌ ${metric}: Found ${expected}, Expected ${actualValue}`, 'red');
          hasErrors = true;
        }
      }
    }
  }

  // Check index.json separately
  log('\n   Checking: skills-library/index.json', 'blue');
  try {
    const index = JSON.parse(fs.readFileSync('skills-library/index.json', 'utf8'));

    if (index.metrics) {
      if (index.metrics.total_skills === actual.total) {
        log(`      ✅ total_skills: ${index.metrics.total_skills} (correct)`, 'green');
      } else {
        log(`      ❌ total_skills: Found ${index.metrics.total_skills}, Expected ${actual.total}`, 'red');
        hasErrors = true;
      }

      if (index.metrics.executable_skills === actual.executable) {
        log(`      ✅ executable_skills: ${index.metrics.executable_skills} (correct)`, 'green');
      } else {
        log(`      ❌ executable_skills: Found ${index.metrics.executable_skills}, Expected ${actual.executable}`, 'red');
        hasErrors = true;
      }

      if (index.metrics.context_skills === actual.context) {
        log(`      ✅ context_skills: ${index.metrics.context_skills} (correct)`, 'green');
      } else {
        log(`      ❌ context_skills: Found ${index.metrics.context_skills}, Expected ${actual.context}`, 'red');
        hasErrors = true;
      }
    } else {
      log('      ⚠️ No metrics section found in index.json', 'yellow');
    }
  } catch (error) {
    log(`      ❌ Error reading index.json: ${error.message}`, 'red');
    hasErrors = true;
  }

  return !hasErrors;
}

// Main execution
function main() {
  log('\n========================================', 'cyan');
  log('📚 Documentation Metrics Verification', 'cyan');
  log('========================================\n', 'cyan');

  // Count actual skills
  const actual = countActualSkills();

  // Verify documentation
  const isValid = verifyDocumentation(actual);

  // Print summary
  log('\n========================================', 'cyan');
  if (isValid) {
    log('✅ All documentation is accurate!', 'green');
    log('========================================\n', 'cyan');
    process.exit(0);
  } else {
    log('❌ Documentation errors found!', 'red');
    log('========================================\n', 'cyan');
    log('To fix:', 'yellow');
    log('  1. Update affected files with correct numbers', 'yellow');
    log('  2. Reference METRICS.md for canonical counts', 'yellow');
    log('  3. Run this script again to verify\n', 'yellow');
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { countActualSkills, verifyDocumentation };
