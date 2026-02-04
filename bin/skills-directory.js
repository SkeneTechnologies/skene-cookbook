#!/usr/bin/env node
/**
 * Skills Directory CLI
 *
 * Install 800+ AI skills to Cursor and Claude.
 *
 * Usage:
 *   npx skills-directory install --target cursor
 *   npx skills-directory install --target claude
 *   npx skills-directory install --target all
 *   npx skills-directory stats
 *   npx skills-directory list --domain plg
 */

import { spawn } from 'child_process';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const pkgRoot = join(__dirname, '..');
const cliPath = join(pkgRoot, 'scripts', 'skill-converter', 'cli.ts');

const args = process.argv.slice(2);

const child = spawn('npx', ['tsx', cliPath, ...args], {
  stdio: 'inherit',
  cwd: pkgRoot,
});

child.on('exit', (code) => {
  process.exit(code ?? 0);
});
