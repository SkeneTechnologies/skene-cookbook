/**
 * Skill Exporter
 * 
 * Exports skills to different platform formats:
 * - Claude: SKILL.md with YAML frontmatter
 * - Cursor: instructions.mdc with globs
 * - SkeneFlow: skill.json + instructions.md (native format)
 */

import { mkdir, writeFile, symlink, rm } from 'node:fs/promises';
import { join, dirname, basename } from 'node:path';
import type { LoadedSkill, ExportFormat, ExportOptions, DOMAIN_GLOB_MAPPING } from './types.js';

// Import the domain to glob mapping
const DOMAIN_GLOBS: Record<string, string[]> = {
  'cursor_rules': ['**/*'],
  'development': ['**/*.{js,jsx,ts,tsx,py,go,rs,java,rb,php}'],
  'superpowers': ['**/*'],
  'security': ['**/*'],
  'scientific': ['**/*.{py,ipynb,R,jl}'],
  'plg': ['**/*.{ts,tsx,js,jsx}'],
  'plg_frameworks': ['**/*.{ts,tsx,js,jsx,md}'],
  'monetization': ['**/*.{ts,tsx,js,jsx}'],
  'revops': ['**/*.{ts,tsx,js,jsx}'],
  'customer_success': ['**/*.{ts,tsx,js,jsx}'],
  'ecosystem': ['**/*.{ts,tsx,js,jsx}'],
  'marketing': ['**/*.{ts,tsx,js,jsx,md}'],
  'ai_ops': ['**/*.{ts,tsx,js,jsx,py}'],
  'data_ops': ['**/*.{sql,py,ts}'],
  'devex': ['**/*'],
  'finops': ['**/*.{ts,tsx,js,jsx}'],
  'product_ops': ['**/*.{ts,tsx,js,jsx}'],
  'support_ops': ['**/*.{ts,tsx,js,jsx}'],
  'people_ops': ['**/*'],
  'anthropic_official': ['**/*'],
  'community': ['**/*'],
  'compliance': ['**/*'],
  'meta': ['**/*'],
  'skene': ['**/*'],
  'vcf': ['**/*'],
};

/**
 * Get globs for a skill based on its domain and existing config
 */
function getGlobsForSkill(skill: LoadedSkill): string[] {
  // Use existing cursor globs if defined
  if (skill.manifest.platforms?.cursor?.globs) {
    return skill.manifest.platforms.cursor.globs;
  }
  
  // Use domain-based globs
  const domain = skill.manifest.domain;
  return DOMAIN_GLOBS[domain] || ['**/*'];
}

/**
 * Export skill to Claude format (SKILL.md)
 */
function toClaudeFormat(skill: LoadedSkill): string {
  const { manifest, instructions } = skill;
  
  // Build description with triggers
  let description = manifest.description;
  const triggers = manifest.platforms?.claude?.triggers || [];
  if (triggers.length > 0) {
    description += ` Use when: ${triggers.join(', ')}.`;
  }
  
  // Build frontmatter
  const frontmatter = [
    '---',
    `name: ${manifest.name}`,
    `description: ${description}`,
  ];
  
  // Add license if available
  const license = manifest.platforms?.claude?.license;
  if (license) {
    frontmatter.push(`license: ${license}`);
  }
  
  frontmatter.push('---');
  
  return frontmatter.join('\n') + '\n\n' + instructions;
}

/**
 * Export skill to Cursor format (.mdc)
 */
function toCursorFormat(skill: LoadedSkill): string {
  const { manifest, instructions } = skill;
  
  // Get globs for this skill
  const globs = getGlobsForSkill(skill);
  
  // Build frontmatter
  const frontmatter = [
    '---',
    `description: ${manifest.description}`,
    `globs: ${globs.join(',')}`,
    '---',
  ];
  
  return frontmatter.join('\n') + '\n\n' + instructions;
}

/**
 * Export skill to SkeneFlow format (skill.json + instructions.md)
 */
function toSkeneFlowFormat(skill: LoadedSkill): { manifest: string; instructions: string } {
  const { manifest, instructions } = skill;
  
  // Build full SkeneFlow manifest
  const skeneManifest = {
    id: manifest.id,
    version: manifest.version,
    name: manifest.name,
    description: manifest.description,
    domain: manifest.domain,
    source: manifest.source || 'native',
    tools: manifest.platforms?.skeneflow?.tools || [],
    exitStates: manifest.platforms?.skeneflow?.exitStates || ['success', 'failure'],
    inputSchema: manifest.platforms?.skeneflow?.inputSchema || {},
    outputSchema: manifest.platforms?.skeneflow?.outputSchema || {},
    temperature: manifest.temperature ?? 0,
    tags: manifest.tags || [],
  };
  
  // Add metrics if available
  if (manifest.platforms?.skeneflow?.metrics) {
    (skeneManifest as any).metrics = manifest.platforms.skeneflow.metrics;
  }
  
  return {
    manifest: JSON.stringify(skeneManifest, null, 2),
    instructions,
  };
}

/**
 * Export a single skill to the specified format
 */
export async function exportSkill(
  skill: LoadedSkill,
  format: ExportFormat,
  outputDir: string,
  includeReferences: boolean = true
): Promise<string[]> {
  const outputFiles: string[] = [];
  
  // Create output directory
  const skillOutputDir = join(outputDir, skill.manifest.domain, basename(dirname(skill.sourcePath)) === skill.manifest.domain 
    ? basename(skill.sourcePath) 
    : skill.manifest.id.split('/').pop() || skill.manifest.name);
  
  await mkdir(skillOutputDir, { recursive: true });
  
  switch (format) {
    case 'claude': {
      const content = toClaudeFormat(skill);
      const outputPath = join(skillOutputDir, 'SKILL.md');
      await writeFile(outputPath, content);
      outputFiles.push(outputPath);
      break;
    }
    
    case 'cursor': {
      const content = toCursorFormat(skill);
      const outputPath = join(skillOutputDir, 'instructions.mdc');
      await writeFile(outputPath, content);
      outputFiles.push(outputPath);
      
      // Also write a minimal skill.json for metadata
      const miniManifest = {
        id: skill.manifest.id,
        name: skill.manifest.name,
        description: skill.manifest.description,
        domain: skill.manifest.domain,
        globs: getGlobsForSkill(skill),
      };
      const manifestPath = join(skillOutputDir, 'skill.json');
      await writeFile(manifestPath, JSON.stringify(miniManifest, null, 2));
      outputFiles.push(manifestPath);
      break;
    }
    
    case 'skeneflow': {
      const { manifest, instructions } = toSkeneFlowFormat(skill);
      
      const manifestPath = join(skillOutputDir, 'skill.json');
      await writeFile(manifestPath, manifest);
      outputFiles.push(manifestPath);
      
      const instructionsPath = join(skillOutputDir, 'instructions.md');
      await writeFile(instructionsPath, instructions);
      outputFiles.push(instructionsPath);
      break;
    }
  }
  
  // Write reference files if requested
  if (includeReferences && skill.references) {
    for (const [filename, content] of Object.entries(skill.references)) {
      const refPath = join(skillOutputDir, filename);
      await writeFile(refPath, content);
      outputFiles.push(refPath);
    }
  }
  
  return outputFiles;
}

/**
 * Export all skills to the specified format
 */
export async function exportAllSkills(
  skills: LoadedSkill[],
  options: ExportOptions
): Promise<{ exported: number; files: string[] }> {
  const allFiles: string[] = [];
  let exported = 0;
  
  for (const skill of skills) {
    try {
      const files = await exportSkill(
        skill,
        options.format,
        options.outputDir,
        options.includeReferences ?? true
      );
      allFiles.push(...files);
      exported++;
    } catch (error) {
      console.error(`Failed to export ${skill.manifest.id}:`, error);
    }
  }
  
  console.log(`Exported ${exported} skills to ${options.format} format`);
  return { exported, files: allFiles };
}

/**
 * Generate a flat cursor rules directory structure
 * (for direct installation to .cursor/rules/)
 */
export async function exportFlatCursorRules(
  skills: LoadedSkill[],
  outputDir: string
): Promise<{ exported: number; files: string[] }> {
  const allFiles: string[] = [];
  let exported = 0;
  
  await mkdir(outputDir, { recursive: true });
  
  for (const skill of skills) {
    try {
      const content = toCursorFormat(skill);
      
      // Use domain-name as filename for uniqueness
      const filename = `${skill.manifest.domain}--${skill.manifest.name.replace(/[^a-zA-Z0-9-_]/g, '-')}.mdc`;
      const outputPath = join(outputDir, filename);
      
      await writeFile(outputPath, content);
      allFiles.push(outputPath);
      exported++;
    } catch (error) {
      console.error(`Failed to export ${skill.manifest.id}:`, error);
    }
  }
  
  console.log(`Exported ${exported} flat cursor rules to ${outputDir}`);
  return { exported, files: allFiles };
}

/**
 * Generate skills index file
 */
export async function generateSkillsIndex(
  skills: LoadedSkill[],
  outputPath: string
): Promise<void> {
  const index = {
    version: '1.0.0',
    generated: new Date().toISOString(),
    total: skills.length,
    byDomain: {} as Record<string, { count: number; skills: string[] }>,
    byTag: {} as Record<string, string[]>,
  };
  
  for (const skill of skills) {
    // Index by domain
    const domain = skill.manifest.domain;
    if (!index.byDomain[domain]) {
      index.byDomain[domain] = { count: 0, skills: [] };
    }
    index.byDomain[domain].count++;
    index.byDomain[domain].skills.push(skill.manifest.id);
    
    // Index by tag
    for (const tag of skill.manifest.tags || []) {
      if (!index.byTag[tag]) {
        index.byTag[tag] = [];
      }
      index.byTag[tag].push(skill.manifest.id);
    }
  }
  
  await writeFile(outputPath, JSON.stringify(index, null, 2));
  console.log(`Generated skills index at ${outputPath}`);
}
