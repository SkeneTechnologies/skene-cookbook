#!/usr/bin/env node

// Use dynamic import for ESM modules
(async () => {
  try {
    const chalk = (await import('chalk')).default;
    const boxen = (await import('boxen')).default;

    const message = [
      chalk.white.bold('✅ Skills Directory Installed'),
      '',
      chalk.cyan('What can you build today?'),
      '',
      chalk.dim('  🎯 Sales Agent') + chalk.white(' — Qualify & score leads automatically'),
      chalk.dim('     Value: $20K-$40K/month | Time: 1 week to deploy'),
      '',
      chalk.dim('  📊 Finance Agent') + chalk.white(' — Real-time CFO dashboard'),
      chalk.dim('     Value: $50K+/month | Time: 2-3 days to deploy'),
      '',
      chalk.dim('  🚀 Growth Agent') + chalk.white(' — Full-funnel optimization'),
      chalk.dim('     Value: 15%+ conversion lift | Time: 1 week to deploy'),
      '',
      chalk.green('Get started:'),
      chalk.cyan('  $ npx skills-directory install --target all'),
      '',
      chalk.dim('Learn more: ') + chalk.underline('docs/VALUE.md'),
    ].join('\n');

    const box = boxen(message, {
      padding: 1,
      margin: 1,
      borderStyle: 'round',
      borderColor: 'cyan',
      textAlignment: 'center',
    });

    // Force output to be visible even with npm warnings
    console.log('\n' + box + '\n');
  } catch (error) {
    // Silently fail if dependencies aren't available
    // This prevents postinstall errors in environments without chalk/boxen
  }
})();
