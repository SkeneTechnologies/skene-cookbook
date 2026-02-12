# Evaluation Report: data_privacy_scanner

**Session**: batch_eval
**Generated**: 2026-02-11 22:18:30

## Summary

- **Success Rate**: 100.0% (4/4)
- **Validation Pass Rate**: 100.0%
- **Auto-Act Rate**: 50.0%
- **Total Executions**: 4

## Performance Metrics

| Metric | Value |
|--------|-------|
| Average Latency | 335.06ms |
| P50 Latency | 0.09ms |
| P95 Latency | 1340.05ms |
| P99 Latency | 1340.05ms |
| Max Latency | 1340.05ms |
| Min Latency | 0.05ms |

## Decision Breakdown

| Decision Type | Count | Percentage |
|--------------|-------|------------|
| Auto Act | 2 | 50.0% |
| Flag For Review | 2 | 50.0% |

## Recommendations

- 📊 Low auto-act rate - consider improving confidence scoring
- ⚡ High P95 latency - investigate performance bottlenecks
- ✅ Excellent performance - skill is production-ready
