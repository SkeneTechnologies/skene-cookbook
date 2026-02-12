# Evaluation Report: mon_pricing_optimization

**Session**: batch_eval
**Generated**: 2026-02-12 00:05:11

## Summary

- **Success Rate**: 0.0% (0/3)
- **Validation Pass Rate**: 0.0%
- **Auto-Act Rate**: 66.7%
- **Total Executions**: 3

## Performance Metrics

| Metric | Value |
|--------|-------|
| Average Latency | 469.71ms |
| P50 Latency | 0.32ms |
| P95 Latency | 1408.61ms |
| P99 Latency | 1408.61ms |
| Max Latency | 1408.61ms |
| Min Latency | 0.20ms |

## Decision Breakdown

| Decision Type | Count | Percentage |
|--------------|-------|------------|
| Auto Act | 2 | 66.7% |
| Flag For Review | 1 | 33.3% |

## Recommendations

- ⚠️ Success rate below 95% - investigate failure causes
- ⚠️ Validation pass rate below 98% - review input/output schemas
- 📊 Low auto-act rate - consider improving confidence scoring
- ⚡ High P95 latency - investigate performance bottlenecks
