# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Decision engine for determining auto-execute vs require-approval.

Combines confidence scoring, risk assessment, and validation status to make
intelligent decisions about skill execution.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class DecisionType(Enum):
    """Types of execution decisions."""

    AUTO_ACT = "auto_act"  # Execute automatically
    FLAG_FOR_REVIEW = "flag_for_review"  # Execute but notify human
    REQUIRE_APPROVAL = "require_approval"  # Block until human approves
    BLOCK = "block"  # Reject execution


@dataclass
class Decision:
    """Decision result with reasoning."""

    type: DecisionType
    confidence: float  # 0.0 to 1.0
    risk_level: str  # Low, Medium, High, Critical
    validation_passed: bool
    reasoning: str
    metadata: Dict[str, Any]

    def should_execute(self) -> bool:
        """Whether execution should proceed automatically."""
        return self.type in [DecisionType.AUTO_ACT, DecisionType.FLAG_FOR_REVIEW]

    def requires_human_approval(self) -> bool:
        """Whether human approval is required before execution."""
        return self.type == DecisionType.REQUIRE_APPROVAL

    def is_blocked(self) -> bool:
        """Whether execution is blocked."""
        return self.type == DecisionType.BLOCK


@dataclass
class DecisionConfig:
    """Configuration for decision engine."""

    # Confidence thresholds
    auto_act_threshold: float = 0.85  # >= this -> auto_act (if other conditions met)
    flag_threshold: float = 0.50  # >= this -> flag_for_review
    block_threshold: float = 0.30  # < this -> block

    # Risk level overrides
    critical_risk_requires_approval: bool = True
    high_risk_min_confidence: float = 0.75

    # Validation requirements
    block_on_validation_failure: bool = True

    # Execution history weight
    use_execution_history: bool = True
    min_executions_for_history: int = 5
    history_success_rate_threshold: float = 0.90


class DecisionEngine:
    """
    Multi-factor decision engine for skill execution.

    Determines whether to:
    - AUTO_ACT: Execute automatically (high confidence, acceptable risk)
    - FLAG_FOR_REVIEW: Execute but notify human (medium confidence)
    - REQUIRE_APPROVAL: Block until human approves (low confidence or high risk)
    - BLOCK: Reject execution (validation failed or very low confidence)
    """

    def __init__(self, config: Optional[DecisionConfig] = None):
        """
        Initialize decision engine.

        Args:
            config: Optional custom configuration
        """
        self.config = config or DecisionConfig()
        self._execution_history: Dict[str, Dict[str, Any]] = {}

    def make_decision(
        self,
        skill_id: str,
        confidence: float,
        risk_level: str,
        validation_passed: bool,
        execution_history: Optional[Dict[str, Any]] = None,
    ) -> Decision:
        """
        Make execution decision based on multiple factors.

        Args:
            skill_id: Skill identifier
            confidence: Confidence score (0.0 to 1.0)
            risk_level: Security risk level (Low, Medium, High, Critical)
            validation_passed: Whether I/O validation passed
            execution_history: Optional execution history stats

        Returns:
            Decision with type and reasoning
        """
        metadata = {
            "skill_id": skill_id,
            "confidence": confidence,
            "risk_level": risk_level,
            "validation_passed": validation_passed,
        }

        # Rule 1: Validation failure -> BLOCK
        if self.config.block_on_validation_failure and not validation_passed:
            return Decision(
                type=DecisionType.BLOCK,
                confidence=confidence,
                risk_level=risk_level,
                validation_passed=validation_passed,
                reasoning="Blocked: I/O validation failed",
                metadata=metadata,
            )

        # Rule 2: Critical risk -> REQUIRE_APPROVAL
        if risk_level == "Critical" and self.config.critical_risk_requires_approval:
            return Decision(
                type=DecisionType.REQUIRE_APPROVAL,
                confidence=confidence,
                risk_level=risk_level,
                validation_passed=validation_passed,
                reasoning="Requires approval: Critical risk level",
                metadata=metadata,
            )

        # Rule 3: Very low confidence -> BLOCK
        if confidence < self.config.block_threshold:
            return Decision(
                type=DecisionType.BLOCK,
                confidence=confidence,
                risk_level=risk_level,
                validation_passed=validation_passed,
                reasoning=f"Blocked: Confidence too low ({confidence:.2f} < {self.config.block_threshold})",
                metadata=metadata,
            )

        # Rule 4: High risk requires higher confidence
        if risk_level == "High" and confidence < self.config.high_risk_min_confidence:
            return Decision(
                type=DecisionType.FLAG_FOR_REVIEW,
                confidence=confidence,
                risk_level=risk_level,
                validation_passed=validation_passed,
                reasoning=f"Flagged: High risk requires confidence >= {self.config.high_risk_min_confidence}",
                metadata=metadata,
            )

        # Rule 5: Check execution history (if available)
        if execution_history and self.config.use_execution_history:
            total_execs = execution_history.get("total_executions", 0)
            success_rate = execution_history.get("success_rate", 0.0)

            if total_execs >= self.config.min_executions_for_history:
                if success_rate < self.config.history_success_rate_threshold:
                    return Decision(
                        type=DecisionType.FLAG_FOR_REVIEW,
                        confidence=confidence,
                        risk_level=risk_level,
                        validation_passed=validation_passed,
                        reasoning=f"Flagged: Low historical success rate ({success_rate:.1%})",
                        metadata={**metadata, "history": execution_history},
                    )

        # Rule 6: High confidence -> AUTO_ACT
        if confidence >= self.config.auto_act_threshold:
            return Decision(
                type=DecisionType.AUTO_ACT,
                confidence=confidence,
                risk_level=risk_level,
                validation_passed=validation_passed,
                reasoning=f"Auto-executing: High confidence ({confidence:.2f}), acceptable risk",
                metadata=metadata,
            )

        # Rule 7: Medium confidence -> FLAG_FOR_REVIEW
        if confidence >= self.config.flag_threshold:
            return Decision(
                type=DecisionType.FLAG_FOR_REVIEW,
                confidence=confidence,
                risk_level=risk_level,
                validation_passed=validation_passed,
                reasoning=f"Flagged: Medium confidence ({confidence:.2f})",
                metadata=metadata,
            )

        # Rule 8: Low confidence -> REQUIRE_APPROVAL
        return Decision(
            type=DecisionType.REQUIRE_APPROVAL,
            confidence=confidence,
            risk_level=risk_level,
            validation_passed=validation_passed,
            reasoning=f"Requires approval: Low confidence ({confidence:.2f})",
            metadata=metadata,
        )

    def record_execution_outcome(self, skill_id: str, success: bool, confidence: float):
        """
        Record execution outcome for history tracking.

        Args:
            skill_id: Skill identifier
            success: Whether execution succeeded
            confidence: Confidence score used
        """
        if skill_id not in self._execution_history:
            self._execution_history[skill_id] = {
                "total_executions": 0,
                "successful_executions": 0,
                "success_rate": 0.0,
            }

        history = self._execution_history[skill_id]
        history["total_executions"] += 1
        if success:
            history["successful_executions"] += 1
        history["success_rate"] = history["successful_executions"] / history["total_executions"]

    def get_execution_history(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """
        Get execution history for a skill.

        Args:
            skill_id: Skill identifier

        Returns:
            Execution history or None
        """
        return self._execution_history.get(skill_id)
