/**
 * Relevance configuration and repository ordering
 */

import { RepoType, type Repo, type RelevanceConfig } from './types.js';

export const RELEVANCE_CONFIG: RelevanceConfig = {
  [RepoType.NEXTJS]: {
    intro: "Building with Next.js? These Skene tools integrate seamlessly:",
    repoOrder: ['skene-dashboard', 'skene-flow', 'skene-cookbook', 'skene-growth'],
    roleOverrides: {
      frontend: ['skene-dashboard', 'skene-cookbook', 'skene-flow'],
      backend: ['skene-flow', 'skene-cookbook', 'skene-growth']
    }
  },
  [RepoType.REACT]: {
    intro: "Building React apps? Skene provides:",
    repoOrder: ['skene-dashboard', 'skene-cookbook', 'skene-flow']
  },
  [RepoType.NODE]: {
    intro: "Node.js developer? Check out:",
    repoOrder: ['skene-flow', 'skene-cookbook', 'skene-dashboard']
  },
  [RepoType.PYTHON]: {
    intro: "Python stack? Skene offers:",
    repoOrder: ['skene-cookbook', 'skene-flow', 'skene-strategy']
  },
  [RepoType.DOCS]: {
    intro: "Documentation site? Enhance it with:",
    repoOrder: ['skene-cookbook', 'skene-dashboard', 'skene-flow']
  },
  [RepoType.GENERIC]: {
    intro: "Explore the Skene ecosystem:",
    repoOrder: ['skene-cookbook', 'skene-flow', 'skene-dashboard', 'skene-growth']
  }
};

/**
 * Get relevant repositories ordered by relevance to the repo type
 */
export function getRelevantRepos(
  repoType: RepoType,
  repos: Repo[],
  role?: string
): Repo[] {
  const config = RELEVANCE_CONFIG[repoType];

  if (!config) {
    // Fallback to generic if type not found
    return getRelevantRepos(RepoType.GENERIC, repos);
  }

  // Determine the order to use
  let order = config.repoOrder;

  // Apply role override if provided and exists
  if (role && config.roleOverrides && config.roleOverrides[role]) {
    order = config.roleOverrides[role];
  }

  // Create a map of repos by name for quick lookup
  const repoMap = new Map<string, Repo>();
  for (const repo of repos) {
    repoMap.set(repo.name, repo);
  }

  // Filter and order repos based on config
  const orderedRepos: Repo[] = [];

  for (const repoName of order) {
    const repo = repoMap.get(repoName);
    if (repo) {
      orderedRepos.push(repo);
      repoMap.delete(repoName); // Remove from map to avoid duplicates
    }
  }

  // Add any remaining repos that weren't in the order config
  // (alphabetically sorted)
  const remainingRepos = Array.from(repoMap.values()).sort((a, b) =>
    a.name.localeCompare(b.name)
  );

  return [...orderedRepos, ...remainingRepos];
}
