/**
 * Configuration constants for Ecosystem Generator
 */

export const GITHUB_ORG = 'SkeneTechnologies';

export const CACHE_TTL_MS = 3600000; // 1 hour

export const CACHE_DIR_NAME = '.skene/cache';

export const GITHUB_API_BASE = 'https://api.github.com';

export const REQUEST_TIMEOUT_MS = 5000;

export const MAX_RETRIES = 1;

export const KNOWN_REPOS = [
  'skene-cookbook',
  'skene-dashboard',
  'skene-flow',
  'skene-growth',
  'skene-strategy',
  'skene-prototypes',
  'skene-marketing',
  'skene-docs'
];

export const SECONDARY_LINKS: Record<string, { text: string; url: string }> = {
  'skene-cookbook': {
    text: 'Browse skill chains →',
    url: 'https://github.com/SkeneTechnologies/skene-cookbook/blob/main/docs/SKILL_CHAINS.md'
  }
};
