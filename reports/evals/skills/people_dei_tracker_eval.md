# Evaluation Report: people_dei_tracker

**Session**: batch_eval
**Generated**: 2026-02-11 22:18:32

## Summary

- **Success Rate**: 100.0% (3/3)
- **Validation Pass Rate**: 100.0%
- **Auto-Act Rate**: 66.7%
- **Total Executions**: 3

## Performance Metrics

| Metric | Value |
|--------|-------|
| Average Latency | 442.14ms |
| P50 Latency | 0.95ms |
| P95 Latency | 1325.05ms |
| P99 Latency | 1325.05ms |
| Max Latency | 1325.05ms |
| Min Latency | 0.43ms |

## Decision Breakdown

| Decision Type | Count | Percentage |
|--------------|-------|------------|
| Auto Act | 2 | 66.7% |
| Flag For Review | 1 | 33.3% |

## Recommendations

- 📊 Low auto-act rate - consider improving confidence scoring
- ⚡ High P95 latency - investigate performance bottlenecks
- ✅ Excellent performance - skill is production-ready
