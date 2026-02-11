/**
 * GitHub API client
 */

import { GITHUB_API_BASE, REQUEST_TIMEOUT_MS, MAX_RETRIES } from './config.js';
import type { GitHubApiRepo, Repo } from './types.js';

export class GitHubClient {
  private token?: string;

  constructor(token?: string) {
    this.token = token || process.env.GITHUB_TOKEN;
  }

  /**
   * List all public repositories for an organization
   */
  async listOrgRepos(org: string): Promise<Repo[]> {
    try {
      const url = `${GITHUB_API_BASE}/orgs/${org}/repos?per_page=100&type=public`;
      const response = await this.fetchWithRetry(url);

      if (!response.ok) {
        if (response.status === 403) {
          console.warn('⚠️  GitHub rate limit reached. Using cached data if available.');
          return [];
        }
        if (response.status === 404) {
          console.warn(`⚠️  Organization ${org} not found.`);
          return [];
        }
        throw new Error(`GitHub API error: ${response.status}`);
      }

      const data = (await response.json()) as GitHubApiRepo[];

      // Filter out archived repos and map to our Repo interface
      return data
        .filter(repo => !repo.archived)
        .map(repo => ({
          name: repo.name,
          description: repo.description || '',
          url: repo.html_url,
          updatedAt: repo.updated_at,
          defaultBranch: repo.default_branch
        }));
    } catch (error) {
      if ((error as Error).name === 'AbortError') {
        console.warn('⚠️  GitHub API request timed out.');
        return [];
      }
      console.error('Error fetching repos:', (error as Error).message);
      return [];
    }
  }

  /**
   * Fetch README content for a repository
   */
  async fetchReadme(owner: string, repo: string): Promise<string> {
    try {
      const url = `${GITHUB_API_BASE}/repos/${owner}/${repo}/readme`;
      const response = await this.fetchWithRetry(url);

      if (!response.ok) {
        if (response.status === 404) {
          // No README found, return empty string
          return '';
        }
        throw new Error(`GitHub API error: ${response.status}`);
      }

      const data = await response.json();

      // Decode base64 content
      if (data.content && data.encoding === 'base64') {
        return Buffer.from(data.content, 'base64').toString('utf8');
      }

      return '';
    } catch (error) {
      if ((error as Error).name === 'AbortError') {
        console.warn(`⚠️  README fetch timed out for ${repo}`);
        return '';
      }
      // Silent failure - README is optional
      return '';
    }
  }

  /**
   * Extract benefit-oriented line from README
   */
  extractBenefitLine(readme: string): string {
    if (!readme) return '';

    const lines = readme.split('\n');
    let inCodeBlock = false;

    for (const line of lines) {
      const trimmed = line.trim();

      // Track code block state
      if (trimmed.startsWith('```')) {
        inCodeBlock = !inCodeBlock;
        continue;
      }

      // Skip if in code block
      if (inCodeBlock) continue;

      // Skip empty lines
      if (!trimmed) continue;

      // Skip titles (lines starting with #)
      if (trimmed.startsWith('#')) continue;

      // Skip badges (![...]) - check if line contains badge markdown
      if (trimmed.includes('![') || trimmed.match(/^\[!\[/)) continue;

      // Skip horizontal rules
      if (trimmed.match(/^[-*_]{3,}$/)) continue;

      // Skip lines that are mostly links/badges
      if (trimmed.match(/^\[.*\]\(.*\)$/)) continue;

      // Find first paragraph with meaningful content (>50 chars)
      if (trimmed.length > 50) {
        // Clean up markdown formatting
        let cleaned = trimmed
          // Remove links [text](url) -> text
          .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
          // Remove bold **text** -> text
          .replace(/\*\*([^*]+)\*\*/g, '$1')
          // Remove italic *text* -> text
          .replace(/\*([^*]+)\*/g, '$1')
          // Remove inline code `code` -> code
          .replace(/`([^`]+)`/g, '$1')
          // Remove HTML tags
          .replace(/<[^>]+>/g, '');

        // Truncate if too long
        if (cleaned.length > 120) {
          cleaned = cleaned.substring(0, 117) + '…';
        }

        return cleaned;
      }
    }

    return '';
  }

  /**
   * Fetch with timeout and retry logic
   */
  private async fetchWithRetry(url: string, retries = MAX_RETRIES): Promise<Response> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    const headers: Record<string, string> = {
      Accept: 'application/vnd.github.v3+json'
    };

    if (this.token) {
      headers.Authorization = `token ${this.token}`;
    }

    try {
      const response = await fetch(url, {
        headers,
        signal: controller.signal
      });

      clearTimeout(timeout);
      return response;
    } catch (error) {
      clearTimeout(timeout);

      // Retry on timeout
      if ((error as Error).name === 'AbortError' && retries > 0) {
        // Wait 1 second before retrying
        await new Promise(resolve => setTimeout(resolve, 1000));
        return this.fetchWithRetry(url, retries - 1);
      }

      throw error;
    }
  }
}
