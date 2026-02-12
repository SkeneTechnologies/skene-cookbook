# Phase 1 Quick Reference Guide

**Status**: ✅ Complete (85% success rate, 90/106 skills)
**Date**: February 11, 2026

---

## What Happened in Phase 1

### Domains Evaluated (6 total, 106 skills)

| Domain | Result | Command |
|--------|--------|---------|
| ✅ ecosystem (16) | 100% | `python scripts/batch_eval_skills.py --domain ecosystem --parallel 10` |
| ✅ finops (12) | 100% | `python scripts/batch_eval_skills.py --domain finops --parallel 10` |
| ✅ support_ops (12) | 100% | `python scripts/batch_eval_skills.py --domain support_ops --parallel 10` |
| 🟨 customer_success (29) | 76% | `python scripts/batch_eval_skills.py --domain customer_success --parallel 10` |
| 🟨 ai_ops (19) | 74% | `python scripts/batch_eval_skills.py --domain ai_ops --parallel 10` |
| 🟨 product_ops (18) | 78% | `python scripts/batch_eval_skills.py --domain product_ops --parallel 10` |

---

## Fixes Applied

### 1. Ecosystem Schemas (4 skills)

Added `inputSchema` and `outputSchema` to:
- `skills-library/ecosystem/co_sell_trigger/skill.json`
- `skills-library/ecosystem/eql_scoring/skill.json`
- `skills-library/ecosystem/marketplace_integration/skill.json`
- `skills-library/ecosystem/partner_mapping/skill.json`

### 2. Naming Convention (generator fix)

Updated `eval_harness/test_data_generator.py`:
- Added domain abbreviation mapping (`cs_`, `ai_`, `prodops_`, etc.)
- Handles multiple naming patterns
- Fixed 52 "skill_not_found" errors

---

## Remaining Work (16 skills)

### Skills Needing Schemas (14 total)

**Customer Success (7)**:
```bash
# These need inputSchema/outputSchema added:
skills-library/customer_success/health_scoring/skill.json
skills-library/customer_success/expansion_playbook/skill.json
skills-library/customer_success/churn_prediction/skill.json
skills-library/customer_success/nps_followup/skill.json
skills-library/customer_success/renewal_orchestration/skill.json
skills-library/customer_success/value_realization/skill.json
```

**AI Ops (5)**:
```bash
# These need inputSchema/outputSchema added:
skills-library/ai_ops/conversation_intelligence/skill.json
skills-library/ai_ops/personalization_engine/skill.json
skills-library/ai_ops/autonomous_outreach/skill.json
skills-library/ai_ops/predictive_lead_scoring/skill.json
```

**Product Ops (4)**:
```bash
# These need inputSchema/outputSchema added:
skills-library/product_ops/feedback_synthesis/skill.json
skills-library/product_ops/feature_adoption/skill.json
skills-library/product_ops/voc_aggregation/skill.json
skills-library/product_ops/roadmap_alignment/skill.json
```

### Special Cases (2)

- `customer_success/feedback_collection` - Needs investigation
- `ai_ops/prompt-engineering` - Needs investigation

---

## How to Add Missing Schemas

### Template

Use the ecosystem fixes as templates. Basic structure:

```json
{
  "id": "skill_id",
  "version": "1.0.0",
  "name": "Skill Name",
  "description": "...",
  "exitStates": [...],
  "inputSchema": {
    "type": "object",
    "properties": {
      "action": {
        "type": "string",
        "enum": ["get", "update", "list"],
        "description": "Action to perform"
      },
      "resourceId": {
        "type": "string",
        "description": "Resource identifier"
      }
    },
    "required": ["action"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "result": {
        "type": "string"
      },
      "data": {
        "type": "object"
      },
      "status": {
        "type": "string",
        "enum": ["success", "failed"]
      }
    }
  },
  "metrics": {...},
  "temperature": 0,
  ...
}
```

### Steps

1. Read skill description and tools
2. Determine input properties from tool names/description
3. Add at least one `required` field in inputSchema
4. Define output properties based on exitStates
5. Test with batch eval

### Example Commands

```bash
# After adding schemas, re-test:
python scripts/batch_eval_skills.py --domain customer_success --parallel 10

# Verify all passing:
python scripts/batch_eval_skills.py --domains customer_success,ai_ops,product_ops --parallel 10
# Target: 100% success
```

---

## Quick Commands

### Re-run Evaluations

```bash
# Single domain
python scripts/batch_eval_skills.py --domain ecosystem --parallel 10

# Multiple domains
python scripts/batch_eval_skills.py --domains ecosystem,finops,support_ops --parallel 10

# All pilot domains
python scripts/batch_eval_skills.py --domains ecosystem,finops,support_ops,customer_success,ai_ops,product_ops --parallel 10
```

### Analyze Failures

```bash
# Find latest session ID
ls -lt reports/evals/batch_*_aggregate.json | head -1

# Analyze
python scripts/analyze_eval_failures.py --session batch_YYYYMMDD_HHMMSS --prioritize
```

### View Reports

```bash
# Aggregate report
cat reports/evals/batch_*_aggregate.md | tail -50

# Failure analysis
cat reports/evals/failure_analysis_*.md | tail -100

# Individual skill
cat reports/evals/skills/elg_co_sell_trigger_eval.md
```

---

## Next Steps Options

### Option A: Complete Phase 1 (Recommended)

Fix remaining 16 skills before Phase 2:

```bash
# 1. Add schemas to 14 skills (1-2 hours)
# 2. Investigate 2 special cases (30 min)
# 3. Re-run pilot domains (5 min)
python scripts/batch_eval_skills.py --domains customer_success,ai_ops,product_ops --parallel 10
# 4. Verify 100% success rate
```

**Benefit**: Clean slate before Phase 2, validates schema addition process

### Option B: Move to Phase 2

Proceed with business-critical domains:

```bash
# Evaluate 150 skills across 4 domains
python scripts/batch_eval_skills.py --domains marketing,revops,plg,monetization --parallel 10
```

**Benefit**: Discover issues in more domains faster, can batch fix all schemas at once

---

## Phase 2 Preview

**Target**: 150 skills across 4 business-critical domains

**Commands**:
```bash
# Marketing (52 skills)
python scripts/batch_eval_skills.py --domain marketing --parallel 10

# RevOps (25 skills)
python scripts/batch_eval_skills.py --domain revops --parallel 10

# PLG (24 skills)
python scripts/batch_eval_skills.py --domain plg --parallel 10

# Monetization (20 skills)
python scripts/batch_eval_skills.py --domain monetization --parallel 10

# All Phase 2 domains at once
python scripts/batch_eval_skills.py --domains marketing,revops,plg,monetization --parallel 10
```

**Estimated Time**: 2-3 minutes for all 150 skills

**Expected Issues**: Similar schema gaps (10-20% missing schemas)

---

## Documentation

- **Phase 0 Report**: `EVAL_HARNESS_PHASE_0_COMPLETE.md`
- **Phase 1 Report**: `PHASE_1_PILOT_COMPLETE.md`
- **Quick Start Guide**: `docs/BATCH_EVAL_QUICKSTART.md`
- **Implementation Summary**: `PHASE_0_IMPLEMENTATION_SUMMARY.md`

---

## Troubleshooting

### "Skill not found" errors

Check naming pattern in `skills-library/{domain}/` directories vs skill IDs in `skill.json`.

### "No metrics collected" errors

Skill is missing `inputSchema` or `outputSchema` in `skill.json`.

### Evaluation taking too long

Reduce `--parallel` workers:
```bash
python scripts/batch_eval_skills.py --domain ecosystem --parallel 3
```

---

**Last Updated**: February 11, 2026
**Phase 1 Status**: ✅ Complete (85% success rate)
**Ready for**: Phase 2 or Phase 1 cleanup
