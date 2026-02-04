/**
 * Skill Uniqueness Checker
 *
 * Validates that all skills are unique by:
 * - Path: domain/skill-name (filesystem location)
 * - manifest.id: id field in skill.json
 * - Content: instructions body hash, description (exact duplicates)
 */

import { readFile, readdir } from 'node:fs/promises';
import { join, relative, resolve } from 'node:path';
import { createHash } from 'node:crypto';

export async function findSkillDirectories(basePath: string): Promise<string[]> {
  const skillDirs: string[] = [];

  async function scan(dirPath: string, depth: number = 0) {
    if (depth > 3) return;

    try {
      const entries = await readdir(dirPath, { withFileTypes: true });
      const hasSkillJson = entries.some((e) => e.name === 'skill.json' && e.isFile());

      if (hasSkillJson) {
        skillDirs.push(dirPath);
        return;
      }

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

export async function loadManifest(skillPath: string): Promise<Record<string, unknown> | null> {
  try {
    const content = await readFile(join(skillPath, 'skill.json'), 'utf-8');
    return JSON.parse(content);
  } catch {
    return null;
  }
}

export async function loadInstructionsContent(skillPath: string): Promise<string | null> {
  const candidates = ['instructions.md', 'instructions.mdc', 'SKILL.md'];
  for (const name of candidates) {
    try {
      const content = await readFile(join(skillPath, name), 'utf-8');
      const body = content.replace(/^---[\s\S]*?---\n?/, '').trim();
      return body.replace(/\s+/g, ' ');
    } catch {
      continue;
    }
  }
  return null;
}

function hashContent(content: string): string {
  return createHash('sha256').update(content).digest('hex').slice(0, 16);
}

interface UniquenessResult {
  total: number;
  uniqueByPath: boolean;
  uniqueById: boolean;
  uniqueByContent: boolean;
  pathDuplicates: Array<{ path: string; skills: string[] }>;
  idDuplicates: Array<{ id: string; paths: string[] }>;
  instructionsDuplicates: Array<{ hash: string; paths: string[]; preview?: string }>;
  descriptionDuplicates: Array<{ description: string; paths: string[] }>;
  idMismatches: Array<{ path: string; pathId: string; manifestId: string }>;
}

export async function checkSkillUniqueness(libraryPath: string): Promise<UniquenessResult> {
  const absLibraryPath = resolve(libraryPath);
  const skillDirs = await findSkillDirectories(absLibraryPath);

  const byPath = new Map<string, string[]>();
  const byManifestId = new Map<string, string[]>();
  const byInstructionsHash = new Map<string, { paths: string[]; preview: string }>();
  const byDescription = new Map<string, string[]>();
  const idMismatches: UniquenessResult['idMismatches'] = [];

  for (const skillDir of skillDirs) {
    const relPath = relative(absLibraryPath, skillDir) || skillDir;
    const pathId = relPath.replace(/\\/g, '/');

    const manifest = await loadManifest(skillDir);
    const manifestId = (manifest?.id as string) ?? null;

    // Track by path (path is always unique - one dir = one path)
    if (!byPath.has(pathId)) {
      byPath.set(pathId, []);
    }
    byPath.get(pathId)!.push(skillDir);

    // Track by manifest.id
    const id = manifestId ?? pathId;
    if (!byManifestId.has(id)) {
      byManifestId.set(id, []);
    }
    byManifestId.get(id)!.push(skillDir);

    // Check if manifest.id differs from path-based id
    if (manifestId && manifestId !== pathId) {
      idMismatches.push({ path: skillDir, pathId, manifestId });
    }

    // Content-based uniqueness: instructions hash
    const instructionsContent = await loadInstructionsContent(skillDir);
    if (instructionsContent && instructionsContent.length > 50) {
      const hash = hashContent(instructionsContent);
      const preview = instructionsContent.slice(0, 80).replace(/\n/g, ' ');
      if (!byInstructionsHash.has(hash)) {
        byInstructionsHash.set(hash, { paths: [], preview });
      }
      byInstructionsHash.get(hash)!.paths.push(pathId);
    }

    // Content-based uniqueness: description (exact match)
    const description = (manifest?.description as string)?.trim();
    if (description && description.length > 30) {
      if (!byDescription.has(description)) {
        byDescription.set(description, []);
      }
      byDescription.get(description)!.push(pathId);
    }
  }

  const pathDuplicates = [...byPath.entries()]
    .filter(([, paths]) => paths.length > 1)
    .map(([path, paths]) => ({ path, skills: paths }));

  const idDuplicates = [...byManifestId.entries()]
    .filter(([, paths]) => paths.length > 1)
    .map(([id, paths]) => ({ id, paths }));

  const instructionsDuplicates = [...byInstructionsHash.entries()]
    .filter(([, v]) => v.paths.length > 1)
    .map(([hash, v]) => ({ hash, paths: v.paths, preview: v.preview }));

  const descriptionDuplicates = [...byDescription.entries()]
    .filter(([, paths]) => paths.length > 1)
    .map(([description, paths]) => ({ description, paths }));

  const contentUnique =
    instructionsDuplicates.length === 0 && descriptionDuplicates.length === 0;

  return {
    total: skillDirs.length,
    uniqueByPath: pathDuplicates.length === 0,
    uniqueById: idDuplicates.length === 0,
    uniqueByContent: contentUnique,
    pathDuplicates,
    idDuplicates,
    instructionsDuplicates,
    descriptionDuplicates,
    idMismatches,
  };
}

function formatResult(result: UniquenessResult, _libraryPath: string): string {
  const lines: string[] = [];

  lines.push('\n📋 Skill Uniqueness Validation\n');
  lines.push(`Total skills: ${result.total}`);
  lines.push(`Unique by path: ${result.uniqueByPath ? '✅ Yes' : '❌ No'}`);
  lines.push(`Unique by manifest.id: ${result.uniqueById ? '✅ Yes' : '❌ No'}`);
  lines.push(`Unique by content: ${result.uniqueByContent ? '✅ Yes' : '❌ No'}`);
  lines.push('');

  if (result.pathDuplicates.length > 0) {
    lines.push('❌ Duplicate paths (same directory counted twice - unexpected):');
    for (const { path, skills } of result.pathDuplicates) {
      lines.push(`  ${path}:`);
      skills.forEach((s) => lines.push(`    - ${s}`));
    }
    lines.push('');
  }

  if (result.idDuplicates.length > 0) {
    lines.push('❌ Duplicate manifest.id (multiple skills share same id):');
    for (const { id, paths } of result.idDuplicates) {
      lines.push(`  id: "${id}"`);
      paths.forEach((p) => lines.push(`    - ${p}`));
    }
    lines.push('');
  }

  if (result.instructionsDuplicates.length > 0) {
    lines.push('❌ Duplicate instructions content (identical instruction bodies):');
    for (const { hash, paths, preview } of result.instructionsDuplicates) {
      lines.push(`  hash: ${hash}`);
      lines.push(`  preview: "${(preview ?? '').slice(0, 60)}..."`);
      paths.forEach((p) => lines.push(`    - ${p}`));
    }
    lines.push('');
  }

  if (result.descriptionDuplicates.length > 0) {
    lines.push('❌ Duplicate descriptions (exact same description in skill.json):');
    for (const { description, paths } of result.descriptionDuplicates) {
      lines.push(`  "${description.slice(0, 80)}${description.length > 80 ? '...' : ''}"`);
      paths.forEach((p) => lines.push(`    - ${p}`));
    }
    lines.push('');
  }

  if (result.idMismatches.length > 0) {
    lines.push('⚠️  Path vs manifest.id mismatches (path differs from id):');
    for (const { pathId, manifestId } of result.idMismatches.slice(0, 20)) {
      lines.push(`  path: ${pathId}  →  manifest.id: ${manifestId}`);
    }
    if (result.idMismatches.length > 20) {
      lines.push(`  ... and ${result.idMismatches.length - 20} more`);
    }
    lines.push('');
  }

  const allUnique =
    result.uniqueByPath && result.uniqueById && result.uniqueByContent;
  if (allUnique) {
    lines.push('✅ All skills are unique (by path, manifest.id, and content)!');
  } else if (result.instructionsDuplicates.length > 0 || result.descriptionDuplicates.length > 0) {
    lines.push('❌ Content duplicates found. Review instructions and descriptions above.');
  } else {
    lines.push('❌ Uniqueness validation failed. See duplicates above.');
  }

  lines.push('');
  return lines.join('\n');
}

// CLI
if (process.argv[1]?.includes('check-unique')) {
  const libraryPath = process.argv[2] || './skills-library';

  checkSkillUniqueness(libraryPath)
    .then((result) => {
      console.log(formatResult(result, libraryPath));
      const ok =
        result.uniqueByPath && result.uniqueById && result.uniqueByContent;
      process.exit(ok ? 0 : 1);
    })
    .catch((err) => {
      console.error('Uniqueness check failed:', err);
      process.exit(1);
    });
}
