#!/usr/bin/env npx tsx
/**
 * Skene Ecosystem Generator CLI
 *
 * Generates tailored ecosystem recommendations based on host repository type
 *
 * Usage:
 *   npx skills-directory ecosystem
 *   npx skills-directory ecosystem --output ECOSYSTEM.md
 *   npx skills-directory ecosystem --no-cache
 *   npx skills-directory ecosystem --role frontend
 */

import { writeFileSync } from 'node:fs';
import { GITHUB_ORG } from './config.js';
import { CacheManager } from './cache-manager.js';
import { GitHubClient } from './github-client.js';
import { detectRepoType } from './repo-detector.js';
import { getRelevantRepos } from './relevance-mapper.js';
import { generateMarkdown } from './markdown-generator.js';
import type { EcosystemOptions, Repo } from './types.js';

/**
 * Generate ecosystem content
 */
export async function generateEcosystem(options: EcosystemOptions): Promise<string> {
  try {
    const { repoRoot, output, noCache, role, autoMode } = options;

    // Initialize cache manager
    const cache = new CacheManager(repoRoot);

    // Clear cache if requested
    if (noCache) {
      cache.clear();
    }

    // Detect repository type
    const repoType = detectRepoType(repoRoot);

    // Initialize GitHub client
    const github = new GitHubClient();

    // Fetch organization repos (with cache)
    let repos: Repo[] = [];
    const cacheKey = `org-repos-${GITHUB_ORG}`;

    if (!noCache) {
      const cached = cache.get(cacheKey);
      if (cached) {
        repos = cached;
        if (!autoMode) {
          console.log('✓ Using cached repository list');
        }
      }
    }

    if (repos.length === 0) {
      if (!autoMode) {
        console.log(`Fetching repositories from ${GITHUB_ORG}...`);
      }
      repos = await github.listOrgRepos(GITHUB_ORG);

      if (repos.length > 0) {
        cache.set(cacheKey, repos);
      }
    }

    // Fetch README for each repo and extract benefit line (with cache)
    for (const repo of repos) {
      const readmeCacheKey = `readme-${repo.name}`;

      if (!noCache) {
        const cached = cache.get(readmeCacheKey);
        if (cached !== null) {
          repo.benefitLine = cached;
          continue;
        }
      }

      if (!autoMode) {
        console.log(`Extracting benefits from ${repo.name}...`);
      }

      const readme = await github.fetchReadme(GITHUB_ORG, repo.name);
      const benefitLine = github.extractBenefitLine(readme);

      repo.benefitLine = benefitLine;
      cache.set(readmeCacheKey, benefitLine);
    }

    // Order repos by relevance
    const orderedRepos = getRelevantRepos(repoType, repos, role);

    // Generate markdown
    const markdown = generateMarkdown(repoType, orderedRepos, role);

    // Write to file if output specified
    if (output) {
      writeFileSync(output, markdown, 'utf8');
      if (!autoMode) {
        console.log(`\n✅ Ecosystem content written to ${output}`);
      }
    }

    return markdown;
  } catch (error) {
    console.error('Error generating ecosystem:', (error as Error).message);

    // Fallback to generic message
    const fallback = `## Skene Ecosystem

Explore the Skene ecosystem:

### [skene-cookbook](https://github.com/${GITHUB_ORG}/skene-cookbook)
760+ AI skills for Claude and Cursor. Build agents in days, not months.

### [skene-flow](https://github.com/${GITHUB_ORG}/skene-flow)
Orchestrate AI agents and workflows with visual designer and execution engine.

### [skene-dashboard](https://github.com/${GITHUB_ORG}/skene-dashboard)
Production-ready dashboard components and templates for SaaS applications.

---

**Explore all Skene repositories:** https://github.com/${GITHUB_ORG}
`;

    if (options.output) {
      try {
        writeFileSync(options.output, fallback, 'utf8');
      } catch {
        // Silent failure
      }
    }

    return fallback;
  }
}
