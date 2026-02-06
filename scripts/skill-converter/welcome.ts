import chalk from 'chalk';
import boxen from 'boxen';
import terminalSize from 'terminal-size';
import { getLogo } from './logo.js';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { existsSync } from 'node:fs';

export interface WelcomeScreenConfig {
  showLogo?: boolean;
  tagline?: string;
}

/**
 * Check if this is first installation
 */
export function isFirstInstall(): boolean {
  const home = homedir();
  const claudeManifest = join(home, '.claude', 'skills', 'skene-skills.json');
  const cursorManifest = join(home, '.cursor', 'skills', 'skene-skills.json');

  return !existsSync(claudeManifest) && !existsSync(cursorManifest);
}

/**
 * Render welcome screen with Charm-style formatting
 */
export function renderWelcomeScreen(config: WelcomeScreenConfig = {}): string {
  const {
    showLogo = true,
    tagline = '800+ AI Skills for Claude and Cursor'
  } = config;

  const { columns: termWidth } = terminalSize();
  const lines: string[] = [];

  // Logo section (white/bright for high contrast)
  if (showLogo) {
    const logo = getLogo(termWidth);

    // Center the logo if terminal is wide enough
    if (termWidth > 60) {
      const logoLines = logo.split('\n');
      const centeredLines = logoLines.map(line => {
        const logoWidth = line.length;
        const padding = Math.max(0, Math.floor((termWidth - logoWidth) / 2));
        return ' '.repeat(padding) + line;
      });
      lines.push(chalk.white.bold(centeredLines.join('\n')));
    } else {
      lines.push(chalk.white.bold(logo));
    }
    lines.push('');
  }

  // Title box using boxen with width constraint
  const title = 'Welcome to Skene Skills Directory';

  // Calculate safe width (leave margin for borders and padding)
  const maxContentWidth = Math.min(termWidth - 10, 60); // Never exceed terminal width

  const titleBox = boxen(chalk.bold.white(title), {
    padding: { left: 2, right: 2, top: 0, bottom: 0 },
    borderStyle: 'round',
    borderColor: 'white',
    dimBorder: false,
    textAlignment: 'center',
    width: maxContentWidth,  // Explicit width constraint
  });

  lines.push(titleBox);
  lines.push('');

  // Tagline
  lines.push(chalk.dim(`  ${tagline}`));
  lines.push('');

  return lines.join('\n');
}

/**
 * Render success message after installation
 */
export function renderSuccessMessage(installedCount: number, targets: string[]): string {
  const { columns: termWidth } = terminalSize();

  const message = [
    chalk.green.bold('✓ Installation Complete!'),
    '',
    chalk.white(`  Installed ${chalk.bold(installedCount)} skills to:`),
    ...targets.map(t => chalk.dim(`    • ${t}`)),
    '',
    chalk.dim('  Try: ') + chalk.cyan('npx skills-directory --help'),
  ].join('\n');

  // Calculate safe width
  const maxWidth = Math.min(termWidth - 4, 50);

  return boxen(message, {
    padding: 1,
    borderStyle: 'round',
    borderColor: 'green',
    width: maxWidth,  // Explicit width to prevent breaking
  });
}
