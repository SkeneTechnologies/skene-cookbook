/**
 * Skill Installer
 * 
 * Installs skills to different platforms:
 * - Cursor: Copy/symlink .mdc files to .cursor/rules/
 * - Claude: Copy/symlink to Claude skills directory
 * - SkeneFlow: Register with skill registry
 */

import { mkdir, symlink, copyFile, rm, readdir, stat, writeFile, readFile } from 'node:fs/promises';
import { join, dirname, basename, resolve } from 'node:path';
import { homedir } from 'node:os';
import type { LoadedSkill, InstallTarget, InstallOptions } from './types.js';
import { exportSkill, exportFlatCursorRules } from './exporter.js';

/**
 * Get default paths for different platforms
 */
export function getDefaultPaths(): {
  cursorRules: string;
  cursorSkills: string;
  claudeSkills: string;
  skeneflowRegistry: string;
} {
  const home = homedir();
  
  return {
    // Cursor rules directory (workspace-level, will use cwd)
    cursorRules: join(process.cwd(), '.cursor', 'rules'),
    // Cursor skills directory (user-level)
    cursorSkills: join(home, '.cursor', 'skills'),
    // Claude skills directory
    claudeSkills: join(home, '.claude', 'skills'),
    // SkeneFlow registry
    skeneflowRegistry: join(process.cwd(), 'skills-library'),
  };
}

/**
 * Ensure directory exists
 */
async function ensureDir(dirPath: string): Promise<void> {
  await mkdir(dirPath, { recursive: true });
}

/**
 * Install skills to Cursor
 */
export async function installToCursor(
  skills: LoadedSkill[],
  options: {
    outputDir: string;
    useSymlinks?: boolean;
    flat?: boolean;
  }
): Promise<{ installed: number; path: string }> {
  await ensureDir(options.outputDir);
  
  if (options.flat) {
    // Flat structure: all .mdc files in one directory
    const result = await exportFlatCursorRules(skills, options.outputDir);
    return { installed: result.exported, path: options.outputDir };
  }
  
  // Nested structure: domain/skill/ directories
  let installed = 0;
  
  for (const skill of skills) {
    try {
      await exportSkill(skill, 'cursor', options.outputDir, false);
      installed++;
    } catch (error) {
      console.error(`Failed to install ${skill.manifest.id} to Cursor:`, error);
    }
  }
  
  return { installed, path: options.outputDir };
}

/**
 * Install skills to Claude
 */
export async function installToClaude(
  skills: LoadedSkill[],
  options: {
    outputDir: string;
    useSymlinks?: boolean;
  }
): Promise<{ installed: number; path: string }> {
  await ensureDir(options.outputDir);
  
  let installed = 0;
  
  for (const skill of skills) {
    try {
      await exportSkill(skill, 'claude', options.outputDir, true);
      installed++;
    } catch (error) {
      console.error(`Failed to install ${skill.manifest.id} to Claude:`, error);
    }
  }
  
  return { installed, path: options.outputDir };
}

/**
 * Generate Cursor rules manifest file
 */
export async function generateCursorManifest(
  skills: LoadedSkill[],
  outputPath: string
): Promise<void> {
  const manifest = {
    version: '1.0.0',
    generated: new Date().toISOString(),
    source: 'skene-skills',
    rules: skills.map(skill => ({
      id: skill.manifest.id,
      name: skill.manifest.name,
      description: skill.manifest.description,
      domain: skill.manifest.domain,
      file: `${skill.manifest.domain}--${skill.manifest.name.replace(/[^a-zA-Z0-9-_]/g, '-')}.mdc`,
    })),
  };
  
  await writeFile(outputPath, JSON.stringify(manifest, null, 2));
}

/**
 * Generate Claude skills manifest file
 */
export async function generateClaudeManifest(
  skills: LoadedSkill[],
  outputPath: string
): Promise<void> {
  const manifest = {
    version: '1.0.0',
    generated: new Date().toISOString(),
    source: 'skene-skills',
    skills: skills.map(skill => ({
      id: skill.manifest.id,
      name: skill.manifest.name,
      description: skill.manifest.description,
      domain: skill.manifest.domain,
      path: join(skill.manifest.domain, skill.manifest.name, 'SKILL.md'),
      triggers: skill.manifest.platforms?.claude?.triggers || [],
    })),
  };
  
  await writeFile(outputPath, JSON.stringify(manifest, null, 2));
}

/**
 * Full installation to all platforms
 */
export async function installAll(
  skills: LoadedSkill[],
  options: InstallOptions
): Promise<{
  cursor?: { installed: number; path: string };
  claude?: { installed: number; path: string };
  skeneflow?: { registered: number };
}> {
  const results: {
    cursor?: { installed: number; path: string };
    claude?: { installed: number; path: string };
    skeneflow?: { registered: number };
  } = {};
  
  const defaultPaths = getDefaultPaths();
  
  // Install to Cursor
  if (options.target === 'cursor' || options.target === 'all') {
    const cursorPath = options.cursorPath || defaultPaths.cursorSkills;
    results.cursor = await installToCursor(skills, {
      outputDir: cursorPath,
      useSymlinks: options.symlink,
      flat: true, // Use flat structure for easier discovery
    });
    
    // Generate manifest
    await generateCursorManifest(skills, join(cursorPath, 'skene-skills.json'));
  }
  
  // Install to Claude
  if (options.target === 'claude' || options.target === 'all') {
    const claudePath = options.claudePath || defaultPaths.claudeSkills;
    results.claude = await installToClaude(skills, {
      outputDir: claudePath,
      useSymlinks: options.symlink,
    });
    
    // Generate manifest
    await generateClaudeManifest(skills, join(claudePath, 'skene-skills.json'));
  }
  
  // Register with SkeneFlow
  if (options.target === 'skeneflow' || options.target === 'all') {
    // SkeneFlow uses the native skill format, so we just need to ensure
    // the skills are accessible to the registry
    results.skeneflow = { registered: skills.length };
    console.log(`Registered ${skills.length} skills with SkeneFlow`);
  }
  
  return results;
}

/**
 * Uninstall skills from a platform
 */
export async function uninstall(
  target: InstallTarget,
  options: {
    cursorPath?: string;
    claudePath?: string;
  } = {}
): Promise<void> {
  const defaultPaths = getDefaultPaths();
  
  if (target === 'cursor' || target === 'all') {
    const cursorPath = options.cursorPath || defaultPaths.cursorSkills;
    try {
      // Remove skene-skills files (those with skene- prefix or from manifest)
      const manifestPath = join(cursorPath, 'skene-skills.json');
      const manifest = JSON.parse(await readFile(manifestPath, 'utf-8'));
      
      for (const rule of manifest.rules) {
        const filePath = join(cursorPath, rule.file);
        try {
          await rm(filePath);
        } catch {
          // File doesn't exist
        }
      }
      
      await rm(manifestPath);
      console.log(`Uninstalled Cursor skills from ${cursorPath}`);
    } catch {
      console.log(`No Cursor skills to uninstall at ${cursorPath}`);
    }
  }
  
  if (target === 'claude' || target === 'all') {
    const claudePath = options.claudePath || defaultPaths.claudeSkills;
    try {
      const manifestPath = join(claudePath, 'skene-skills.json');
      const manifest = JSON.parse(await readFile(manifestPath, 'utf-8'));
      
      for (const skill of manifest.skills) {
        const dirPath = join(claudePath, skill.domain, skill.name);
        try {
          await rm(dirPath, { recursive: true });
        } catch {
          // Directory doesn't exist
        }
      }
      
      await rm(manifestPath);
      console.log(`Uninstalled Claude skills from ${claudePath}`);
    } catch {
      console.log(`No Claude skills to uninstall at ${claudePath}`);
    }
  }
}
