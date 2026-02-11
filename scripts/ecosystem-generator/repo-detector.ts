/**
 * Repository type detection
 */

import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { RepoType } from './types.js';

export function detectRepoType(repoRoot: string): RepoType {
  try {
    // Priority 1: Check for Next.js
    const packageJsonPath = join(repoRoot, 'package.json');
    if (existsSync(packageJsonPath)) {
      try {
        const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf8'));
        const allDeps = {
          ...packageJson.dependencies,
          ...packageJson.devDependencies,
          ...packageJson.peerDependencies
        };

        // Check for Next.js
        if (allDeps['next']) {
          return RepoType.NEXTJS;
        }

        // Check for React
        if (allDeps['react']) {
          return RepoType.REACT;
        }

        // Has package.json -> Node.js
        return RepoType.NODE;
      } catch (error) {
        // JSON parse error, continue with other checks
      }
    }

    // Priority 2: Check for Python
    const pythonFiles = [
      'pyproject.toml',
      'requirements.txt',
      'setup.py',
      'Pipfile'
    ];

    for (const file of pythonFiles) {
      if (existsSync(join(repoRoot, file))) {
        return RepoType.PYTHON;
      }
    }

    // Priority 3: Check for docs-heavy structure
    if (isDocsRepository(repoRoot)) {
      return RepoType.DOCS;
    }

    // Default: generic
    return RepoType.GENERIC;
  } catch (error) {
    // On any error, return generic
    return RepoType.GENERIC;
  }
}

function isDocsRepository(repoRoot: string): boolean {
  try {
    // Check for docs directory
    const docsDir = join(repoRoot, 'docs');
    if (existsSync(docsDir) && statSync(docsDir).isDirectory()) {
      // Count markdown files in docs/
      const files = readdirSync(docsDir);
      const mdFiles = files.filter(f => f.endsWith('.md'));
      if (mdFiles.length > 5) {
        return true;
      }
    }

    // Check root directory for many markdown files
    const rootFiles = readdirSync(repoRoot);
    const mdFiles = rootFiles.filter(f => f.endsWith('.md'));

    // If more than 50% of files are markdown and there are at least 5
    const totalFiles = rootFiles.filter(f => {
      const stat = statSync(join(repoRoot, f));
      return stat.isFile();
    });

    if (mdFiles.length >= 5 && mdFiles.length / totalFiles.length > 0.5) {
      return true;
    }

    return false;
  } catch (error) {
    return false;
  }
}
