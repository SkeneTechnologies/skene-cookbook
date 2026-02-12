# Evaluation Report: mon_upgrade_trigger

**Session**: batch_eval
**Generated**: 2026-02-12 00:05:12

## Summary

- **Success Rate**: 0.0% (0/3)
- **Validation Pass Rate**: 0.0%
- **Auto-Act Rate**: 100.0%
- **Total Executions**: 3

## Performance Metrics

| Metric | Value |
|--------|-------|
| Average Latency | 481.83ms |
| P50 Latency | 0.20ms |
| P95 Latency | 1445.17ms |
| P99 Latency | 1445.17ms |
| Max Latency | 1445.17ms |
| Min Latency | 0.13ms |

## Decision Breakdown

| Decision Type | Count | Percentage |
|--------------|-------|------------|
| Auto Act | 3 | 100.0% |

## Recommendations

- ⚠️ Success rate below 95% - investigate failure causes
- ⚠️ Validation pass rate below 98% - review input/output schemas
- ⚡ High P95 latency - investigate performance bottlenecks
