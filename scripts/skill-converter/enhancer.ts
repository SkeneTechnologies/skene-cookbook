/**
 * Skill Enhancer
 * 
 * Enhances skills with:
 * - Claude triggers (natural language activation patterns)
 * - SkeneFlow tools (MCP tool integrations)
 * - Quality tiers (verified, community, experimental)
 */

import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import type { LoadedSkill, UnifiedSkillManifest } from './types.js';
import { loadAllSkills } from './loader.js';

// Quality tier definitions
export type QualityTier = 'verified' | 'community' | 'experimental';

// Domain to quality tier mapping (based on source)
const DOMAIN_QUALITY_TIERS: Record<string, QualityTier> = {
  'anthropic_official': 'verified',
  'cursor_rules': 'verified',
  'security': 'verified',
  'superpowers': 'verified',
  'plg': 'verified',
  'plg_frameworks': 'verified',
  'scientific': 'community',
  'marketing': 'community',
  'revops': 'community',
  'customer_success': 'community',
  'monetization': 'community',
  'ai_ops': 'community',
  'product_ops': 'community',
  'ecosystem': 'community',
  'devex': 'community',
  'development': 'community',
  'support_ops': 'community',
  'finops': 'community',
  'data_ops': 'community',
  'compliance': 'community',
  'people_ops': 'community',
  'community': 'community',
  'meta': 'experimental',
  'skene': 'experimental',
  'vcf': 'experimental',
};

// Claude trigger patterns by domain
const CLAUDE_TRIGGER_PATTERNS: Record<string, string[]> = {
  'plg': [
    'help with activation',
    'improve onboarding',
    'reduce churn',
    'increase conversion',
    'product-led growth',
  ],
  'plg_frameworks': [
    'PLG strategy',
    'growth framework',
    'pricing strategy',
    'trial optimization',
    'feature adoption',
  ],
  'security': [
    'security audit',
    'vulnerability analysis',
    'code security',
    'secure coding',
    'penetration testing',
  ],
  'superpowers': [
    'systematic debugging',
    'code review',
    'test-driven development',
    'writing plans',
    'brainstorming',
  ],
  'development': [
    'code review',
    'codebase exploration',
    'development best practices',
    'refactoring',
  ],
  'ai_ops': [
    'AI automation',
    'intent classification',
    'prompt engineering',
    'LLM optimization',
  ],
  'monetization': [
    'pricing',
    'billing',
    'subscription',
    'usage metering',
    'revenue optimization',
  ],
  'customer_success': [
    'customer health',
    'churn prevention',
    'renewal',
    'expansion',
    'NPS',
  ],
  'revops': [
    'sales pipeline',
    'forecasting',
    'lead qualification',
    'deal velocity',
  ],
  'marketing': [
    'content strategy',
    'SEO',
    'campaigns',
    'copywriting',
    'growth marketing',
  ],
  'scientific': [
    'data analysis',
    'research',
    'visualization',
    'statistics',
    'bioinformatics',
  ],
  'anthropic_official': [
    'PDF processing',
    'document creation',
    'presentation',
    'spreadsheet',
  ],
};

// SkeneFlow tools by domain
const SKENEFLOW_TOOLS: Record<string, Array<{ name: string; required: boolean }>> = {
  'plg': [
    { name: 'lifecycle.get_segment', required: true },
    { name: 'lifecycle.record_moment', required: false },
    { name: 'analytics.track_event', required: false },
    { name: 'messaging.send_in_app', required: false },
  ],
  'monetization': [
    { name: 'stripe.get_customer', required: true },
    { name: 'stripe.list_subscriptions', required: false },
    { name: 'stripe.create_checkout', required: false },
  ],
  'customer_success': [
    { name: 'lifecycle.get_segment', required: true },
    { name: 'analytics.get_cohort', required: false },
    { name: 'crm.update_account', required: false },
  ],
  'revops': [
    { name: 'crm.get_pipeline', required: true },
    { name: 'crm.list_deals', required: false },
    { name: 'analytics.get_forecast', required: false },
  ],
  'marketing': [
    { name: 'resend.send_email', required: false },
    { name: 'analytics.track_campaign', required: false },
  ],
  'ai_ops': [
    { name: 'ai.classify', required: false },
    { name: 'ai.generate', required: false },
    { name: 'ai.score_lead', required: false },
  ],
};

/**
 * Generate Claude triggers from skill description and domain
 */
function generateClaudeTriggers(skill: LoadedSkill): string[] {
  const triggers: string[] = [];
  const domain = skill.manifest.domain;
  const name = skill.manifest.name;
  const description = skill.manifest.description;
  
  // Add domain-specific triggers
  const domainTriggers = CLAUDE_TRIGGER_PATTERNS[domain] || [];
  
  // Extract key phrases from description
  const descWords = description.toLowerCase();
  
  // Add name-based trigger
  triggers.push(`help with ${name.replace(/-/g, ' ').replace(/_/g, ' ')}`);
  
  // Add relevant domain triggers based on description match
  for (const trigger of domainTriggers) {
    if (descWords.includes(trigger.split(' ')[0])) {
      triggers.push(trigger);
    }
  }
  
  // Add "when to use" style triggers
  if (descWords.includes('use when')) {
    const useWhenMatch = description.match(/use when[^.]+/i);
    if (useWhenMatch) {
      triggers.push(useWhenMatch[0].toLowerCase().replace('use when ', ''));
    }
  }
  
  // Limit to 5 triggers max
  return [...new Set(triggers)].slice(0, 5);
}

/**
 * Get quality tier for a skill
 */
function getQualityTier(skill: LoadedSkill): QualityTier {
  const domain = skill.manifest.domain;
  
  // Check if skill has explicit source
  if (skill.manifest.source === 'external') {
    // External skills from known good sources
    if (domain === 'anthropic_official' || domain === 'cursor_rules') {
      return 'verified';
    }
  }
  
  return DOMAIN_QUALITY_TIERS[domain] || 'experimental';
}

/**
 * Get SkeneFlow tools for a skill based on domain
 */
function getSkeneFlowTools(skill: LoadedSkill): Array<{ name: string; required: boolean }> {
  const domain = skill.manifest.domain;
  
  // If skill already has tools, return them
  if (skill.manifest.platforms?.skeneflow?.tools?.length) {
    return skill.manifest.platforms.skeneflow.tools;
  }
  
  // Get domain-specific tools
  return SKENEFLOW_TOOLS[domain] || [];
}

/**
 * Enhance a single skill manifest
 */
export function enhanceSkillManifest(skill: LoadedSkill): UnifiedSkillManifest {
  const manifest = { ...skill.manifest };
  
  // Ensure platforms object exists
  if (!manifest.platforms) {
    manifest.platforms = {};
  }
  
  // Add Claude platform config
  if (!manifest.platforms.claude) {
    manifest.platforms.claude = {};
  }
  
  // Generate and add triggers
  const triggers = generateClaudeTriggers(skill);
  if (triggers.length > 0) {
    manifest.platforms.claude.triggers = triggers;
  }
  
  // Add Cursor platform config with globs (if not present)
  if (!manifest.platforms.cursor) {
    manifest.platforms.cursor = {};
  }
  
  // Add SkeneFlow platform config
  if (!manifest.platforms.skeneflow) {
    manifest.platforms.skeneflow = {};
  }
  
  // Add tools
  const tools = getSkeneFlowTools(skill);
  if (tools.length > 0) {
    manifest.platforms.skeneflow.tools = tools;
  }
  
  // Add quality tier to tags
  const tier = getQualityTier(skill);
  const currentTags = manifest.tags || [];
  
  // Remove existing tier tags
  const filteredTags = currentTags.filter(t => !['verified', 'community', 'experimental'].includes(t));
  
  // Add tier tag
  manifest.tags = [...filteredTags, tier];
  
  return manifest;
}

/**
 * Enhance all skills and write back to disk
 */
export async function enhanceAllSkills(libraryPath: string): Promise<{
  enhanced: number;
  withTriggers: number;
  withTools: number;
  byTier: Record<QualityTier, number>;
}> {
  const skills = await loadAllSkills(libraryPath);
  
  let enhanced = 0;
  let withTriggers = 0;
  let withTools = 0;
  const byTier: Record<QualityTier, number> = {
    verified: 0,
    community: 0,
    experimental: 0,
  };
  
  for (const skill of skills) {
    try {
      const enhancedManifest = enhanceSkillManifest(skill);
      
      // Write back to disk
      const manifestPath = join(skill.sourcePath, 'skill.json');
      await writeFile(manifestPath, JSON.stringify(enhancedManifest, null, 2) + '\n');
      
      enhanced++;
      
      // Count stats
      if (enhancedManifest.platforms?.claude?.triggers?.length) {
        withTriggers++;
      }
      if (enhancedManifest.platforms?.skeneflow?.tools?.length) {
        withTools++;
      }
      
      // Count tiers
      const tier = enhancedManifest.tags?.find(t => 
        ['verified', 'community', 'experimental'].includes(t)
      ) as QualityTier | undefined;
      
      if (tier) {
        byTier[tier]++;
      }
    } catch (error) {
      console.error(`Failed to enhance ${skill.manifest.id}:`, error);
    }
  }
  
  return { enhanced, withTriggers, withTools, byTier };
}

// CLI handler
if (process.argv[1]?.endsWith('enhancer.ts')) {
  const libraryPath = process.argv[2] || './skills-library';
  
  console.log('\n🔧 Enhancing skills with Claude triggers, SkeneFlow tools, and quality tiers...\n');
  
  enhanceAllSkills(libraryPath).then(result => {
    console.log('✅ Enhancement complete!\n');
    console.log(`  Total enhanced: ${result.enhanced}`);
    console.log(`  With Claude triggers: ${result.withTriggers}`);
    console.log(`  With SkeneFlow tools: ${result.withTools}`);
    console.log('\n  Quality Tiers:');
    console.log(`    Verified: ${result.byTier.verified}`);
    console.log(`    Community: ${result.byTier.community}`);
    console.log(`    Experimental: ${result.byTier.experimental}`);
  }).catch(error => {
    console.error('Error:', error);
    process.exit(1);
  });
}
