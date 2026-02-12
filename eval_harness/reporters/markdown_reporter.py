# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Markdown report generation for evaluation results.

Compatible with existing skene-cookbook report format.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ..core.eval_session import EvalSessionResult
from ..core.metrics_collector import AggregatedMetrics


class MarkdownReporter:
    """
    Generate Markdown evaluation reports.

    Compatible with existing skene-cookbook report format.
    """

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize reporter.

        Args:
            output_dir: Output directory for reports
        """
        self.output_dir = output_dir or Path("reports/evals")

    def generate_skill_report(
        self,
        skill_id: str,
        metrics: AggregatedMetrics,
        session_id: str,
        chain_compatibility: Optional[Dict[str, List[str]]] = None,
    ) -> str:
        """
        Generate Markdown report for a single skill evaluation.

        Args:
            skill_id: Skill identifier
            metrics: Aggregated metrics
            session_id: Evaluation session ID
            chain_compatibility: Optional chain compatibility information

        Returns:
            Markdown report as string
        """
        report = f"""# Evaluation Report: {skill_id}

**Session**: {session_id}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Success Rate**: {metrics.success_rate:.1%} ({sum(1 for r in metrics.records if r.success)}/{metrics.total_executions})
- **Validation Pass Rate**: {metrics.validation_pass_rate:.1%}
- **Auto-Act Rate**: {metrics.auto_act_rate:.1%}
- **Total Executions**: {metrics.total_executions}

## Performance Metrics

| Metric | Value |
|--------|-------|
| Average Latency | {metrics.avg_duration_ms:.2f}ms |
| P50 Latency | {metrics.p50_duration_ms:.2f}ms |
| P95 Latency | {metrics.p95_duration_ms:.2f}ms |
| P99 Latency | {metrics.p99_duration_ms:.2f}ms |
| Max Latency | {metrics.max_duration_ms:.2f}ms |
| Min Latency | {metrics.min_duration_ms:.2f}ms |

## Decision Breakdown

| Decision Type | Count | Percentage |
|--------------|-------|------------|
"""

        # Add decision breakdown rows
        total_decisions = sum(metrics.decision_counts.values())
        for decision_type, count in sorted(metrics.decision_counts.items()):
            percentage = (count / total_decisions * 100) if total_decisions > 0 else 0
            report += (
                f"| {decision_type.replace('_', ' ').title()} | {count} | {percentage:.1f}% |\n"
            )

        # Add errors section if there are errors
        if metrics.error_type_counts:
            report += "\n## Errors\n\n"
            report += "| Error Type | Count |\n"
            report += "|-----------|-------|\n"

            for error_type, count in sorted(
                metrics.error_type_counts.items(), key=lambda x: x[1], reverse=True
            ):
                report += f"| {error_type} | {count} |\n"

        # Add chain compatibility section if provided
        if chain_compatibility:
            report += "\n## Chain Compatibility\n\n"

            if "compatible" in chain_compatibility:
                report += "### Compatible Skills\n\n"
                for skill in chain_compatibility["compatible"]:
                    report += f"- ✅ {skill}\n"

            if "warnings" in chain_compatibility:
                report += "\n### Compatibility Warnings\n\n"
                for skill, warnings in chain_compatibility["warnings"].items():
                    report += f"- ⚠️ **{skill}**\n"
                    for warning in warnings:
                        report += f"  - {warning}\n"

            if "incompatible" in chain_compatibility:
                report += "\n### Incompatible Skills\n\n"
                for skill in chain_compatibility["incompatible"]:
                    report += f"- ❌ {skill}\n"

        # Add recommendations
        report += "\n## Recommendations\n\n"

        if metrics.success_rate < 0.95:
            report += "- ⚠️ Success rate below 95% - investigate failure causes\n"

        if metrics.validation_pass_rate < 0.98:
            report += "- ⚠️ Validation pass rate below 98% - review input/output schemas\n"

        if metrics.auto_act_rate < 0.70:
            report += "- 📊 Low auto-act rate - consider improving confidence scoring\n"

        if metrics.p95_duration_ms > 1000:
            report += "- ⚡ High P95 latency - investigate performance bottlenecks\n"

        if not metrics.error_type_counts and metrics.success_rate > 0.95:
            report += "- ✅ Excellent performance - skill is production-ready\n"

        return report

    def generate_session_report(self, session_result: EvalSessionResult) -> str:
        """
        Generate Markdown report for entire evaluation session.

        Args:
            session_result: Session evaluation results

        Returns:
            Markdown report as string
        """
        report = f"""# Evaluation Session Report: {session_result.session_name}

**Session ID**: {session_result.session_id}
**Duration**: {session_result.duration_seconds():.2f}s
**Start Time**: {session_result.start_time.strftime('%Y-%m-%d %H:%M:%S')}
**End Time**: {session_result.end_time.strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Skills Evaluated**: {len(session_result.skills_evaluated)}
- **Total Executions**: {session_result.summary['total_executions']}
- **Overall Success Rate**: {session_result.summary['overall_success_rate']:.1%}
- **Overall Validation Pass Rate**: {session_result.summary['overall_validation_pass_rate']:.1%}

## Skills Performance

| Skill ID | Executions | Success Rate | Avg Latency |
|----------|-----------|--------------|-------------|
"""

        # Add skill rows
        for skill_id in sorted(session_result.skills_evaluated):
            metrics = session_result.metrics.get(skill_id)
            if metrics:
                report += (
                    f"| {skill_id} | {metrics.total_executions} | "
                    f"{metrics.success_rate:.1%} | {metrics.avg_duration_ms:.2f}ms |\n"
                )

        return report

    def save_skill_report(
        self,
        skill_id: str,
        metrics: AggregatedMetrics,
        session_id: str,
        chain_compatibility: Optional[Dict[str, List[str]]] = None,
    ) -> Path:
        """
        Generate and save skill evaluation report.

        Args:
            skill_id: Skill identifier
            metrics: Aggregated metrics
            session_id: Evaluation session ID
            chain_compatibility: Optional chain compatibility information

        Returns:
            Path to saved report
        """
        report = self.generate_skill_report(skill_id, metrics, session_id, chain_compatibility)

        output_path = self.output_dir / "skills" / f"{skill_id}_eval.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(report)

        return output_path

    def save_session_report(self, session_result: EvalSessionResult) -> Path:
        """
        Generate and save session evaluation report.

        Args:
            session_result: Session evaluation results

        Returns:
            Path to saved report
        """
        report = self.generate_session_report(session_result)

        output_path = self.output_dir / "sessions" / f"{session_result.session_id}_eval.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(report)

        return output_path
