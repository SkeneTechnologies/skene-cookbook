# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
JSON report generation for evaluation results.

Machine-readable format for programmatic analysis.
"""

import json
from pathlib import Path
from typing import Optional

from ..core.metrics_collector import AggregatedMetrics
from ..core.eval_session import EvalSessionResult


class JSONReporter:
    """
    Generate JSON evaluation reports.

    Provides machine-readable exports for programmatic analysis,
    dashboards, and integration with other tools.
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
        session_id: str
    ) -> dict:
        """
        Generate JSON report for a single skill evaluation.

        Args:
            skill_id: Skill identifier
            metrics: Aggregated metrics
            session_id: Evaluation session ID

        Returns:
            Report as dictionary
        """
        return {
            'skill_id': skill_id,
            'session_id': session_id,
            'summary': metrics.to_dict(),
            'records': [
                {
                    'timestamp': record.timestamp,
                    'duration_ms': record.duration_ms,
                    'success': record.success,
                    'validation_passed': record.validation_passed,
                    'decision_type': record.decision_type,
                    'error_type': record.error_type,
                    'metadata': record.metadata
                }
                for record in metrics.records
            ]
        }

    def generate_session_report(
        self,
        session_result: EvalSessionResult
    ) -> dict:
        """
        Generate JSON report for entire evaluation session.

        Args:
            session_result: Session evaluation results

        Returns:
            Report as dictionary
        """
        return session_result.to_dict()

    def save_skill_report(
        self,
        skill_id: str,
        metrics: AggregatedMetrics,
        session_id: str
    ) -> Path:
        """
        Generate and save skill evaluation report as JSON.

        Args:
            skill_id: Skill identifier
            metrics: Aggregated metrics
            session_id: Evaluation session ID

        Returns:
            Path to saved report
        """
        report = self.generate_skill_report(skill_id, metrics, session_id)

        output_path = self.output_dir / "skills" / f"{skill_id}_eval.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        return output_path

    def save_session_report(
        self,
        session_result: EvalSessionResult
    ) -> Path:
        """
        Generate and save session evaluation report as JSON.

        Args:
            session_result: Session evaluation results

        Returns:
            Path to saved report
        """
        report = self.generate_session_report(session_result)

        output_path = (
            self.output_dir / "sessions" /
            f"{session_result.session_id}_eval.json"
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        return output_path
