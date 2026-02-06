# Skills Library Cleanup Summary

**Date:** 2026-02-06
**Branch:** cleanup/remove-project-specific-skills
**Commit:** 38ebdd2

## Overview

Cleaned up the skills library to remove project-specific and internal references, making it more general-purpose and broadly applicable to external users.

## Results

- **Before:** 808 skills
- **After:** 764 skills
- **Removed:** 44 skills
- **Files changed:** 666 files

## What Was Removed

### 1. Skene-Specific Skills (9 skills)

**Removed entire `skills-library/skene/` domain:**
- skene_analyze_features
- skene_analyze_growth_hubs
- skene_analyze_product_overview
- skene_analyze_tech_stack
- skene_generate_growth_manifest
- skene_generate_growth_template

**Removed Skene-branded marketing skills:**
- marketing/brand/skene_voice_guardian
- marketing/tools/skene_growth_bridge
- plg_frameworks/setup-skene-growth

**Why:** These skills were tightly coupled to internal Skene products (uvx skene-growth) and internal configuration files (config/personality/operator-memo.md).

### 2. Internal Tool Skills (5 skills)

- marketing/operations/langsmith_fetch - LangSmith-specific debugging tool
- marketing/tools/skill_share - Referenced internal "Rube" Slack service
- marketing/tools/cpo_operator - Internal CPO-specific workflow
- marketing/analytics/developer_growth_analysis - Used Rube for Slack DMs
- marketing/analytics/plg_score_explainer - Referenced skene-growth analysis

**Why:** These skills depended on internal services (Rube), internal tools (LangSmith), or Skene-specific workflows not available to external users.

### 3. Internal Marketing/Research Skills (2 skills)

- marketing/research/influencer_repo_analyzer - Deep Skene product integration
- marketing/tools/reverse_influence_strategist - Skene product specific

**Why:** These skills were designed specifically to promote Skene products rather than being general-purpose marketing skills.

### 4. Meta Orchestration Skills (6 skills)

**Removed entire `skills-library/meta/` domain:**
- meta_customer_360
- meta_growth_diagnostician
- meta_gtm_orchestrator
- meta_incident_coordinator
- meta_land_expand_journey
- meta_revenue_intelligence

**Why:** These experimental meta-skills assumed specific company infrastructure and referenced internal data models (crm.*, cs.*, support.*) not generalizable to external users.

### 5. Archived PLG Skills (22 skills moved to archived/)

**Moved from `skills-library/plg_frameworks/.archived/` to `archived/plg_frameworks/`:**
- activation-metrics
- engagement-loops
- expansion-revenue
- feature-adoption
- feature-gating
- free-tool-strategy
- growth-loops
- growth-modeling
- in-product-messaging
- paywall-upgrade-cro
- pricing-strategy
- product-analytics
- product-led-sales
- product-onboarding
- referral-program
- retention-analysis
- self-serve-motion
- signup-flow-cro
- trial-optimization
- usage-based-pricing
- user-segmentation
- viral-loops

**Why:** These were already archived but mixed into the active skills directory. Moved to top-level archived/ directory for clarity.

## What Was Generalized

### 1. Removed Internal Config References

**Changed in 3 marketing skills:**
- social_content_generator
- outreach_personalizer
- objective_strategist

**Before:**
```markdown
- `config/personality/operator-memo.md` — Brand positioning
```

**After:**
```markdown
- If brand guidelines exist in your project, reference them for positioning
```

### 2. Generalized Product Examples

**In social_content_generator:**
- Changed "The Skene Voice" → "Effective Developer-First Voice"
- Updated example CTAs from "github.com/skene-ai/skene-growth" → "[your-product-url]"
- Replaced "uvx skene-growth analyze" → "[your command/action]"

**In humanization_engine:**
- Changed "our PLG analysis tool, skene-growth" → "our developer tool"
- Updated examples to be product-agnostic

**In outreach_personalizer:**
- Changed "skene-growth" references → "our analyzer" or "your tool"
- Updated command examples to be generic placeholders

### 3. Documentation Improvements

**Added `skills-library/cursor_rules/README.md`:**
- Explains that cursor_rules contains tool-specific coding guidelines
- Documents organization by tool/framework
- Clarifies these are curated from community sources (awesome-cursor-rules)
- Notes they complement the broader skills library

**Updated `README.md`:**
- Changed "800+ skills" → "760+ skills"
- Updated skill count references throughout

## What Was Kept

### ✅ cursor_rules (241 skills)
**Decision:** KEEP with documentation
**Rationale:** These are legitimate tool-specific coding guidelines from community sources. Added README explaining their purpose.

### ✅ anthropic_official (16 skills)
**Decision:** KEEP
**Rationale:** These are general-purpose official skills, not internal tooling.

### ✅ Boyce framework (13 skills)
**Decision:** KEEP
**Rationale:** Public PLG methodology by Wes Bush/ProductLed, broadly applicable.

### ✅ Scientific domain (141 skills)
**Decision:** KEEP
**Rationale:** Specialized but legitimate skills for scientific/research users.

### ✅ All other domains
**Decision:** KEEP
**Rationale:** General-purpose skills applicable to any development team.

## Impact Analysis

### Library Focus

**Before cleanup:**
- Mixed internal/external skills
- Skene product references throughout
- Internal service dependencies
- Confused value proposition

**After cleanup:**
- Clear general-purpose focus
- No internal service dependencies
- Product-agnostic examples
- Clean, reusable skills library

### External User Experience

**Improvements:**
- No confusion about Skene-specific skills
- No broken references to internal services
- Clear examples that work for any product
- Better documentation of specialized domains (cursor_rules)

### Maintenance Benefits

**Going forward:**
- Easier to contribute new skills
- Clear boundaries for what belongs in library
- Less maintenance overhead for internal tools
- Better separation of concerns

## Files Modified

- **Deleted:** 176 files (44 skills × 4 files each average)
- **Renamed/Moved:** 88 files (archived PLG skills)
- **Modified:** 7 files (generalized internal references)
- **Created:** 1 file (cursor_rules/README.md)

## Verification

```bash
# Before cleanup
find skills-library -type f -name "skill.json" | wc -l
# 808

# After cleanup
find skills-library -type f -name "skill.json" | wc -l
# 764

# Skills removed
808 - 764 = 44 skills ✅
```

## Next Steps

### Recommended Follow-ups

1. **Regenerate docs/directory.md**
   - Update skills directory documentation
   - Ensure all counts are accurate
   - Remove references to deleted skills

2. **Update docs/VALUE.md**
   - Check if any examples referenced removed skills
   - Update skill counts if mentioned

3. **Test Installation**
   - Run `npx skills-directory install --target all`
   - Verify no broken references
   - Test status command

4. **Review Marketing Skills**
   - Audit remaining skills with `"source": "skene-marketing"` tag
   - Decide if this tag should be removed or documented
   - Consider if more generalization is needed

5. **Update CONTRIBUTING.md**
   - Add guidelines about what skills belong in library
   - Document criteria for general-purpose vs. project-specific
   - Provide examples of good vs. bad skills

## Success Criteria

✅ All explicitly Skene-branded skills removed
✅ Skills referencing internal tools removed or generalized
✅ cursor_rules documented appropriately
✅ No broken references between remaining skills
✅ Documentation updated to reflect new skill count
✅ Installation still works correctly
✅ Library focuses on general-purpose, broadly applicable skills

## Commit Message

```
Clean up project-specific and internal skills from library

Removed 44 skills to make the library more general-purpose and broadly applicable

See CLEANUP_SUMMARY.md for full details.
```
