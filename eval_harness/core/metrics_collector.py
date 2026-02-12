# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Metrics collection and aggregation for skill executions.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from collections import defaultdict
import time


@dataclass
class ExecutionRecord:
    """Record of a single skill execution."""

    skill_id: str
    skill_version: str
    timestamp: float
    duration_ms: float
    success: bool
    validation_passed: bool
    decision_type: str  # 'auto_act', 'flag_for_review', 'require_approval', 'block'
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AggregatedMetrics:
    """Aggregated metrics for a skill."""

    skill_id: str
    total_executions: int
    success_rate: float  # 0.0 to 1.0
    validation_pass_rate: float  # 0.0 to 1.0
    auto_act_rate: float  # 0.0 to 1.0

    # Latency metrics
    avg_duration_ms: float
    p50_duration_ms: float
    p95_duration_ms: float
    p99_duration_ms: float
    max_duration_ms: float
    min_duration_ms: float

    # Decision breakdown
    decision_counts: Dict[str, int] = field(default_factory=dict)

    # Error breakdown
    error_type_counts: Dict[str, int] = field(default_factory=dict)

    # Raw records for detailed analysis
    records: List[ExecutionRecord] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'skill_id': self.skill_id,
            'total_executions': self.total_executions,
            'success_rate': round(self.success_rate, 3),
            'validation_pass_rate': round(self.validation_pass_rate, 3),
            'auto_act_rate': round(self.auto_act_rate, 3),
            'latency': {
                'avg_ms': round(self.avg_duration_ms, 2),
                'p50_ms': round(self.p50_duration_ms, 2),
                'p95_ms': round(self.p95_duration_ms, 2),
                'p99_ms': round(self.p99_duration_ms, 2),
                'max_ms': round(self.max_duration_ms, 2),
                'min_ms': round(self.min_duration_ms, 2),
            },
            'decisions': self.decision_counts,
            'errors': self.error_type_counts,
        }


class MetricsCollector:
    """
    Collects and aggregates metrics across skill executions.

    Tracks success rate, latency, validation pass rate, decision types,
    and error distributions.
    """

    def __init__(self):
        """Initialize metrics collector."""
        self._records: Dict[str, List[ExecutionRecord]] = defaultdict(list)

    def record_execution(
        self,
        skill_id: str,
        skill_version: str,
        duration_ms: float,
        success: bool,
        validation_passed: bool,
        decision_type: str,
        error_type: Optional[str] = None,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Record a skill execution.

        Args:
            skill_id: Skill identifier
            skill_version: Skill version
            duration_ms: Execution duration in milliseconds
            success: Whether execution succeeded
            validation_passed: Whether I/O validation passed
            decision_type: 'auto_act', 'flag_for_review', 'require_approval', 'block'
            error_type: Type of error if failed
            error_message: Error message if failed
            metadata: Additional metadata
        """
        record = ExecutionRecord(
            skill_id=skill_id,
            skill_version=skill_version,
            timestamp=time.time(),
            duration_ms=duration_ms,
            success=success,
            validation_passed=validation_passed,
            decision_type=decision_type,
            error_type=error_type,
            error_message=error_message,
            metadata=metadata or {}
        )

        self._records[skill_id].append(record)

    def get_aggregated_metrics(self, skill_id: str) -> Optional[AggregatedMetrics]:
        """
        Get aggregated metrics for a skill.

        Args:
            skill_id: Skill identifier

        Returns:
            AggregatedMetrics or None if no records exist
        """
        records = self._records.get(skill_id, [])
        if not records:
            return None

        total = len(records)
        successes = sum(1 for r in records if r.success)
        validations_passed = sum(1 for r in records if r.validation_passed)
        auto_acts = sum(1 for r in records if r.decision_type == 'auto_act')

        # Calculate latency percentiles
        durations = sorted([r.duration_ms for r in records])
        p50_idx = int(len(durations) * 0.50)
        p95_idx = int(len(durations) * 0.95)
        p99_idx = int(len(durations) * 0.99)

        # Decision breakdown
        decision_counts: Dict[str, int] = defaultdict(int)
        for r in records:
            decision_counts[r.decision_type] += 1

        # Error breakdown
        error_type_counts: Dict[str, int] = defaultdict(int)
        for r in records:
            if r.error_type:
                error_type_counts[r.error_type] += 1

        return AggregatedMetrics(
            skill_id=skill_id,
            total_executions=total,
            success_rate=successes / total,
            validation_pass_rate=validations_passed / total,
            auto_act_rate=auto_acts / total,
            avg_duration_ms=sum(durations) / len(durations),
            p50_duration_ms=durations[p50_idx],
            p95_duration_ms=durations[p95_idx],
            p99_duration_ms=durations[p99_idx],
            max_duration_ms=max(durations),
            min_duration_ms=min(durations),
            decision_counts=dict(decision_counts),
            error_type_counts=dict(error_type_counts),
            records=records
        )

    def get_all_metrics(self) -> Dict[str, AggregatedMetrics]:
        """
        Get aggregated metrics for all tracked skills.

        Returns:
            Dictionary mapping skill_id to AggregatedMetrics
        """
        return {
            skill_id: self.get_aggregated_metrics(skill_id)
            for skill_id in self._records.keys()
        }

    def get_records(self, skill_id: str) -> List[ExecutionRecord]:
        """
        Get all execution records for a skill.

        Args:
            skill_id: Skill identifier

        Returns:
            List of ExecutionRecords
        """
        return self._records.get(skill_id, [])

    def reset(self, skill_id: Optional[str] = None):
        """
        Reset collected metrics.

        Args:
            skill_id: If provided, only reset metrics for this skill.
                     If None, reset all metrics.
        """
        if skill_id:
            self._records.pop(skill_id, None)
        else:
            self._records.clear()

    def export_summary(self) -> Dict[str, Any]:
        """
        Export summary statistics across all skills.

        Returns:
            Summary dictionary
        """
        all_records = [
            record
            for records in self._records.values()
            for record in records
        ]

        if not all_records:
            return {
                'total_executions': 0,
                'skills_tracked': 0
            }

        total = len(all_records)
        successes = sum(1 for r in all_records if r.success)
        validations_passed = sum(1 for r in all_records if r.validation_passed)
        auto_acts = sum(1 for r in all_records if r.decision_type == 'auto_act')

        return {
            'total_executions': total,
            'skills_tracked': len(self._records),
            'overall_success_rate': round(successes / total, 3),
            'overall_validation_pass_rate': round(validations_passed / total, 3),
            'overall_auto_act_rate': round(auto_acts / total, 3),
            'avg_duration_ms': round(
                sum(r.duration_ms for r in all_records) / total, 2
            ),
        }
