# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Evaluation session management for batch evaluations.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

from .validator import SkillValidator, ValidationResult
from .tracer import SkillTracer, SpanContext
from .metrics_collector import MetricsCollector, AggregatedMetrics


@dataclass
class EvalConfig:
    """Configuration for an evaluation session."""

    session_id: str
    session_name: str
    skills_to_eval: List[str]  # Skill IDs
    test_data_paths: Dict[str, str]  # skill_id -> test data file path
    output_dir: Path
    tracing_enabled: bool = True
    validation_enabled: bool = True
    metrics_enabled: bool = True
    trace_provider: str = 'console'  # 'console', 'otlp', 'none'
    otlp_endpoint: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EvalConfig':
        """Create from dictionary."""
        return cls(
            session_id=data['session_id'],
            session_name=data['session_name'],
            skills_to_eval=data['skills_to_eval'],
            test_data_paths=data.get('test_data_paths', {}),
            output_dir=Path(data['output_dir']),
            tracing_enabled=data.get('tracing_enabled', True),
            validation_enabled=data.get('validation_enabled', True),
            metrics_enabled=data.get('metrics_enabled', True),
            trace_provider=data.get('trace_provider', 'console'),
            otlp_endpoint=data.get('otlp_endpoint'),
        )


@dataclass
class EvalSessionResult:
    """Results from an evaluation session."""

    session_id: str
    session_name: str
    start_time: datetime
    end_time: datetime
    skills_evaluated: List[str]
    metrics: Dict[str, AggregatedMetrics]
    validation_results: Dict[str, List[ValidationResult]]
    traces: List[SpanContext]
    summary: Dict[str, Any]

    def duration_seconds(self) -> float:
        """Calculate session duration in seconds."""
        return (self.end_time - self.start_time).total_seconds()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'session_id': self.session_id,
            'session_name': self.session_name,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'duration_seconds': self.duration_seconds(),
            'skills_evaluated': self.skills_evaluated,
            'metrics': {
                skill_id: metrics.to_dict()
                for skill_id, metrics in self.metrics.items()
            },
            'summary': self.summary,
        }


class EvalSession:
    """
    Manages an evaluation session with integrated validation, tracing, and metrics.

    Provides a unified interface for running evaluations across multiple skills.
    """

    def __init__(
        self,
        config: EvalConfig,
        validator: Optional[SkillValidator] = None,
        tracer: Optional[SkillTracer] = None,
        metrics_collector: Optional[MetricsCollector] = None
    ):
        """
        Initialize evaluation session.

        Args:
            config: Session configuration
            validator: Optional custom validator
            tracer: Optional custom tracer
            metrics_collector: Optional custom metrics collector
        """
        self.config = config
        self.validator = validator or SkillValidator()
        self.tracer = tracer or SkillTracer(
            provider=config.trace_provider,
            endpoint=config.otlp_endpoint
        )
        self.metrics_collector = metrics_collector or MetricsCollector()

        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self._validation_results: Dict[str, List[ValidationResult]] = {}

    def start(self):
        """Start the evaluation session."""
        self.start_time = datetime.now()
        print(f"\n{'='*60}")
        print(f"Starting Eval Session: {self.config.session_name}")
        print(f"Session ID: {self.config.session_id}")
        print(f"Skills to evaluate: {len(self.config.skills_to_eval)}")
        print(f"{'='*60}\n")

    def end(self) -> EvalSessionResult:
        """
        End the evaluation session and return results.

        Returns:
            EvalSessionResult with all collected data
        """
        self.end_time = datetime.now()

        # Collect all metrics
        metrics = self.metrics_collector.get_all_metrics()

        # Build summary
        summary = {
            'total_skills': len(self.config.skills_to_eval),
            'total_executions': sum(
                m.total_executions for m in metrics.values()
            ),
            'overall_success_rate': sum(
                m.success_rate * m.total_executions for m in metrics.values()
            ) / sum(m.total_executions for m in metrics.values()) if metrics else 0,
            'overall_validation_pass_rate': sum(
                m.validation_pass_rate * m.total_executions for m in metrics.values()
            ) / sum(m.total_executions for m in metrics.values()) if metrics else 0,
        }

        result = EvalSessionResult(
            session_id=self.config.session_id,
            session_name=self.config.session_name,
            start_time=self.start_time,
            end_time=self.end_time,
            skills_evaluated=list(metrics.keys()),
            metrics=metrics,
            validation_results=self._validation_results,
            traces=self.tracer.get_spans(),
            summary=summary
        )

        print(f"\n{'='*60}")
        print(f"Eval Session Complete: {self.config.session_name}")
        print(f"Duration: {result.duration_seconds():.2f}s")
        print(f"Skills evaluated: {len(result.skills_evaluated)}")
        print(f"Total executions: {summary['total_executions']}")
        print(f"Success rate: {summary['overall_success_rate']:.1%}")
        print(f"{'='*60}\n")

        return result

    def validate_and_record(
        self,
        skill_id: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any]
    ) -> tuple[ValidationResult, ValidationResult]:
        """
        Validate input and output, record results.

        Args:
            skill_id: Skill identifier
            input_data: Input data to validate
            output_data: Output data to validate

        Returns:
            Tuple of (input_validation_result, output_validation_result)
        """
        if not self.config.validation_enabled:
            return (
                ValidationResult(valid=True),
                ValidationResult(valid=True)
            )

        input_result = self.validator.validate_input(skill_id, input_data)
        output_result = self.validator.validate_output(skill_id, output_data)

        # Record validation results
        if skill_id not in self._validation_results:
            self._validation_results[skill_id] = []
        self._validation_results[skill_id].extend([input_result, output_result])

        return input_result, output_result

    def save_results(self, output_path: Optional[Path] = None):
        """
        Save session results to disk.

        Args:
            output_path: Optional custom output path.
                        If None, uses config.output_dir/session_id.json
        """
        if output_path is None:
            output_path = self.config.output_dir / f"{self.config.session_id}.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        result = self.end()

        with open(output_path, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)

        print(f"Results saved to: {output_path}")

        # Also save traces as separate file
        traces_path = output_path.with_suffix('.traces.json')
        with open(traces_path, 'w') as f:
            f.write(self.tracer.export_json())

        print(f"Traces saved to: {traces_path}")
