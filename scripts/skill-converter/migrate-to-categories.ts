/**
 * Migration: Multi-category skills
 *
 * 1. Adds `categories` to canonical skills (anthropic_official, etc.)
 * 2. Removes duplicate skill directories (marketing/* copies)
 *
 * Run with --dry-run to preview, --execute to apply.
 */

import { readFile, writeFile, rm } from 'node:fs/promises';
import { join, resolve } from 'node:path';

const LIBRARY_PATH = resolve(process.cwd(), 'skills-library');

/** Canonical path -> categories to add (where the duplicate lived) */
const MIGRATION_MAP: Array<{
  canonical: string;
  categoriesToAdd: string[];
  duplicateToRemove: string;
}> = [
  {
    canonical: 'anthropic_official/brand-guidelines',
    categoriesToAdd: ['marketing', 'marketing/brand'],
    duplicateToRemove: 'marketing/brand/brand_guidelines',
  },
  {
    canonical: 'anthropic_official/theme-factory',
    categoriesToAdd: ['marketing', 'marketing/brand'],
    duplicateToRemove: 'marketing/brand/theme_factory',
  },
  {
    canonical: 'anthropic_official/canvas-design',
    categoriesToAdd: ['marketing', 'marketing/media'],
    duplicateToRemove: 'marketing/media/canvas_design',
  },
  {
    canonical: 'anthropic_official/docx',
    categoriesToAdd: ['marketing', 'marketing/documents'],
    duplicateToRemove: 'marketing/documents/document_skills_docx',
  },
  {
    canonical: 'anthropic_official/pdf',
    categoriesToAdd: ['marketing', 'marketing/documents'],
    duplicateToRemove: 'marketing/documents/document_skills_pdf',
  },
  {
    canonical: 'anthropic_official/pptx',
    categoriesToAdd: ['marketing', 'marketing/documents'],
    duplicateToRemove: 'marketing/documents/document_skills_pptx',
  },
  {
    canonical: 'anthropic_official/xlsx',
    categoriesToAdd: ['marketing', 'marketing/documents'],
    duplicateToRemove: 'marketing/documents/document_skills_xlsx',
  },
  {
    canonical: 'anthropic_official/internal-comms',
    categoriesToAdd: ['marketing', 'marketing/content'],
    duplicateToRemove: 'marketing/content/internal_comms',
  },
  {
    canonical: 'anthropic_official/webapp-testing',
    categoriesToAdd: ['marketing', 'marketing/tools'],
    duplicateToRemove: 'marketing/tools/webapp_testing',
  },
  {
    canonical: 'anthropic_official/web-artifacts-builder',
    categoriesToAdd: ['marketing', 'marketing/media'],
    duplicateToRemove: 'marketing/media/artifacts_builder',
  },
  {
    canonical: 'anthropic_official/mcp-builder',
    categoriesToAdd: ['marketing', 'marketing/tools'],
    duplicateToRemove: 'marketing/tools/mcp_builder',
  },
  {
    canonical: 'anthropic_official/skill-creator',
    categoriesToAdd: ['marketing', 'marketing/tools'],
    duplicateToRemove: 'marketing/tools/skill_creator',
  },
];

async function addCategoriesToManifest(
  skillPath: string,
  categoriesToAdd: string[],
  dryRun: boolean
): Promise<boolean> {
  const manifestPath = join(skillPath, 'skill.json');
  try {
    const content = await readFile(manifestPath, 'utf-8');
    const manifest = JSON.parse(content);

    const existing = manifest.categories ?? [];
    const merged = [...new Set([...existing, ...categoriesToAdd])];
    manifest.categories = merged.sort();

    if (dryRun) {
      console.log(`  [dry-run] Would add categories to ${skillPath}: ${merged.join(', ')}`);
      return true;
    }

    await writeFile(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
    console.log(`  ✓ Added categories to ${manifestPath}: ${merged.join(', ')}`);
    return true;
  } catch (err) {
    console.error(`  ✗ Failed to update ${manifestPath}:`, err);
    return false;
  }
}

async function removeDuplicateDir(dupPath: string, dryRun: boolean): Promise<boolean> {
  const fullPath = join(LIBRARY_PATH, dupPath);
  try {
    if (dryRun) {
      console.log(`  [dry-run] Would remove ${dupPath}`);
      return true;
    }
    await rm(fullPath, { recursive: true });
    console.log(`  ✓ Removed ${dupPath}`);
    return true;
  } catch (err) {
    console.error(`  ✗ Failed to remove ${dupPath}:`, err);
    return false;
  }
}

async function run(dryRun: boolean) {
  console.log('\n📦 Multi-category migration');
  console.log(dryRun ? '   (dry-run — no changes)\n' : '   (executing)\n');

  let ok = 0;
  let fail = 0;

  for (const { canonical, categoriesToAdd, duplicateToRemove } of MIGRATION_MAP) {
    const canonicalPath = join(LIBRARY_PATH, canonical);
    console.log(`\n${canonical} → ${duplicateToRemove}`);

    const a = await addCategoriesToManifest(canonicalPath, categoriesToAdd, dryRun);
    const b = await removeDuplicateDir(duplicateToRemove, dryRun);

    if (a && b) ok++;
    else fail++;
  }

  console.log('\n---');
  console.log(`Done. ${ok} migrated, ${fail} failed.`);
  if (dryRun) {
    console.log('\nRun with --execute to apply changes.');
  }
  console.log('');
}

const args = process.argv.slice(2);
const dryRun = !args.includes('--execute');

run(dryRun).catch((err) => {
  console.error('Migration failed:', err);
  process.exit(1);
});
