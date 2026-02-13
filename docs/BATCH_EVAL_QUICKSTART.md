# Batch Evaluation Quick Start Guide

**Status**: Phase 0 Complete ✅
**Last Updated**: February 11, 2026

---

## Overview

The batch evaluation infrastructure allows you to evaluate multiple skills at once with automatic test data generation, parallel execution, and comprehensive reporting.

**Key Features**:

- ⚡ Parallel evaluation (5-20 workers)
- 🤖 Automatic test data generation from schemas
- 📊 Aggregate reports (domain-level and session-level)
- 🔍 Failure analysis with actionable recommendations
- 🚀 Full library evaluation in ~3-4 minutes

---

## Installation

Ensure dependencies are installed:

```bash
source .venv/bin/activate
pip install -r requirements-test.txt
```

---

## Quick Start

### 1. Evaluate a Single Domain

```bash
# Evaluate all skills in ecosystem domain
python scripts/batch_eval_skills.py --domain ecosystem --parallel 5

# Output:
# ============================================================
# Batch Skill Evaluation
# ============================================================
# Discovered 16 skills across 1 domains
# [1/16] ✓ ecosystem/elg_mdf_tracker
# [2/16] ✓ ecosystem/elg_partner_tier_manager
# ...
# ============================================================
# Evaluation Complete
# ============================================================
# Total: 16, Successful: 12, Failed: 4
# Success Rate: 75.0%
```

### 2. Evaluate Multiple Domains

```bash
# Evaluate 3 business-critical domains
python scripts/batch_eval_skills.py \
  --domains ecosystem,marketing,revops \
  --parallel 10
```

### 3. Evaluate Specific Skills

```bash
# Evaluate just 2 skills
python scripts/batch_eval_skills.py \
  --skills elg_mdf_tracker,elg_partner_tier_manager
```

### 4. Analyze Failures

```bash
# After batch eval, analyze failures
python scripts/analyze_eval_failures.py \
  --session batch_20260211_171252 \
  --prioritize

# Output:
# ============================================================
# Failure Analysis Complete
# ============================================================
# Total Failures: 4
# Top Categories:
#   unknown: 4
# Action Items: 1
# Report: reports/evals/failure_analysis_batch_20260211_171252.md
```

---

## Common Workflows

### Workflow 1: Evaluate New Domain

```bash
# 1. Generate test data only (fast, no evaluation)
python scripts/batch_eval_skills.py --domain marketing --generate-only

# 2. Review generated test data
ls -lh test_cases/

# 3. Run evaluation using generated test data
python scripts/batch_eval_skills.py --domain marketing --use-existing-test-data --parallel 10

# 4. Check results
cat reports/evals/batch_*_aggregate.md

# 5. Analyze failures
python scripts/analyze_eval_failures.py --domain marketing --prioritize
```

### Workflow 2: Re-evaluate After Fixes

```bash
# After fixing schema issues, re-evaluate same domain
python scripts/batch_eval_skills.py \
  --domain ecosystem \
  --parallel 10

# Compare with previous session
diff reports/evals/batch_OLD_aggregate.md reports/evals/batch_NEW_aggregate.md
```

### Workflow 3: Full Library Sweep

```bash
# Evaluate ALL 765 skills (takes ~3-4 minutes)
python scripts/batch_eval_skills.py \
  --domains ecosystem,marketing,revops,plg,monetization,customer_success,ai_ops,product_ops,support_ops,finops,security,community,compliance,data_ops,people_ops,development,vcf,devex,superpowers,anthropic_official,cursor_rules,plg_frameworks,scientific \
  --parallel 20

# Or use a bash loop
for domain in ecosystem marketing revops plg monetization; do
  python scripts/batch_eval_skills.py --domain $domain --parallel 10
done
```

---

## Output Files

### Test Data

**Location**: `test_cases/`

**Example**: `test_cases/elg_mdf_tracker_test_data.json`

```json
{
  "skill_id": "elg_mdf_tracker",
  "generated_at": "2026-02-11T17:12:52.129965",
  "num_cases": 3,
  "test_cases": [
    {
      "inputs": {
        "partnerId": "test-abc123",
        "action": "check_budget"
      },
      "label": "valid_case_1",
      "expected_valid": true
    }
  ]
}
```

### Per-Skill Reports

**Location**: `reports/evals/skills/`

**Example**: `reports/evals/skills/elg_mdf_tracker_eval.md`

### Aggregate Reports

**Location**: `reports/evals/`

**Files**:

- `batch_{timestamp}_aggregate.md` - Human-readable summary
- `batch_{timestamp}_aggregate.json` - Machine-readable data

**Example**:

```markdown
# Batch Evaluation Report: batch_20260211_171252

## Overall Summary

- **Total Skills**: 16
- **Successful**: 12 (75.0%)
- **Failed**: 4 (25.0%)

## Domain Breakdown

| Domain    | Total | Success | Failed | Avg Success Rate | Avg Auto-Act Rate |
| --------- | ----- | ------- | ------ | ---------------- | ----------------- |
| ecosystem | 16    | 12      | 4      | 100.0%           | 90.0%             |
```

### Failure Analysis Reports

**Location**: `reports/evals/`

**Example**: `failure_analysis_batch_20260211_171252.md`

```markdown
# Evaluation Failure Analysis

## Summary Statistics

- **Total Failures**: 4

## Action Plan (Prioritized)

1. Schema Missing (Priority 5/5)
   - Fix: Add inputSchema/outputSchema to skill.json
   - Affected Skills: 4
```

---

## Advanced Options

### Parallel Workers

```bash
# More workers = faster, but higher CPU usage
python scripts/batch_eval_skills.py --domain ecosystem --parallel 20
```

**Recommendation**: Use 5-10 workers on laptop, 20+ on server.

### Use Existing Test Data

```bash
# Faster (skips test data generation)
python scripts/batch_eval_skills.py --domain ecosystem --use-existing-test-data
```

**Use Case**: Re-running evaluation after code changes (not schema changes).

### Verbose Output

```bash
# Show detailed progress
python scripts/batch_eval_skills.py --domain ecosystem --verbose
```

**Output**:

```
[1/16] ✓ ecosystem/elg_mdf_tracker
    Success: 100.0%, Auto-act: 33.3%
```

### Custom Directories

```bash
# Use custom paths
python scripts/batch_eval_skills.py \
  --domain ecosystem \
  --test-data-dir /tmp/test_cases \
  --report-dir /tmp/reports
```

---

## Troubleshooting

### Issue: "Skill not found"

**Cause**: Skill ID doesn't match directory structure.

**Fix**: Check skill ID in `skill.json` matches directory name.

```bash
# Find skill directories
find skills-library/ecosystem -name "skill.json" -exec jq -r '.id' {} \;
```

### Issue: "No test cases generated"

**Cause**: Skill missing `inputSchema` in `skill.json`.

**Fix**: Add `inputSchema` field:

```json
{
  "id": "my_skill",
  "inputSchema": {
    "type": "object",
    "properties": {
      "action": { "type": "string" }
    },
    "required": ["action"]
  }
}
```

### Issue: "No metrics collected"

**Cause**: Validation failed (often due to empty inputs).

**Fix**: Ensure schema has at least one required field, or adjust confidence thresholds.

### Issue: Slow evaluation

**Cause**: Too many workers or CPU-bound.

**Fix**: Reduce `--parallel` workers:

```bash
python scripts/batch_eval_skills.py --domain ecosystem --parallel 3
```

---

## Performance Tips

### 1. Generate Test Data Once

```bash
# Generate test data upfront
python scripts/batch_eval_skills.py --domains ecosystem,marketing,revops --generate-only

# Then run multiple evaluations using cached data
python scripts/batch_eval_skills.py --domain ecosystem --use-existing-test-data
```

### 2. Evaluate in Batches

```bash
# Small batches are easier to debug
python scripts/batch_eval_skills.py --domain ecosystem
python scripts/batch_eval_skills.py --domain marketing
python scripts/batch_eval_skills.py --domain revops
```

### 3. Parallel Execution

```bash
# Run multiple domains in parallel (separate terminals)
python scripts/batch_eval_skills.py --domain ecosystem &
python scripts/batch_eval_skills.py --domain marketing &
python scripts/batch_eval_skills.py --domain revops &
wait
```

---

## Integration with Existing Tools

### With Single Skill Eval

```bash
# Use single-skill eval for detailed debugging
python scripts/run_eval_harness.py eval-skill --skill-id elg_mdf_tracker

# Then batch eval for regression testing
python scripts/batch_eval_skills.py --domain ecosystem
```

### With loom CLI

(Coming soon: `loom eval batch --domain ecosystem`)

### With CI/CD

```bash
# GitHub Actions example
name: Eval Harness
on: [pull_request]
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: pip install -r requirements-test.txt
      - run: python scripts/batch_eval_skills.py --domain ecosystem
```

---

## FAQ

**Q: How long does full library evaluation take?**
A: ~3-4 minutes with 20 parallel workers (765 skills @ 0.5 sec/skill).

**Q: Can I evaluate skills without implementations?**
A: Yes! The eval harness validates schemas and generates test data without requiring actual skill logic.

**Q: What if my skill has no required fields?**
A: The generator will create empty inputs `{}`. Consider adding at least one required field for better validation.

**Q: How do I export failures to CSV?**
A: Use `--export` flag:

```bash
python scripts/analyze_eval_failures.py --session batch_20260211_171252 --export failures.csv
```

**Q: Can I run this in CI/CD?**
A: Yes! See "Integration with Existing Tools" section above.

**Q: What's the difference between batch eval and single eval?**
A:

- **Single eval** (`run_eval_harness.py`): Deep dive on one skill with tracing
- **Batch eval** (`batch_eval_skills.py`): Fast validation of many skills

---

## Next Steps

1. **Run Phase 1 Pilot** (5 domains, 50 skills):

   ```bash
   python scripts/batch_eval_skills.py \
     --domains customer_success,ai_ops,product_ops,support_ops,finops \
     --parallel 10
   ```

2. **Fix schema gaps** identified in failures

3. **Tune confidence thresholds** for better auto-act rates

4. **Roll out to all 765 skills** in ~10 weeks

---

## Resources

- **Phase 0 Completion Report**: [docs/internal/EVAL_HARNESS_PHASE_0_COMPLETE.md](internal/EVAL_HARNESS_PHASE_0_COMPLETE.md) (maintainers)
- **Original Rollout Plan**: Check project documentation
- **Eval Harness README**: `eval_harness/README.md`
- **Skills Catalog**: `skills-library/SKILLS_CATALOG.md`

---

**Questions or issues?** Open an issue or check the troubleshooting guide.
