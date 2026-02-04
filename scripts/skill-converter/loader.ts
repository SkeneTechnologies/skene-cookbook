/**
 * Skill Loader
 * 
 * Loads skills from the skills-library and normalizes them
 * to the unified format.
 */

import { readFile, readdir, stat } from 'node:fs/promises';
import { join, basename, dirname } from 'node:path';
import type { UnifiedSkillManifest, LoadedSkill } from './types.js';

/**
 * Get all categories a skill belongs to (for multi-category discovery).
 * Includes domain plus any explicit categories.
 */
export function getSkillCategories(skill: LoadedSkill): string[] {
  const domain = skill.manifest.domain || 'unknown';
  const categories = skill.manifest.categories;
  if (categories && categories.length > 0) {
    const set = new Set([domain, ...categories]);
    return [...set];
  }
  return [domain];
}

/**
 * Parse YAML frontmatter from markdown files
 */
function parseFrontmatter(content: string): { frontmatter: Record<string, string>; body: string } {
  const match = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  
  if (!match) {
    return { frontmatter: {}, body: content };
  }
  
  const frontmatter: Record<string, string> = {};
  const lines = match[1].split('\n');
  
  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex === -1) continue;
    
    const key = line.slice(0, colonIndex).trim();
    const value = line.slice(colonIndex + 1).trim();
    
    if (key && value) {
      frontmatter[key] = value;
    }
  }
  
  return { frontmatter, body: match[2] };
}

/**
 * Load a skill manifest from skill.json
 */
async function loadManifest(skillPath: string): Promise<UnifiedSkillManifest | null> {
  const manifestPath = join(skillPath, 'skill.json');
  
  try {
    const content = await readFile(manifestPath, 'utf-8');
    const manifest = JSON.parse(content);
    return manifest as UnifiedSkillManifest;
  } catch {
    return null;
  }
}

/**
 * Load instructions from .md or .mdc file
 */
async function loadInstructions(skillPath: string): Promise<{ content: string; frontmatter: Record<string, string>; format: 'md' | 'mdc' } | null> {
  // Try different instruction file names
  const candidates = [
    'instructions.md',
    'instructions.mdc',
    'SKILL.md',
  ];
  
  for (const candidate of candidates) {
    const filePath = join(skillPath, candidate);
    try {
      const content = await readFile(filePath, 'utf-8');
      const { frontmatter, body } = parseFrontmatter(content);
      const format = candidate.endsWith('.mdc') ? 'mdc' : 'md';
      return { content: body, frontmatter, format };
    } catch {
      // File doesn't exist, try next
    }
  }
  
  return null;
}

/**
 * Load all reference files in a skill directory
 */
async function loadReferences(skillPath: string): Promise<Record<string, string>> {
  const references: Record<string, string> = {};
  
  try {
    const files = await readdir(skillPath);
    
    for (const file of files) {
      // Skip main files
      if (['skill.json', 'instructions.md', 'instructions.mdc', 'SKILL.md', 'LICENSE.txt'].includes(file)) {
        continue;
      }
      
      // Only load markdown and text files
      if (file.endsWith('.md') || file.endsWith('.txt')) {
        const filePath = join(skillPath, file);
        const fileStat = await stat(filePath);
        
        if (fileStat.isFile()) {
          references[file] = await readFile(filePath, 'utf-8');
        }
      }
    }
  } catch {
    // Directory read failed
  }
  
  return references;
}

/**
 * Enhance manifest with frontmatter data
 */
function enhanceManifest(
  manifest: UnifiedSkillManifest,
  frontmatter: Record<string, string>,
  format: 'md' | 'mdc'
): UnifiedSkillManifest {
  const enhanced = { ...manifest };
  
  // Ensure platforms object exists
  if (!enhanced.platforms) {
    enhanced.platforms = {};
  }
  
  // Use frontmatter description if manifest description is minimal
  if (frontmatter.description && manifest.description.length < 50) {
    enhanced.description = frontmatter.description;
  }
  
  // Extract globs for cursor format
  if (format === 'mdc' && frontmatter.globs) {
    if (!enhanced.platforms.cursor) {
      enhanced.platforms.cursor = {};
    }
    enhanced.platforms.cursor.globs = frontmatter.globs.split(',').map(g => g.trim());
  }
  
  // Extract license for claude format
  if (frontmatter.license) {
    if (!enhanced.platforms.claude) {
      enhanced.platforms.claude = {};
    }
    enhanced.platforms.claude.license = frontmatter.license;
  }
  
  return enhanced;
}

/**
 * Load a single skill from a directory
 */
export async function loadSkill(skillPath: string): Promise<LoadedSkill | null> {
  // Load manifest
  const manifest = await loadManifest(skillPath);
  if (!manifest) {
    console.warn(`No skill.json found in ${skillPath}`);
    return null;
  }
  
  // Load instructions
  const instructions = await loadInstructions(skillPath);
  if (!instructions) {
    console.warn(`No instructions found in ${skillPath}`);
    return null;
  }
  
  // Enhance manifest with frontmatter
  const enhancedManifest = enhanceManifest(manifest, instructions.frontmatter, instructions.format);
  
  // Load references
  const references = await loadReferences(skillPath);
  
  return {
    manifest: enhancedManifest,
    instructions: instructions.content,
    references: Object.keys(references).length > 0 ? references : undefined,
    sourcePath: skillPath,
  };
}

/**
 * Recursively find all skill directories
 */
async function findSkillDirectories(basePath: string): Promise<string[]> {
  const skillDirs: string[] = [];
  
  async function scan(dirPath: string, depth: number = 0) {
    if (depth > 3) return; // Max depth to prevent infinite recursion
    
    try {
      const entries = await readdir(dirPath, { withFileTypes: true });
      
      // Check if this is a skill directory (has skill.json)
      const hasSkillJson = entries.some(e => e.name === 'skill.json' && e.isFile());
      
      if (hasSkillJson) {
        skillDirs.push(dirPath);
        return; // Don't recurse into skill directories
      }
      
      // Recurse into subdirectories
      for (const entry of entries) {
        if (entry.isDirectory() && !entry.name.startsWith('.')) {
          await scan(join(dirPath, entry.name), depth + 1);
        }
      }
    } catch {
      // Directory read failed
    }
  }
  
  await scan(basePath);
  return skillDirs;
}

/**
 * Load all skills from the skills-library
 */
export async function loadAllSkills(libraryPath: string): Promise<LoadedSkill[]> {
  const skillDirs = await findSkillDirectories(libraryPath);
  const skills: LoadedSkill[] = [];
  
  for (const dir of skillDirs) {
    const skill = await loadSkill(dir);
    if (skill) {
      skills.push(skill);
    }
  }
  
  console.log(`Loaded ${skills.length} skills from ${libraryPath}`);
  return skills;
}

/**
 * Group skills by domain (primary category)
 */
export function groupByDomain(skills: LoadedSkill[]): Record<string, LoadedSkill[]> {
  const grouped: Record<string, LoadedSkill[]> = {};
  
  for (const skill of skills) {
    const domain = skill.manifest.domain || 'unknown';
    if (!grouped[domain]) {
      grouped[domain] = [];
    }
    grouped[domain].push(skill);
  }
  
  return grouped;
}

/**
 * Group skills by all categories (domain + categories array).
 * A skill appears under each category it belongs to.
 */
export function groupByCategory(skills: LoadedSkill[]): Record<string, LoadedSkill[]> {
  const grouped: Record<string, LoadedSkill[]> = {};
  
  for (const skill of skills) {
    const categories = getSkillCategories(skill);
    for (const cat of categories) {
      if (!grouped[cat]) {
        grouped[cat] = [];
      }
      grouped[cat].push(skill);
    }
  }
  
  return grouped;
}

/**
 * Filter skills by domains/categories and/or tags.
 * When filtering by domains, matches if the skill's domain or any category matches.
 */
export function filterSkills(
  skills: LoadedSkill[],
  options: { domains?: string[]; tags?: string[] }
): LoadedSkill[] {
  return skills.filter(skill => {
    // Filter by domain or category
    if (options.domains && options.domains.length > 0) {
      const skillCategories = getSkillCategories(skill);
      const matches = options.domains.some(d => skillCategories.includes(d));
      if (!matches) {
        return false;
      }
    }
    
    // Filter by tags
    if (options.tags && options.tags.length > 0) {
      const skillTags = skill.manifest.tags || [];
      if (!options.tags.some(tag => skillTags.includes(tag))) {
        return false;
      }
    }
    
    return true;
  });
}
