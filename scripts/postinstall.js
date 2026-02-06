#!/usr/bin/env node

// ANSI color codes - no external dependencies needed
const colors = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  cyan: '\x1b[36m',
  green: '\x1b[32m',
  white: '\x1b[37m',
  dim: '\x1b[2m'
};

// Helper functions for colored text
function cyan(text) { return colors.cyan + text + colors.reset; }
function green(text) { return colors.green + text + colors.reset; }
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

// Build the message content
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
  green('Get started:'),
  cyan('  $ npx skills-directory install --target all'),
  '',
  dim('Learn more: docs/VALUE.md'),
  ''
];

// Calculate box width based on content
// Strip ANSI codes for accurate length calculation
function stripAnsi(str) {
  return str.replace(/\x1b\[[0-9;]*m/g, '');
}

const maxLineLength = Math.max(...messageLines.map(line => stripAnsi(line).length));
const boxWidth = Math.max(maxLineLength + 4, 60);

// Display the boxed message
console.log('');
console.log(cyan(box.topLeft + box.horizontal.repeat(boxWidth - 2) + box.topRight));

messageLines.forEach(line => {
  const strippedLine = stripAnsi(line);
  const padding = ' '.repeat(Math.max(0, boxWidth - strippedLine.length - 4));
  console.log(cyan(box.vertical) + '  ' + line + padding + cyan(box.vertical));
});

console.log(cyan(box.bottomLeft + box.horizontal.repeat(boxWidth - 2) + box.bottomRight));
console.log('');
