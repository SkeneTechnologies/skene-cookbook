#!/usr/bin/env npx tsx
/**
 * Skills Overlap Analyzer
 *
 * Groups skills by normalized id (manifest.id or path segment) and reports
 * duplicates (multiple paths sharing the same id).
 *
 * Usage:
 *   npx tsx scripts/skill-converter/overlap-analyzer.ts [path]
 *   npm run skills:check-overlap
 */

import { writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join, dirname, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { findSkillDirectories, loadManifest, loadInstructionsContent } from './check-unique.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..', '..');

interface OverlapDuplicate {
  id: string;
  paths: string[];
  canonical?: string;
  instructionSimilarity?: Array<{ pathA: string; pathB: string; overlapPct: number }>;
}

interface OverlapReport {
  total: number;
  duplicates: OverlapDuplicate[];
}

function normalizeId(id: string): string {
  return id.toLowerCase().replace(/[^a-z0-9-]/g, '-');
}

function tokenize(text: string): Set<string> {
  return new Set(text.toLowerCase().replace(/\s+/g, ' ').trim().split(' ').filter(Boolean));
}

function jaccardOverlap(a: Set<string>, b: Set<string>): number {
  if (a.size === 0 && b.size === 0) return 1;
  const intersection = [...a].filter((x) => b.has(x)).length;
  const union = new Set([...a, ...b]).size;
  return union === 0 ? 0 : intersection / union;
}

function printHelp(): void {
  console.log(`Skills Overlap Analyzer

Groups skills by normalized id and reports duplicates (multiple paths sharing same id).

Usage:
  npx tsx scripts/skill-converter/overlap-analyzer.ts [path]
  npm run skills:check-overlap

Options:
  --output PATH     Write JSON report (default: docs/requirement-extraction/audit-outputs/overlap-report.json)
  --no-similarity   Skip instruction similarity (faster; default when many skills)
  -h, --help        Show this help

Output:
  Human-readable summary to stdout, JSON to file.
`);
}

async function analyzeOverlap(
  libraryPath: string,
  includeSimilarity: boolean
): Promise<OverlapReport> {
  const absPath = resolve(libraryPath);
  const skillDirs = await findSkillDirectories(absPath);
  const byId = new Map<string, string[]>();
  const pathToDir = new Map<string, string>();

  for (const skillDir of skillDirs) {
    const relPath = relative(absPath, skillDir) || skillDir;
    const pathId = relPath.replace(/\\/g, '/');
    pathToDir.set(pathId, skillDir);
    const manifest = await loadManifest(skillDir);
    const manifestId = (manifest?.id as string) ?? null;
    const id = manifestId ?? pathId.split('/').pop() ?? pathId;
    const normalized = normalizeId(id);

    if (!byId.has(normalized)) {
      byId.set(normalized, []);
    }
    byId.get(normalized)!.push(pathId);
  }

  const duplicates: OverlapDuplicate[] = [];
  for (const [id, paths] of byId) {
    if (paths.length > 1) {
      const canonical = paths.slice().sort()[0];
      const dup: OverlapDuplicate = { id, paths, canonical };

      if (includeSimilarity) {
        const similarityPairs: Array<{ pathA: string; pathB: string; overlapPct: number }> = [];
        const tokensByPath = new Map<string, Set<string>>();
        for (const p of paths) {
          const dir = pathToDir.get(p);
          if (dir) {
            const content = await loadInstructionsContent(dir);
            const text = (content ?? '').slice(0, 500);
            tokensByPath.set(p, tokenize(text));
          }
        }
        for (let i = 0; i < paths.length; i++) {
          for (let j = i + 1; j < paths.length; j++) {
            const ta = tokensByPath.get(paths[i]);
            const tb = tokensByPath.get(paths[j]);
            if (ta && tb) {
              const pct = Math.round(jaccardOverlap(ta, tb) * 100);
              similarityPairs.push({ pathA: paths[i], pathB: paths[j], overlapPct: pct });
            }
          }
        }
        if (similarityPairs.length > 0) {
          dup.instructionSimilarity = similarityPairs;
        }
      }
      duplicates.push(dup);
    }
  }

  return { total: skillDirs.length, duplicates };
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const help = args.includes('-h') || args.includes('--help');
  const outputIdx = args.indexOf('--output');
  const outputPath =
    outputIdx >= 0 && args[outputIdx + 1]
      ? join(process.cwd(), args[outputIdx + 1])
      : join(ROOT, 'docs', 'requirement-extraction', 'audit-outputs', 'overlap-report.json');

  const libraryPath = args.find((a) => !a.startsWith('-')) ?? './skills-library';
  const includeSimilarity = !args.includes('--no-similarity');

  if (help) {
    printHelp();
    process.exit(0);
  }

  const report = await analyzeOverlap(libraryPath, includeSimilarity);

  console.log('\n📋 Skills Overlap Analysis\n');
  console.log(`Total skills: ${report.total}`);
  console.log(`Duplicate ids: ${report.duplicates.length}`);
  console.log('');

  if (report.duplicates.length > 0) {
    console.log('❌ Duplicates (multiple paths share same id):');
    for (const d of report.duplicates) {
      console.log(`  id: "${d.id}"`);
      console.log(`    canonical: ${d.canonical}`);
      for (const p of d.paths) {
        console.log(`    - ${p}`);
      }
      if (d.instructionSimilarity?.length) {
        for (const s of d.instructionSimilarity) {
          console.log(`    instruction overlap ${s.pathA} ↔ ${s.pathB}: ${s.overlapPct}%`);
        }
      }
      console.log('');
    }
  } else {
    console.log('✅ No overlap duplicates found.');
  }

  const outDir = dirname(outputPath);
  if (!existsSync(outDir)) {
    mkdirSync(outDir, { recursive: true });
  }
  writeFileSync(outputPath, JSON.stringify(report, null, 2));
  console.log(`Report written to ${outputPath}`);

  process.exit(report.duplicates.length > 0 ? 1 : 0);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
