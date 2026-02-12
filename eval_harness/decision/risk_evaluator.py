# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Risk evaluation for skill execution.

Integrates with existing security_risk_level from metadata.yaml
and provides additional runtime risk assessment.
"""

from pathlib import Path
from typing import Any, Dict, Optional


class RiskEvaluator:
    """
    Evaluate risk for skill execution.

    Combines static risk level (from metadata) with runtime risk factors
    to provide comprehensive risk assessment.
    """

    # Risk level hierarchy
    RISK_LEVELS = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}

    def __init__(self):
        """Initialize risk evaluator."""
        pass

    def evaluate_risk(
        self, static_risk_level: str, runtime_factors: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate overall risk considering static and runtime factors.

        Args:
            static_risk_level: Risk level from metadata.yaml (Low/Medium/High/Critical)
            runtime_factors: Optional runtime risk factors

        Returns:
            Risk assessment dictionary with level and details
        """
        base_risk = self.RISK_LEVELS.get(static_risk_level, 2)  # Default to Medium
        runtime_factors = runtime_factors or {}

        # Calculate runtime risk adjustment
        risk_adjustment = 0

        # Factor 1: External API calls
        if runtime_factors.get("has_external_api_calls"):
            risk_adjustment += 1

        # Factor 2: Data modification
        if runtime_factors.get("modifies_data"):
            risk_adjustment += 1

        # Factor 3: Financial operations
        if runtime_factors.get("financial_operation"):
            risk_adjustment += 2  # Financial ops are higher risk

        # Factor 4: User data access
        if runtime_factors.get("accesses_pii"):
            risk_adjustment += 1

        # Factor 5: System-level operations
        if runtime_factors.get("system_level_operation"):
            risk_adjustment += 1

        # Calculate adjusted risk level
        adjusted_risk_value = min(base_risk + risk_adjustment, 4)  # Cap at Critical

        # Map back to risk level name
        risk_level_name = None
        for name, value in self.RISK_LEVELS.items():
            if value == adjusted_risk_value:
                risk_level_name = name
                break

        return {
            "risk_level": risk_level_name or static_risk_level,
            "static_risk": static_risk_level,
            "risk_adjustment": risk_adjustment,
            "runtime_factors": runtime_factors,
            "requires_monitoring": adjusted_risk_value >= 3,  # High or Critical
            "requires_audit_logging": adjusted_risk_value >= 2,  # Medium or higher
        }

    def should_require_approval(self, risk_level: str, confidence: float) -> bool:
        """
        Determine if execution should require approval based on risk and confidence.

        Args:
            risk_level: Risk level (Low/Medium/High/Critical)
            confidence: Confidence score (0.0-1.0)

        Returns:
            True if approval should be required
        """
        risk_value = self.RISK_LEVELS.get(risk_level, 2)

        # Critical risk always requires approval
        if risk_value >= 4:
            return True

        # High risk with low/medium confidence
        if risk_value >= 3 and confidence < 0.85:
            return True

        # Medium risk with low confidence
        if risk_value >= 2 and confidence < 0.60:
            return True

        return False

    def get_risk_mitigation_recommendations(
        self, risk_level: str, runtime_factors: Optional[Dict[str, Any]] = None
    ) -> list:
        """
        Get recommendations for mitigating identified risks.

        Args:
            risk_level: Risk level
            runtime_factors: Runtime risk factors

        Returns:
            List of mitigation recommendations
        """
        recommendations = []
        risk_value = self.RISK_LEVELS.get(risk_level, 2)
        runtime_factors = runtime_factors or {}

        if risk_value >= 3:
            recommendations.append("Enable audit logging for all executions")
            recommendations.append("Require human review for edge cases")

        if risk_value >= 4:
            recommendations.append("Implement two-phase commit for operations")
            recommendations.append("Add rollback capability")
            recommendations.append("Require approval from authorized personnel")

        if runtime_factors.get("has_external_api_calls"):
            recommendations.append("Implement timeout and retry logic")
            recommendations.append("Add circuit breaker for external API failures")

        if runtime_factors.get("financial_operation"):
            recommendations.append("Add transaction limits and approval thresholds")
            recommendations.append("Implement preview mode before execution")
            recommendations.append("Enable rollback window")

        if runtime_factors.get("modifies_data"):
            recommendations.append("Create backup before modification")
            recommendations.append("Add data validation checks")

        return recommendations
