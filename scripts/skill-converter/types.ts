/**
 * Unified Skill Types
 * 
 * Schema that supports Claude, Cursor, and SkeneFlow platforms
 */

// Platform-specific configuration
export interface ClaudePlatformConfig {
  /** Natural language triggers for skill activation */
  triggers?: string[];
  /** License information */
  license?: string;
}

export interface CursorPlatformConfig {
  /** File glob patterns that trigger this skill */
  globs?: string[];
  /** Always apply to all files (default: false) */
  alwaysApply?: boolean;
}

export interface SkeneFlowPlatformConfig {
  /** MCP tools required by this skill */
  tools?: Array<{ name: string; required: boolean }>;
  /** Possible exit states for state machine transitions */
  exitStates?: string[];
  /** JSON schema for skill inputs */
  inputSchema?: Record<string, unknown>;
  /** JSON schema for skill outputs */
  outputSchema?: Record<string, unknown>;
  /** Success metrics and benchmarks */
  metrics?: {
    primary: string;
    benchmarks?: Record<string, string>;
  };
}

// Unified skill manifest
export interface UnifiedSkillManifest {
  /** Unique skill identifier (domain/name format) */
  id: string;
  /** Semantic version */
  version: string;
  /** Human-readable name */
  name: string;
  /** Detailed description (used for triggering in Claude) */
  description: string;
  /** Domain/category (plg, security, cursor_rules, etc.) */
  domain: string;
  /**
   * Additional categories for multi-category discovery.
   * A skill can appear in multiple categories (e.g. anthropic_official + marketing/documents)
   * without duplicating files. Falls back to [domain] if not set.
   */
  categories?: string[];
  /** Source of the skill (native, anthropic, community, external) */
  source?: 'native' | 'anthropic' | 'community' | 'external';
  /** Human-readable origin (e.g. "Skene PLG frameworks") */
  origin?: string;
  /** Attribution URL or text */
  attribution?: string;
  /** License (e.g. MIT, Apache-2.0) */
  license?: string;
  /** Optional maintainer or org */
  maintainer?: string;
  /** Skill tags for discovery */
  tags?: string[];
  /** LLM temperature setting (0 = deterministic) */
  temperature?: number;
  
  /** Platform-specific configurations */
  platforms?: {
    claude?: ClaudePlatformConfig;
    cursor?: CursorPlatformConfig;
    skeneflow?: SkeneFlowPlatformConfig;
  };
}

// Loaded skill with instructions
export interface LoadedSkill {
  manifest: UnifiedSkillManifest;
  instructions: string;
  /** Additional reference files */
  references?: Record<string, string>;
  /** Source path */
  sourcePath: string;
}

// Export format types
export type ExportFormat = 'claude' | 'cursor' | 'skeneflow';

// Export options
export interface ExportOptions {
  format: ExportFormat;
  outputDir: string;
  /** Only export skills matching these domains */
  domains?: string[];
  /** Only export skills matching these tags */
  tags?: string[];
  /** Include reference files */
  includeReferences?: boolean;
}

// Install target types
export type InstallTarget = 'claude' | 'cursor' | 'skeneflow' | 'all';

export interface InstallOptions {
  target: InstallTarget;
  /** Cursor: path to .cursor/rules/ directory */
  cursorPath?: string;
  /** Claude: path to skills directory */
  claudePath?: string;
  /** SkeneFlow: register with skill registry */
  skeneflowRegistry?: boolean;
  /** Use symlinks instead of copying */
  symlink?: boolean;
  /** Skills to install (all if empty) */
  skills?: string[];
  /** Domains to install (all if empty) */
  domains?: string[];
}

// Domain to glob mapping for cursor rules generation
export const DOMAIN_GLOB_MAPPING: Record<string, string[]> = {
  // Development domains
  'cursor_rules': ['**/*'],
  'development': ['**/*.{js,jsx,ts,tsx,py,go,rs,java,rb,php}'],
  'superpowers': ['**/*'],
  'security': ['**/*'],
  
  // Scientific domains (Python-focused)
  'scientific': ['**/*.{py,ipynb,R,jl}'],
  
  // PLG/Business domains (typically TypeScript apps)
  'plg': ['**/*.{ts,tsx,js,jsx}'],
  'plg_frameworks': ['**/*.{ts,tsx,js,jsx,md}'],
  'monetization': ['**/*.{ts,tsx,js,jsx}'],
  'revops': ['**/*.{ts,tsx,js,jsx}'],
  'customer_success': ['**/*.{ts,tsx,js,jsx}'],
  'ecosystem': ['**/*.{ts,tsx,js,jsx}'],
  'marketing': ['**/*.{ts,tsx,js,jsx,md}'],
  
  // Ops domains
  'ai_ops': ['**/*.{ts,tsx,js,jsx,py}'],
  'data_ops': ['**/*.{sql,py,ts}'],
  'devex': ['**/*'],
  'finops': ['**/*.{ts,tsx,js,jsx}'],
  'product_ops': ['**/*.{ts,tsx,js,jsx}'],
  'support_ops': ['**/*.{ts,tsx,js,jsx}'],
  'people_ops': ['**/*'],
  
  // Other
  'anthropic_official': ['**/*'],
  'community': ['**/*'],
  'compliance': ['**/*'],
  'meta': ['**/*'],
  'skene': ['**/*'],
  'vcf': ['**/*'],
};
