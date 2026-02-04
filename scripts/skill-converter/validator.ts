/**
 * Skill Validator
 * 
 * Validates skill format compatibility for CI/CD pipelines.
 * Checks:
 * - skill.json schema validity
 * - instructions.md/mdc presence and format
 * - Platform-specific requirements
 * - Quality tier consistency
 */

import { readFile, readdir, stat } from 'node:fs/promises';
import { join, basename } from 'node:path';

export interface ValidationError {
  skillId: string;
  path: string;
  error: string;
  severity: 'error' | 'warning';
}

export interface ValidationResult {
  valid: boolean;
  totalSkills: number;
  validSkills: number;
  errors: ValidationError[];
  warnings: ValidationError[];
}

/**
 * Validate skill.json schema
 */
function validateManifest(manifest: any, skillPath: string): ValidationError[] {
  const errors: ValidationError[] = [];
  const skillId = manifest.id || basename(skillPath);
  
  // Required fields
  const requiredFields = ['id', 'version', 'name', 'description', 'domain'];
  for (const field of requiredFields) {
    if (!manifest[field]) {
      errors.push({
        skillId,
        path: join(skillPath, 'skill.json'),
        error: `Missing required field: ${field}`,
        severity: 'error',
      });
    }
  }
  
  // Version format
  if (manifest.version && !/^\d+\.\d+\.\d+/.test(manifest.version)) {
    errors.push({
      skillId,
      path: join(skillPath, 'skill.json'),
      error: `Invalid version format: ${manifest.version} (expected semver)`,
      severity: 'warning',
    });
  }
  
  // Description length
  if (manifest.description && manifest.description.length < 20) {
    errors.push({
      skillId,
      path: join(skillPath, 'skill.json'),
      error: `Description too short (${manifest.description.length} chars, minimum 20)`,
      severity: 'warning',
    });
  }
  
  // Tags validation
  if (manifest.tags) {
    if (!Array.isArray(manifest.tags)) {
      errors.push({
        skillId,
        path: join(skillPath, 'skill.json'),
        error: 'tags must be an array',
        severity: 'error',
      });
    }
  }
  
  // Exit states validation
  if (manifest.exitStates) {
    if (!Array.isArray(manifest.exitStates)) {
      errors.push({
        skillId,
        path: join(skillPath, 'skill.json'),
        error: 'exitStates must be an array',
        severity: 'error',
      });
    }
  }
  
  // Tools validation
  if (manifest.tools) {
    if (!Array.isArray(manifest.tools)) {
      errors.push({
        skillId,
        path: join(skillPath, 'skill.json'),
        error: 'tools must be an array',
        severity: 'error',
      });
    } else {
      for (const tool of manifest.tools) {
        if (typeof tool === 'object' && !tool.name) {
          errors.push({
            skillId,
            path: join(skillPath, 'skill.json'),
            error: 'Each tool must have a name property',
            severity: 'error',
          });
        }
      }
    }
  }
  
  // Platforms validation
  if (manifest.platforms) {
    if (typeof manifest.platforms !== 'object') {
      errors.push({
        skillId,
        path: join(skillPath, 'skill.json'),
        error: 'platforms must be an object',
        severity: 'error',
      });
    }
  }
  
  // Quality tier validation
  const validTiers = ['verified', 'community', 'experimental'];
  if (manifest.tags && Array.isArray(manifest.tags)) {
    const tierTags = manifest.tags.filter((t: string) => validTiers.includes(t));
    if (tierTags.length > 1) {
      errors.push({
        skillId,
        path: join(skillPath, 'skill.json'),
        error: `Multiple quality tiers found: ${tierTags.join(', ')}`,
        severity: 'warning',
      });
    }
  }
  
  return errors;
}

/**
 * Validate instructions file
 */
async function validateInstructions(skillPath: string): Promise<ValidationError[]> {
  const errors: ValidationError[] = [];
  const skillId = basename(skillPath);
  
  // Check for instruction files
  const candidates = ['instructions.md', 'instructions.mdc', 'SKILL.md'];
  let foundInstructions = false;
  
  for (const candidate of candidates) {
    const filePath = join(skillPath, candidate);
    try {
      const content = await readFile(filePath, 'utf-8');
      foundInstructions = true;
      
      // Check for frontmatter in .md files
      if (candidate.endsWith('.md') || candidate.endsWith('.mdc')) {
        const hasFrontmatter = content.startsWith('---');
        
        // .mdc files should have globs
        if (candidate.endsWith('.mdc') && hasFrontmatter) {
          if (!content.includes('globs:')) {
            errors.push({
              skillId,
              path: filePath,
              error: '.mdc file missing globs field in frontmatter',
              severity: 'warning',
            });
          }
        }
      }
      
      // Check minimum content length
      const bodyContent = content.replace(/^---[\s\S]*?---\n?/, '');
      if (bodyContent.trim().length < 100) {
        errors.push({
          skillId,
          path: filePath,
          error: `Instructions too short (${bodyContent.trim().length} chars, minimum 100)`,
          severity: 'warning',
        });
      }
      
      break; // Found valid instructions
    } catch {
      // File doesn't exist, try next
    }
  }
  
  if (!foundInstructions) {
    errors.push({
      skillId,
      path: skillPath,
      error: 'No instructions file found (instructions.md, instructions.mdc, or SKILL.md)',
      severity: 'error',
    });
  }
  
  return errors;
}

/**
 * Validate a single skill directory
 */
async function validateSkill(skillPath: string): Promise<ValidationError[]> {
  const errors: ValidationError[] = [];
  const skillId = basename(skillPath);
  
  // Check for skill.json
  const manifestPath = join(skillPath, 'skill.json');
  try {
    const content = await readFile(manifestPath, 'utf-8');
    let manifest: any;
    
    try {
      manifest = JSON.parse(content);
    } catch {
      errors.push({
        skillId,
        path: manifestPath,
        error: 'Invalid JSON in skill.json',
        severity: 'error',
      });
      return errors;
    }
    
    // Validate manifest
    errors.push(...validateManifest(manifest, skillPath));
  } catch {
    errors.push({
      skillId,
      path: skillPath,
      error: 'Missing skill.json',
      severity: 'error',
    });
    return errors;
  }
  
  // Validate instructions
  errors.push(...await validateInstructions(skillPath));
  
  return errors;
}

/**
 * Find all skill directories recursively
 */
async function findSkillDirectories(basePath: string): Promise<string[]> {
  const skillDirs: string[] = [];
  
  async function scan(dirPath: string, depth: number = 0) {
    if (depth > 3) return;
    
    try {
      const entries = await readdir(dirPath, { withFileTypes: true });
      
      // Check if this is a skill directory
      const hasSkillJson = entries.some(e => e.name === 'skill.json' && e.isFile());
      
      if (hasSkillJson) {
        skillDirs.push(dirPath);
        return;
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
 * Validate all skills in the library
 */
export async function validateAllSkills(libraryPath: string): Promise<ValidationResult> {
  const skillDirs = await findSkillDirectories(libraryPath);
  const allErrors: ValidationError[] = [];
  let validSkills = 0;
  
  for (const skillDir of skillDirs) {
    const errors = await validateSkill(skillDir);
    
    if (errors.filter(e => e.severity === 'error').length === 0) {
      validSkills++;
    }
    
    allErrors.push(...errors);
  }
  
  const errors = allErrors.filter(e => e.severity === 'error');
  const warnings = allErrors.filter(e => e.severity === 'warning');
  
  return {
    valid: errors.length === 0,
    totalSkills: skillDirs.length,
    validSkills,
    errors,
    warnings,
  };
}

/**
 * Format validation results for console output
 */
export function formatValidationResults(result: ValidationResult): string {
  const lines: string[] = [];
  
  lines.push('\n📋 Skill Validation Results\n');
  lines.push(`Total Skills: ${result.totalSkills}`);
  lines.push(`Valid Skills: ${result.validSkills}`);
  lines.push(`Errors: ${result.errors.length}`);
  lines.push(`Warnings: ${result.warnings.length}`);
  
  if (result.errors.length > 0) {
    lines.push('\n❌ Errors:');
    for (const error of result.errors.slice(0, 20)) {
      lines.push(`  [${error.skillId}] ${error.error}`);
      lines.push(`    at ${error.path}`);
    }
    if (result.errors.length > 20) {
      lines.push(`  ... and ${result.errors.length - 20} more errors`);
    }
  }
  
  if (result.warnings.length > 0) {
    lines.push('\n⚠️  Warnings:');
    for (const warning of result.warnings.slice(0, 10)) {
      lines.push(`  [${warning.skillId}] ${warning.error}`);
    }
    if (result.warnings.length > 10) {
      lines.push(`  ... and ${result.warnings.length - 10} more warnings`);
    }
  }
  
  lines.push('');
  
  if (result.valid) {
    lines.push('✅ All skills are valid!');
  } else {
    lines.push('❌ Validation failed. Please fix the errors above.');
  }
  
  return lines.join('\n');
}

// CLI handler
if (process.argv[1]?.endsWith('validator.ts')) {
  const libraryPath = process.argv[2] || './skills-library';
  const strict = process.argv.includes('--strict');
  
  validateAllSkills(libraryPath).then(result => {
    console.log(formatValidationResults(result));
    
    // Exit with error code if validation failed
    if (!result.valid || (strict && result.warnings.length > 0)) {
      process.exit(1);
    }
  }).catch(error => {
    console.error('Validation error:', error);
    process.exit(1);
  });
}
