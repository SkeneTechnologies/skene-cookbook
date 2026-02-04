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
    
    case 'export':
      await handleExport();
      break;
    
    case 'stats':
      await handleStats();
      break;
    
    case 'list':
      await handleList();
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
  
  console.log(`\n🚀 Installing Skene Skills to ${target}...\n`);
  
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
  
  // Print results
  console.log('\n✅ Installation complete!\n');
  
  if (results.cursor) {
    console.log(`  Cursor: ${results.cursor.installed} skills installed to ${results.cursor.path}`);
  }
  
  if (results.claude) {
    console.log(`  Claude: ${results.claude.installed} skills installed to ${results.claude.path}`);
  }
  
  if (results.skeneflow) {
    console.log(`  SkeneFlow: ${results.skeneflow.registered} skills registered`);
  }
  
  console.log('\n📖 Usage:');
  if (results.cursor) {
    console.log('  Cursor skills are now available in your IDE');
  }
  if (results.claude) {
    console.log('  Claude skills will trigger automatically based on context');
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

function printHelp() {
  console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                     Skene Skills CLI                          ║
║         Universal AI Skills for Claude and Cursor             ║
╚═══════════════════════════════════════════════════════════════╝

Usage: npx tsx scripts/skill-converter/cli.ts <command> [options]

Commands:
  install     Install skills to Claude, Cursor, or both
  uninstall   Remove installed skills
  export      Export skills to a specific format
  stats       Show library statistics
  list        List available skills
  help        Show this help message

Install Options:
  --target <target>     Target platform: cursor, claude, skeneflow, all (default: all)
  --cursor-path <path>  Custom Cursor skills directory
  --claude-path <path>  Custom Claude skills directory
  --domain <domain>     Only install skills from this domain
  --symlink             Use symlinks instead of copying files

Export Options:
  --format <format>     Output format: cursor, claude, skeneflow (default: skeneflow)
  --output <path>       Output directory (default: ./dist/<format>)
  --domain <domain>     Only export skills from this domain

List Options:
  --domain <domain>     Filter by domain
  --tag <tag>           Filter by tag

Examples:
  # Install all skills to Cursor and Claude
  npx tsx scripts/skill-converter/cli.ts install --target all

  # Install only PLG skills to Cursor
  npx tsx scripts/skill-converter/cli.ts install --target cursor --domain plg

  # Export all skills to Cursor format
  npx tsx scripts/skill-converter/cli.ts export --format cursor --output ./dist/cursor

  # Show statistics
  npx tsx scripts/skill-converter/cli.ts stats

  # List all security skills
  npx tsx scripts/skill-converter/cli.ts list --domain security

For more information, visit: https://github.com/skene-flow/skene-skills
`);
}

// Run
main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
