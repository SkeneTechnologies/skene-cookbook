# Evaluation Report: plgf_pricing_strategy

**Session**: batch_eval
**Generated**: 2026-02-11 22:14:34

## Summary

- **Success Rate**: 100.0% (3/3)
- **Validation Pass Rate**: 100.0%
- **Auto-Act Rate**: 66.7%
- **Total Executions**: 3

## Performance Metrics

| Metric | Value |
|--------|-------|
| Average Latency | 554.04ms |
| P50 Latency | 0.46ms |
| P95 Latency | 1661.57ms |
| P99 Latency | 1661.57ms |
| Max Latency | 1661.57ms |
| Min Latency | 0.09ms |

## Decision Breakdown

| Decision Type | Count | Percentage |
|--------------|-------|------------|
| Auto Act | 2 | 66.7% |
| Flag For Review | 1 | 33.3% |

## Recommendations

- 📊 Low auto-act rate - consider improving confidence scoring
- ⚡ High P95 latency - investigate performance bottlenecks
- ✅ Excellent performance - skill is production-ready
