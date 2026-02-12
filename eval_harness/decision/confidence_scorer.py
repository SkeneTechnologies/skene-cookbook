# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Confidence scoring for skill execution.

Calculates confidence based on multiple factors:
- Input data completeness and quality
- Historical execution success rate
- Schema validation results
- Execution context
"""

from typing import Dict, Any, Optional


class ConfidenceScorer:
    """
    Calculate confidence scores for skill execution.

    Confidence is a 0.0-1.0 score indicating how confident we are that
    the skill will execute successfully with the given inputs.
    """

    def __init__(self):
        """Initialize confidence scorer."""
        pass

    def calculate_confidence(
        self,
        skill_id: str,
        input_data: Dict[str, Any],
        validation_passed: bool,
        execution_history: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        Calculate confidence score for skill execution.

        Args:
            skill_id: Skill identifier
            input_data: Input data for execution
            validation_passed: Whether I/O validation passed
            execution_history: Optional historical execution stats
            context: Optional additional context

        Returns:
            Confidence score between 0.0 and 1.0
        """
        scores = []
        weights = []

        # Factor 1: Validation status (35% weight)
        validation_score = 1.0 if validation_passed else 0.0
        scores.append(validation_score)
        weights.append(0.35)

        # Factor 2: Input data completeness (25% weight)
        completeness_score = self._calculate_input_completeness(input_data)
        scores.append(completeness_score)
        weights.append(0.25)

        # Factor 3: Historical success rate (30% weight if available, else redistribute)
        if execution_history and execution_history.get('total_executions', 0) >= 5:
            history_score = execution_history.get('success_rate', 0.5)
            scores.append(history_score)
            weights.append(0.30)
        else:
            # Redistribute weight to validation and completeness
            weights[0] += 0.15  # validation gets more weight
            weights[1] += 0.15  # completeness gets more weight

        # Factor 4: Context quality (10% weight)
        context_score = self._calculate_context_quality(context or {})
        scores.append(context_score)
        weights.append(0.10)

        # Normalize weights
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]

        # Calculate weighted average
        confidence = sum(s * w for s, w in zip(scores, normalized_weights))

        return round(confidence, 3)

    def _calculate_input_completeness(self, input_data: Dict[str, Any]) -> float:
        """
        Calculate completeness score for input data.

        Checks for:
        - Presence of data (not empty dict)
        - Non-null values
        - Non-empty strings
        - Valid data types

        Args:
            input_data: Input data dictionary

        Returns:
            Completeness score 0.0-1.0
        """
        if not input_data:
            return 0.3  # Empty input, but might be valid for some skills

        total_fields = len(input_data)
        complete_fields = 0

        for key, value in input_data.items():
            # Check if field has meaningful value
            if value is None:
                continue  # Null value

            if isinstance(value, str) and value.strip() == "":
                continue  # Empty string

            if isinstance(value, (list, dict)) and len(value) == 0:
                continue  # Empty collection

            complete_fields += 1

        completeness = complete_fields / total_fields if total_fields > 0 else 0.5

        return round(completeness, 3)

    def _calculate_context_quality(self, context: Dict[str, Any]) -> float:
        """
        Calculate quality score for execution context.

        Context might include:
        - User information
        - Session data
        - Previous step results (in workflows)
        - Environmental data

        Args:
            context: Execution context

        Returns:
            Quality score 0.0-1.0
        """
        if not context:
            return 0.5  # Neutral score if no context

        quality_indicators = 0
        total_indicators = 5

        # Has user information
        if context.get('user_id') or context.get('user'):
            quality_indicators += 1

        # Has session information
        if context.get('session_id') or context.get('session'):
            quality_indicators += 1

        # Has previous results (for chaining)
        if context.get('previous_results') or context.get('upstream_outputs'):
            quality_indicators += 1

        # Has timestamp
        if context.get('timestamp'):
            quality_indicators += 1

        # Has metadata
        if context.get('metadata'):
            quality_indicators += 1

        return round(quality_indicators / total_indicators, 3)
