/**
 * Markdown output generation
 */

import { GITHUB_ORG, SECONDARY_LINKS } from './config.js';
import { RELEVANCE_CONFIG } from './relevance-mapper.js';
import { RepoType, type Repo } from './types.js';

/**
 * Generate markdown content for the ecosystem
 */
export function generateMarkdown(
  repoType: RepoType,
  repos: Repo[],
  role?: string
): string {
  const config = RELEVANCE_CONFIG[repoType] || RELEVANCE_CONFIG[RepoType.GENERIC];

  // Start with header and intro
  const lines: string[] = [
    '## Skene Ecosystem',
    '',
    config.intro,
    ''
  ];

  // Add each repository
  for (const repo of repos) {
    // Heading with link
    lines.push(`### [${repo.name}](${repo.url})`);

    // Benefit line or description
    const content = repo.benefitLine || repo.description || `Explore ${repo.name}`;
    lines.push(content);
    lines.push('');

    // Add secondary link if configured
    const secondaryLink = SECONDARY_LINKS[repo.name];
    if (secondaryLink) {
      lines.push(`**[${secondaryLink.text}](${secondaryLink.url})**`);
      lines.push('');
    }
  }

  // Footer
  lines.push('---');
  lines.push('');
  lines.push(`**Explore all Skene repositories:** https://github.com/${GITHUB_ORG}`);
  lines.push('');

  return lines.join('\n');
}
