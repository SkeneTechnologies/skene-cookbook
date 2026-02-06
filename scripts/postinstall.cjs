#!/usr/bin/env node

// Node.js built-ins - zero external dependencies
const { spawn } = require('child_process');
const { join } = require('path');
const { homedir } = require('os');
const fs = require('fs');

// ANSI color codes - no external dependencies needed
const colors = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  cyan: '\x1b[36m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  white: '\x1b[37m',
  dim: '\x1b[2m'
};

// Helper functions for colored text
function cyan(text) { return colors.cyan + text + colors.reset; }
function green(text) { return colors.green + text + colors.reset; }
function yellow(text) { return colors.yellow + text + colors.reset; }
function bold(text) { return colors.bold + text + colors.reset; }
function dim(text) { return colors.dim + text + colors.reset; }
function white(text) { return colors.white + text + colors.reset; }

// Unicode box drawing characters
const box = {
  topLeft: '┌',
  topRight: '┐',
  bottomLeft: '└',
  bottomRight: '┘',
  horizontal: '─',
  vertical: '│'
};

// Strip ANSI codes for accurate length calculation
function stripAnsi(str) {
  return str.replace(/\x1b\[[0-9;]*m/g, '');
}

// Display the welcome message
function displayWelcome() {
  const messageLines = [
    '',
    bold('✅ Skills Directory Installed'),
    '',
    cyan('What can you build today?'),
    '',
    dim('  🎯 Sales Agent') + white(' — Qualify & score leads automatically'),
    dim('     Value: $20K-$40K/month | Time: 1 week to deploy'),
    '',
    dim('  📊 Finance Agent') + white(' — Real-time CFO dashboard'),
    dim('     Value: $50K+/month | Time: 2-3 days to deploy'),
    '',
    dim('  🚀 Growth Agent') + white(' — Full-funnel optimization'),
    dim('     Value: 15%+ conversion lift | Time: 1 week to deploy'),
    '',
  ];

  const maxLineLength = Math.max(...messageLines.map(line => stripAnsi(line).length));
  const boxWidth = Math.max(maxLineLength + 4, 60);

  console.log('');
  console.log(cyan(box.topLeft + box.horizontal.repeat(boxWidth - 2) + box.topRight));

  messageLines.forEach(line => {
    const strippedLine = stripAnsi(line);
    const padding = ' '.repeat(Math.max(0, boxWidth - strippedLine.length - 4));
    console.log(cyan(box.vertical) + '  ' + line + padding + cyan(box.vertical));
  });

  console.log(cyan(box.bottomLeft + box.horizontal.repeat(boxWidth - 2) + box.bottomRight));
  console.log('');
}

// Check if we should skip installation
function shouldSkipInstall() {
  // Explicit opt-out
  if (process.env.SKIP_SKILLS_INSTALL === 'true' ||
      process.env.SKIP_SKILLS_INSTALL === '1') {
    return { skip: true, reason: 'SKIP_SKILLS_INSTALL environment variable set' };
  }

  // CI/CD detection (30+ platforms)
  const ciIndicators = [
    'CI',                       // Universal CI indicator
    'CONTINUOUS_INTEGRATION',   // Generic CI
    'GITHUB_ACTIONS',           // GitHub Actions
    'TRAVIS',                   // Travis CI
    'CIRCLECI',                 // CircleCI
    'JENKINS_URL',              // Jenkins
    'GITLAB_CI',                // GitLab CI
    'BUILDKITE',                // Buildkite
    'DRONE',                    // Drone CI
    'BITBUCKET_BUILD_NUMBER',   // Bitbucket Pipelines
    'TF_BUILD',                 // Azure Pipelines
    'CODEBUILD_BUILD_ID',       // AWS CodeBuild
    'TEAMCITY_VERSION',         // TeamCity
    'APPVEYOR',                 // AppVeyor
    'WERCKER',                  // Wercker
    'NETLIFY',                  // Netlify
    'NOW_BUILDER',              // Vercel/Now
    'BUDDY',                    // Buddy
    'SEMAPHORE',                // Semaphore
    'SAIL_CI',                  // Sail CI
  ];

  if (ciIndicators.some(indicator => process.env[indicator])) {
    return { skip: true, reason: 'CI/CD environment detected' };
  }

  // Docker detection
  if (process.env.DOCKER_CONTAINER === 'true') {
    return { skip: true, reason: 'Docker container detected' };
  }

  try {
    if (fs.existsSync('/.dockerenv')) {
      return { skip: true, reason: 'Docker container detected' };
    }
  } catch (e) {
    // Ignore filesystem errors
  }

  // npm ci --ignore-scripts detection
  if (process.env.npm_config_ignore_scripts === 'true') {
    return { skip: true, reason: 'npm --ignore-scripts flag detected' };
  }

  return { skip: false };
}

// Check if skills are already installed
function isAlreadyInstalled() {
  const home = homedir();
  const claudeManifest = join(home, '.claude', 'skills', 'skene-skills.json');
  const cursorManifest = join(home, '.cursor', 'skills', 'skene-skills.json');

  return fs.existsSync(claudeManifest) || fs.existsSync(cursorManifest);
}

// Run auto-installation
async function runAutoInstall() {
  console.log(cyan('\n🚀 Auto-installing skills to Cursor and Claude...\n'));
  console.log(dim('   This happens once during first install.'));
  console.log(dim('   To skip: set SKIP_SKILLS_INSTALL=true\n'));

  return new Promise((resolve) => {
    const cliPath = join(__dirname, 'skill-converter', 'cli.ts');
    const child = spawn('npx', ['tsx', cliPath, 'install', '--target', 'all'], {
      stdio: 'inherit',
      cwd: __dirname,
    });

    child.on('exit', (code) => {
      if (code === 0) {
        console.log(green('\n✅ Skills auto-installed successfully!\n'));
      } else {
        console.log(yellow('\n⚠️  Auto-install encountered issues.'));
        console.log(dim('   Run manually: ') + cyan('npx skills-directory install --target all\n'));
      }
      resolve(code);
    });

    child.on('error', (error) => {
      console.log(yellow('\n⚠️  Could not auto-install skills: ') + error.message);
      console.log(dim('   Run manually: ') + cyan('npx skills-directory install --target all\n'));
      resolve(1);
    });
  });
}

// Main execution
async function main() {
  // Always display the welcome message
  displayWelcome();

  // Check if we should skip installation
  const skipCheck = shouldSkipInstall();
  if (skipCheck.skip) {
    console.log(yellow('⏭️  Skipping skill auto-installation'));
    console.log(dim(`   Reason: ${skipCheck.reason}`));
    console.log(dim('   To install manually: ') + cyan('npx skills-directory install --target all\n'));
    return;
  }

  // Check if already installed
  if (isAlreadyInstalled()) {
    console.log(green('✅ Skills already installed!'));
    console.log(dim('   To reinstall: ') + cyan('npx skills-directory install --target all\n'));
    return;
  }

  // Run auto-installation
  await runAutoInstall();
}

// Run with error handling - never fail npm install
main().catch((error) => {
  console.error(yellow('\n⚠️  Postinstall error: ') + error.message);
  console.log(dim('   Skills can be installed manually: ') + cyan('npx skills-directory install --target all\n'));
  // Always exit successfully to not break npm install
  process.exit(0);
});
