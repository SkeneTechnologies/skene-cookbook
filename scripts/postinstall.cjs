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
  // eslint-disable-next-line no-control-regex -- intentional ANSI escape sequence
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

  // Use console.error() so npm shows the message even when installing as a dependency
  console.error('');
  console.error(cyan(box.topLeft + box.horizontal.repeat(boxWidth - 2) + box.topRight));

  messageLines.forEach(line => {
    const strippedLine = stripAnsi(line);
    const padding = ' '.repeat(Math.max(0, boxWidth - strippedLine.length - 4));
    console.error(cyan(box.vertical) + '  ' + line + padding + cyan(box.vertical));
  });

  console.error(cyan(box.bottomLeft + box.horizontal.repeat(boxWidth - 2) + box.bottomRight));
  console.error('');
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

// Generate ecosystem recommendations
async function generateEcosystem() {
  return new Promise((resolve) => {
    console.error(dim('\n   Generating ecosystem recommendations...\n'));

    const cliPath = join(__dirname, 'skill-converter', 'cli.ts');
    const outputPath = join(process.cwd(), 'ECOSYSTEM.md');

    const child = spawn('npx', [
      'tsx',
      cliPath,
      'ecosystem',
      '--repo-root', process.cwd(),
      '--output', outputPath
    ], {
      stdio: 'pipe',
      cwd: __dirname
    });

    child.on('exit', (code) => {
      if (code === 0) {
        console.error(green('   ✅ Generated ECOSYSTEM.md with tailored recommendations'));
      }
      // Always resolve - ecosystem generation is optional
      resolve(code);
    });

    child.on('error', () => {
      // Silent failure - ecosystem generation is optional
      resolve(1);
    });
  });
}

// Run auto-installation
async function runAutoInstall() {
  console.error(cyan('\n🚀 Auto-installing skills to Cursor and Claude...\n'));
  console.error(dim('   This happens once during first install.'));
  console.error(dim('   To skip: set SKIP_SKILLS_INSTALL=true\n'));

  return new Promise((resolve) => {
    const cliPath = join(__dirname, 'skill-converter', 'cli.ts');
    const child = spawn('npx', ['tsx', cliPath, 'install', '--target', 'all'], {
      stdio: 'inherit',
      cwd: __dirname,
    });

    child.on('exit', async (code) => {
      if (code === 0) {
        console.error(green('\n✅ Skills auto-installed successfully!\n'));

        // Generate ecosystem recommendations
        await generateEcosystem();
      } else {
        console.error(yellow('\n⚠️  Auto-install encountered issues.'));
        console.error(dim('   Run manually: ') + cyan('npx skills-directory install --target all\n'));
      }
      resolve(code);
    });

    child.on('error', (error) => {
      console.error(yellow('\n⚠️  Could not auto-install skills: ') + error.message);
      console.error(dim('   Run manually: ') + cyan('npx skills-directory install --target all\n'));
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
    console.error(yellow('⏭️  Skipping skill auto-installation'));
    console.error(dim(`   Reason: ${skipCheck.reason}`));
    console.error(dim('   To install manually: ') + cyan('npx skills-directory install --target all\n'));
    return;
  }

  // Check if already installed
  if (isAlreadyInstalled()) {
    console.error(green('✅ Skills already installed!'));

    // Show where they're installed
    const home = homedir();
    const claudeManifest = join(home, '.claude', 'skills', 'skene-skills.json');
    const cursorManifest = join(home, '.cursor', 'skills', 'skene-skills.json');

    if (fs.existsSync(claudeManifest)) {
      try {
        const manifest = JSON.parse(fs.readFileSync(claudeManifest, 'utf8'));
        console.error(dim('   • Claude: ') + white(`${manifest.skills.length} skills`));
      } catch {
        console.error(dim('   • Claude: ') + white('installed'));
      }
    }

    if (fs.existsSync(cursorManifest)) {
      try {
        const manifest = JSON.parse(fs.readFileSync(cursorManifest, 'utf8'));
        console.error(dim('   • Cursor: ') + white(`${manifest.rules.length} skills`));
      } catch {
        console.error(dim('   • Cursor: ') + white('installed'));
      }
    }

    console.error();
    console.error(dim('   Check status: ') + cyan('npx skills-directory status'));
    console.error(dim('   To reinstall: ') + cyan('npx skills-directory install --target all\n'));
    return;
  }

  // Run auto-installation
  await runAutoInstall();
}

// Run with error handling - never fail npm install
main().catch((error) => {
  console.error(yellow('\n⚠️  Postinstall error: ') + error.message);
  console.error(dim('   Skills can be installed manually: ') + cyan('npx skills-directory install --target all\n'));
  // Always exit successfully to not break npm install
  process.exit(0);
});
