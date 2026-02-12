# Evaluation Report: prodops_feature_adoption

**Session**: batch_eval
**Generated**: 2026-02-12 00:05:02

## Summary

- **Success Rate**: 0.0% (0/3)
- **Validation Pass Rate**: 0.0%
- **Auto-Act Rate**: 66.7%
- **Total Executions**: 3

## Performance Metrics

| Metric | Value |
|--------|-------|
| Average Latency | 32.76ms |
| P50 Latency | 0.38ms |
| P95 Latency | 97.66ms |
| P99 Latency | 97.66ms |
| Max Latency | 97.66ms |
| Min Latency | 0.24ms |

## Decision Breakdown

| Decision Type | Count | Percentage |
|--------------|-------|------------|
| Auto Act | 2 | 66.7% |
| Flag For Review | 1 | 33.3% |

## Recommendations

- ⚠️ Success rate below 95% - investigate failure causes
- ⚠️ Validation pass rate below 98% - review input/output schemas
- 📊 Low auto-act rate - consider improving confidence scoring
