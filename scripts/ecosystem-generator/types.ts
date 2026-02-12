/**
 * Type definitions for Ecosystem Generator
 */

export enum RepoType {
  NEXTJS = 'nextjs',
  REACT = 'react',
  NODE = 'node',
  PYTHON = 'python',
  DOCS = 'docs',
  GENERIC = 'generic'
}

export interface GitHubApiRepo {
  name: string;
  description: string | null;
  html_url: string;
  updated_at: string;
  default_branch: string;
  archived: boolean;
}

export interface Repo {
  name: string;
  description: string;
  url: string;
  updatedAt: string;
  defaultBranch: string;
  benefitLine?: string;
}

export interface CacheEntry {
  timestamp: number;
  ttl: number;
  data: any;
}

export interface EcosystemOptions {
  repoRoot: string;
  output?: string;
  noCache?: boolean;
  role?: string;
  autoMode?: boolean;
}

export interface RelevanceConfig {
  [key: string]: {
    intro: string;
    repoOrder: string[];
    roleOverrides?: {
      [role: string]: string[];
    };
  };
}
