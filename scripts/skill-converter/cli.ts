#!/usr/bin/env npx tsx
/**
 * Skene Skills CLI
 * 
 * Universal AI Skills for Claude and Cursor
 * 
 * Usage:
 *   npx tsx scripts/skill-converter/cli.ts install --target cursor
 *   npx tsx scripts/skill-converter/cli.ts install --target claude
 *   npx tsx scripts/skill-converter/cli.ts install --target all
 *   npx tsx scripts/skill-converter/cli.ts export --format cursor --output ./dist/cursor
 *   npx tsx scripts/skill-converter/cli.ts stats
 *   npx tsx scripts/skill-converter/cli.ts list --domain plg
 */

import { resolve, join } from 'node:path';
import { loadAllSkills, filterSkills, groupByDomain } from './loader.js';
import { exportAllSkills, generateSkillsIndex, exportFlatCursorRules } from './exporter.js';
import { installAll, uninstall, getDefaultPaths } from './installer.js';
import type { ExportFormat, InstallTarget } from './types.js';
import chalk from 'chalk';
import { renderWelcomeScreen, isFirstInstall, renderSuccessMessage } from './welcome.js';

// Parse command line arguments
const args = process.argv.slice(2);
const command = args[0];

function parseArgs(args: string[]): Record<string, string | boolean> {
  const result: Record<string, string | boolean> = {};
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const nextArg = args[i + 1];
      
      if (nextArg && !nextArg.startsWith('--')) {
        result[key] = nextArg;
        i++;
      } else {
        result[key] = true;
      }
    }
  }
  
  return result;
}

const parsedArgs = parseArgs(args.slice(1));

// Get library path (default to skills-library in current directory)
const libraryPath = (parsedArgs['library'] as string) || resolve(process.cwd(), 'skills-library');

async function main() {
  switch (command) {
    case 'install':
      await handleInstall();
      break;

    case 'uninstall':
      await handleUninstall();
      break;

    case 'status':
      await handleStatus();
      break;

    case 'export':
      await handleExport();
      break;

    case 'stats':
      await handleStats();
      break;

    case 'list':
      await handleList();
      break;

    case 'showcase':
      await handleShowcase();
      break;

    case 'help':
    default:
      printHelp();
      break;
  }
}

async function handleInstall() {
  const target = (parsedArgs['target'] as InstallTarget) || 'all';
  const domains = parsedArgs['domain'] ? [(parsedArgs['domain'] as string)] : undefined;
  const symlink = parsedArgs['symlink'] === true;

  // Show welcome screen on first install
  if (isFirstInstall()) {
    console.log(renderWelcomeScreen());
    console.log(chalk.dim('  Installing for the first time...\n'));
    await new Promise(resolve => setTimeout(resolve, 800));
  }

  console.log(chalk.cyan(`\n🚀 Installing Skene Skills to ${chalk.bold(target)}...\n`));
  
  // Load skills
  const allSkills = await loadAllSkills(libraryPath);
  const skills = filterSkills(allSkills, { domains });
  
  console.log(`Found ${skills.length} skills to install\n`);
  
  // Install
  const results = await installAll(skills, {
    target,
    symlink,
    cursorPath: parsedArgs['cursor-path'] as string,
    claudePath: parsedArgs['claude-path'] as string,
  });
  
  // Print results with styled success message
  const targetNames = [
    results.cursor && 'Cursor',
    results.claude && 'Claude',
    results.skeneflow && 'SkeneFlow'
  ].filter(Boolean) as string[];

  console.log('\n' + renderSuccessMessage(skills.length, targetNames));

  // NEW: Show value proposition
  console.log('\n' + chalk.bold.white('💡 What You Can Build Now:\n'));

  const useCases = [
    {
      name: 'Sales Deal-Closing Agent',
      domain: 'revops',
      skills: 5,
      value: '$20K-$40K/month',
      time: '1 week'
    },
    {
      name: 'Churn Prevention Agent',
      domain: 'customer_success',
      skills: 4,
      value: '$400K ARR saved/year',
      time: '3-5 days'
    },
    {
      name: 'Financial Intelligence Agent',
      domain: 'finops',
      skills: 5,
      value: '$50K+/month',
      time: '2-3 days'
    }
  ];

  for (const useCase of useCases) {
    console.log(
      chalk.dim(`  ${useCase.name}`) +
      chalk.white(` (${useCase.skills} skills)`)
    );
    console.log(
      chalk.dim(`    Value: `) + chalk.green(useCase.value) +
      chalk.dim(` | Deploy: `) + chalk.cyan(useCase.time)
    );
    console.log();
  }

  console.log(chalk.dim('  See more: ') + chalk.cyan('docs/SKILL_CHAINS.md'));
  console.log(chalk.dim('  Quick wins: ') + chalk.cyan('docs/QUICK_WINS.md\n'));

  console.log('\n📖 Usage:');
  if (results.cursor) {
    console.log(chalk.dim('  Cursor skills are now available in your IDE'));
  }
  if (results.claude) {
    console.log(chalk.dim('  Claude skills will trigger automatically based on context'));
  }
}

async function handleUninstall() {
  const target = (parsedArgs['target'] as InstallTarget) || 'all';

  console.log(`\n🗑️  Uninstalling Skene Skills from ${target}...\n`);

  await uninstall(target, {
    cursorPath: parsedArgs['cursor-path'] as string,
    claudePath: parsedArgs['claude-path'] as string,
  });

  console.log('\n✅ Uninstallation complete!\n');
}

async function handleStatus() {
  const { homedir } = await import('node:os');
  const { existsSync, readFileSync } = await import('node:fs');

  console.log(chalk.bold.white('\n📊 Skills Installation Status\n'));

  const paths = getDefaultPaths({
    cursorPath: parsedArgs['cursor-path'] as string,
    claudePath: parsedArgs['claude-path'] as string,
  });

  // Check Claude installation
  const claudeManifestPath = join(paths.claude, 'skene-skills.json');
  if (existsSync(claudeManifestPath)) {
    try {
      const manifest = JSON.parse(readFileSync(claudeManifestPath, 'utf8'));
      console.log(chalk.green('✅ Claude Skills Installed'));
      console.log(chalk.dim(`   Skills: `) + chalk.white(manifest.skills.length));
      console.log(chalk.dim(`   Generated: `) + chalk.white(new Date(manifest.generated).toLocaleString()));
      console.log(chalk.dim(`   Location: `) + chalk.cyan(paths.claude));

      // Verify files exist
      let intact = 0;
      for (const skill of manifest.skills) {
        // Use the path from manifest, or fallback to old format (domain/name)
        const skillPath = skill.path
          ? join(paths.claude, skill.path)
          : join(paths.claude, skill.domain, skill.name, 'SKILL.md');
        if (existsSync(skillPath)) {
          intact++;
        }
      }
      console.log(chalk.dim(`   Files intact: `) + chalk.white(`${intact}/${manifest.skills.length}`));

      if (intact < manifest.skills.length) {
        console.log(chalk.yellow(`   ⚠️  ${manifest.skills.length - intact} skill files are missing`));
      }
    } catch (error) {
      console.log(chalk.red('❌ Claude Skills - Manifest corrupted'));
      console.log(chalk.dim(`   Error: `) + chalk.red((error as Error).message));
    }
  } else {
    console.log(chalk.red('❌ Claude Skills Not Installed'));
    console.log(chalk.dim(`   Expected at: `) + chalk.cyan(claudeManifestPath));
  }

  console.log();

  // Check Cursor installation
  const cursorManifestPath = join(paths.cursor, 'skene-skills.json');
  if (existsSync(cursorManifestPath)) {
    try {
      const manifest = JSON.parse(readFileSync(cursorManifestPath, 'utf8'));
      console.log(chalk.green('✅ Cursor Skills Installed'));
      console.log(chalk.dim(`   Skills: `) + chalk.white(manifest.rules.length));
      console.log(chalk.dim(`   Generated: `) + chalk.white(new Date(manifest.generated).toLocaleString()));
      console.log(chalk.dim(`   Location: `) + chalk.cyan(paths.cursor));

      // Verify files exist
      let intact = 0;
      for (const rule of manifest.rules) {
        const rulePath = join(paths.cursor, rule.file);
        if (existsSync(rulePath)) {
          intact++;
        }
      }
      console.log(chalk.dim(`   Files intact: `) + chalk.white(`${intact}/${manifest.rules.length}`));

      if (intact < manifest.rules.length) {
        console.log(chalk.yellow(`   ⚠️  ${manifest.rules.length - intact} skill files are missing`));
      }
    } catch (error) {
      console.log(chalk.red('❌ Cursor Skills - Manifest corrupted'));
      console.log(chalk.dim(`   Error: `) + chalk.red((error as Error).message));
    }
  } else {
    console.log(chalk.red('❌ Cursor Skills Not Installed'));
    console.log(chalk.dim(`   Expected at: `) + chalk.cyan(cursorManifestPath));
  }

  console.log();
  console.log(chalk.dim('💡 To reinstall: ') + chalk.cyan('npx skills-directory install --target all'));
  console.log(chalk.dim('💡 To uninstall: ') + chalk.cyan('npx skills-directory uninstall --target all'));
  console.log();
}

async function handleExport() {
  const format = (parsedArgs['format'] as ExportFormat) || 'skeneflow';
  const outputDir = (parsedArgs['output'] as string) || `./dist/${format}`;
  const domains = parsedArgs['domain'] ? [(parsedArgs['domain'] as string)] : undefined;
  
  console.log(`\n📦 Exporting skills to ${format} format...\n`);
  
  // Load skills
  const allSkills = await loadAllSkills(libraryPath);
  const skills = filterSkills(allSkills, { domains });
  
  console.log(`Exporting ${skills.length} skills to ${outputDir}\n`);
  
  // Export
  const { exported, files } = await exportAllSkills(skills, {
    format,
    outputDir: resolve(outputDir),
    includeReferences: true,
  });
  
  // Generate index
  await generateSkillsIndex(skills, join(resolve(outputDir), 'index.json'));
  
  console.log(`\n✅ Exported ${exported} skills to ${outputDir}`);
  console.log(`   Total files: ${files.length}`);
}

async function handleStats() {
  console.log('\n📊 Skene Skills Library Statistics\n');
  
  // Load skills
  const skills = await loadAllSkills(libraryPath);
  const byDomain = groupByDomain(skills);
  
  // Count totals
  const domains = Object.keys(byDomain).sort();
  const totalSkills = skills.length;
  
  console.log(`Total Skills: ${totalSkills}`);
  console.log(`Total Domains: ${domains.length}\n`);
  
  console.log('Skills by Domain:');
  console.log('─'.repeat(50));
  
  for (const domain of domains) {
    const count = byDomain[domain].length;
    const bar = '█'.repeat(Math.min(count, 40));
    console.log(`  ${domain.padEnd(25)} ${String(count).padStart(4)} ${bar}`);
  }
  
  console.log('─'.repeat(50));
  
  // Platform compatibility
  let withCursorGlobs = 0;
  let withClaudeTriggers = 0;
  let withSkeneflowTools = 0;
  
  for (const skill of skills) {
    if (skill.manifest.platforms?.cursor?.globs) withCursorGlobs++;
    if (skill.manifest.platforms?.claude?.triggers) withClaudeTriggers++;
    if (skill.manifest.platforms?.skeneflow?.tools?.length) withSkeneflowTools++;
  }
  
  console.log('\nPlatform Compatibility:');
  console.log(`  Cursor (with globs):    ${withCursorGlobs} skills`);
  console.log(`  Claude (with triggers): ${withClaudeTriggers} skills`);
  console.log(`  SkeneFlow (with tools): ${withSkeneflowTools} skills`);
  console.log(`  Universal (all skills): ${totalSkills} skills`);
}

async function handleList() {
  const domain = parsedArgs['domain'] as string | undefined;
  const tag = parsedArgs['tag'] as string | undefined;
  
  // Load skills
  const allSkills = await loadAllSkills(libraryPath);
  const skills = filterSkills(allSkills, { 
    domains: domain ? [domain] : undefined,
    tags: tag ? [tag] : undefined,
  });
  
  if (domain) {
    console.log(`\n📋 Skills in domain: ${domain}\n`);
  } else if (tag) {
    console.log(`\n📋 Skills with tag: ${tag}\n`);
  } else {
    console.log(`\n📋 All Skills\n`);
  }
  
  const byDomain = groupByDomain(skills);
  
  for (const [domainName, domainSkills] of Object.entries(byDomain)) {
    console.log(`\n${domainName} (${domainSkills.length}):`);
    
    for (const skill of domainSkills) {
      const desc = skill.manifest.description.slice(0, 60);
      console.log(`  • ${skill.manifest.name.padEnd(30)} ${desc}...`);
    }
  }
  
  console.log(`\nTotal: ${skills.length} skills`);
}

async function handleShowcase() {
  console.log('\n' + chalk.bold.white('💡 What You Can Build with Skills Directory\n'));

  const useCases = [
    {
      emoji: '🎯',
      name: 'Sales Deal-Closing Agent',
      domain: 'RevOps',
      description: 'Automatically qualify, score, and route leads to your sales team',
      skills: 5,
      value: '$20K-$40K/month saved',
      time: '1 week to deploy',
      quickWin: '15-minute: Lead scoring (2 skills)'
    },
    {
      emoji: '💰',
      name: 'Customer Churn Prevention',
      domain: 'Customer Success',
      description: 'Predict churn risk 60-90 days early and trigger intervention playbooks',
      skills: 4,
      value: '$400K ARR saved/year',
      time: '3-5 days to deploy',
      quickWin: '1-hour: Health monitoring alerts (3 skills)'
    },
    {
      emoji: '📊',
      name: 'Financial Intelligence Dashboard',
      domain: 'FinOps',
      description: 'Real-time CFO dashboard with automated board reporting',
      skills: 5,
      value: '$50K+/month saved',
      time: '2-3 days to deploy',
      quickWin: 'Half-day: ARR tracking (2 skills)'
    },
    {
      emoji: '🚀',
      name: 'Growth Optimization Engine',
      domain: 'Marketing/PLG',
      description: 'Continuous A/B testing and conversion optimization',
      skills: 6,
      value: '15-25% conversion lift',
      time: '1 week to deploy',
      quickWin: 'Half-day: Signup flow CRO (3 skills)'
    },
    {
      emoji: '✍️',
      name: 'Content Marketing Automation',
      domain: 'Marketing',
      description: 'End-to-end content creation, distribution, and optimization',
      skills: 7,
      value: '2.5x content volume',
      time: '1 week to deploy',
      quickWin: 'Half-day: Blog post automation (4 skills)'
    }
  ];

  for (const useCase of useCases) {
    console.log(chalk.bold(`${useCase.emoji}  ${useCase.name}`));
    console.log(chalk.dim(`   Domain: ${useCase.domain}`));
    console.log(chalk.white(`   ${useCase.description}`));
    console.log();
    console.log(chalk.dim(`   Skills: `) + chalk.cyan(useCase.skills) + chalk.dim(` | Value: `) + chalk.green(useCase.value));
    console.log(chalk.dim(`   Deploy: `) + chalk.cyan(useCase.time));
    console.log(chalk.dim(`   Quick Win: `) + chalk.yellow(useCase.quickWin));
    console.log();
  }

  console.log(chalk.bold.white('📚 Learn More:\n'));
  console.log(chalk.dim('  Full recipes: ') + chalk.cyan('docs/SKILL_CHAINS.md'));
  console.log(chalk.dim('  Quick wins: ') + chalk.cyan('docs/QUICK_WINS.md'));
  console.log(chalk.dim('  ROI & value: ') + chalk.cyan('docs/VALUE.md'));
  console.log();

  console.log(chalk.bold.white('🏁 Get Started:\n'));
  console.log(chalk.cyan('  $ npx skills-directory install --target all'));
  console.log(chalk.dim('  $ npx skills-directory list --domain revops'));
  console.log();
}

function printHelp() {
  // Show logo in help
  console.log(renderWelcomeScreen({ showLogo: true }));

  // Commands section with better styling
  console.log(chalk.bold.white('Commands:'));
  console.log(chalk.dim('  install [options]     ') + 'Install skills to Claude/Cursor');
  console.log(chalk.dim('  uninstall [options]   ') + 'Remove installed skills');
  console.log(chalk.dim('  status                ') + 'Check installation status and verify files');
  console.log(chalk.dim('  export [options]      ') + 'Export skills to a specific format');
  console.log(chalk.dim('  stats                 ') + 'Show library statistics');
  console.log(chalk.dim('  list [options]        ') + 'List available skills');
  console.log(chalk.dim('  showcase              ') + 'Show what you can build (use cases & ROI)');
  console.log(chalk.dim('  help                  ') + 'Show this help message');

  console.log(chalk.bold.white('\nInstall Options:'));
  console.log(chalk.dim('  --target <target>     ') + 'cursor, claude, skeneflow, all (default: all)');
  console.log(chalk.dim('  --cursor-path <path>  ') + 'Custom Cursor skills directory');
  console.log(chalk.dim('  --claude-path <path>  ') + 'Custom Claude skills directory');
  console.log(chalk.dim('  --domain <domain>     ') + 'Only install skills from this domain');
  console.log(chalk.dim('  --symlink             ') + 'Use symlinks instead of copying files');

  console.log(chalk.bold.white('\nExport Options:'));
  console.log(chalk.dim('  --format <format>     ') + 'cursor, claude, skeneflow (default: skeneflow)');
  console.log(chalk.dim('  --output <path>       ') + 'Output directory (default: ./dist/<format>)');
  console.log(chalk.dim('  --domain <domain>     ') + 'Only export skills from this domain');

  console.log(chalk.bold.white('\nList Options:'));
  console.log(chalk.dim('  --domain <domain>     ') + 'Filter by domain');
  console.log(chalk.dim('  --tag <tag>           ') + 'Filter by tag');

  console.log(chalk.bold.white('\nExamples:'));
  console.log(chalk.cyan('  $ npx skills-directory install --target all'));
  console.log(chalk.cyan('  $ npx skills-directory status'));
  console.log(chalk.cyan('  $ npx skills-directory install --target cursor --domain plg'));
  console.log(chalk.cyan('  $ npx skills-directory showcase'));
  console.log(chalk.cyan('  $ npx skills-directory list --domain plg'));
  console.log(chalk.cyan('  $ npx skills-directory stats'));

  console.log('');
  console.log(chalk.dim('  For more info: ') + chalk.underline('https://github.com/SkeneTechnologies/skene-cookbook'));
  console.log('');
}

// Run
main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
