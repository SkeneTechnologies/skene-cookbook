# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Instrumented skill executor with full evaluation harness integration.

Non-breaking wrapper for skill execution that provides:
- Runtime I/O validation
- Distributed tracing
- Metrics collection
- Auto-act vs flag decision-making
"""

import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from .core.metrics_collector import MetricsCollector
from .core.tracer import SkillTracer
from .core.validator import SkillValidator, ValidationResult
from .decision.confidence_scorer import ConfidenceScorer
from .decision.decision_engine import Decision, DecisionEngine, DecisionType
from .decision.risk_evaluator import RiskEvaluator


@dataclass
class ExecutionResult:
    """Result of instrumented skill execution."""

    success: bool
    outputs: Dict[str, Any]
    decision: Decision
    input_validation: ValidationResult
    output_validation: ValidationResult
    duration_ms: float
    error: Optional[str] = None
    trace_id: Optional[str] = None


class InstrumentedSkillExecutor:
    """
    Instrumented wrapper for skill execution.

    Provides full observability and evaluation without modifying skill implementations.
    """

    def __init__(
        self,
        validator: Optional[SkillValidator] = None,
        tracer: Optional[SkillTracer] = None,
        metrics_collector: Optional[MetricsCollector] = None,
        decision_engine: Optional[DecisionEngine] = None,
        confidence_scorer: Optional[ConfidenceScorer] = None,
        risk_evaluator: Optional[RiskEvaluator] = None,
    ):
        """
        Initialize instrumented executor.

        Args:
            validator: Optional custom validator
            tracer: Optional custom tracer
            metrics_collector: Optional custom metrics collector
            decision_engine: Optional custom decision engine
            confidence_scorer: Optional custom confidence scorer
            risk_evaluator: Optional custom risk evaluator
        """
        self.validator = validator or SkillValidator()
        self.tracer = tracer or SkillTracer(provider="console")
        self.metrics_collector = metrics_collector or MetricsCollector()
        self.decision_engine = decision_engine or DecisionEngine()
        self.confidence_scorer = confidence_scorer or ConfidenceScorer()
        self.risk_evaluator = risk_evaluator or RiskEvaluator()

    def execute_skill(
        self,
        skill_id: str,
        skill_version: str,
        inputs: Dict[str, Any],
        skill_logic: Callable[[Dict[str, Any]], Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None,
        runtime_risk_factors: Optional[Dict[str, Any]] = None,
    ) -> ExecutionResult:
        """
        Execute skill with full instrumentation.

        Args:
            skill_id: Skill identifier (e.g., 'elg_mdf_tracker')
            skill_version: Skill version
            inputs: Input data
            skill_logic: Callable that executes the actual skill logic
            context: Optional execution context
            runtime_risk_factors: Optional runtime risk factors

        Returns:
            ExecutionResult with all instrumentation data
        """
        start_time = time.time()
        context = context or {}

        # Step 1: Validate inputs
        input_validation = self.validator.validate_input(skill_id, inputs)

        # Step 2: Get risk level
        static_risk_level = self.validator.get_risk_level(skill_id)
        risk_assessment = self.risk_evaluator.evaluate_risk(static_risk_level, runtime_risk_factors)

        # Step 3: Calculate confidence
        execution_history = self.decision_engine.get_execution_history(skill_id)
        confidence = self.confidence_scorer.calculate_confidence(
            skill_id=skill_id,
            input_data=inputs,
            validation_passed=input_validation.valid,
            execution_history=execution_history,
            context=context,
        )

        # Step 4: Make decision (auto-act vs flag vs block)
        decision = self.decision_engine.make_decision(
            skill_id=skill_id,
            confidence=confidence,
            risk_level=risk_assessment["risk_level"],
            validation_passed=input_validation.valid,
            execution_history=execution_history,
        )

        # Step 5: Check if execution should be blocked
        if decision.is_blocked():
            duration_ms = (time.time() - start_time) * 1000
            return ExecutionResult(
                success=False,
                outputs={},
                decision=decision,
                input_validation=input_validation,
                output_validation=ValidationResult(valid=False),
                duration_ms=duration_ms,
                error=f"Execution blocked: {decision.reasoning}",
            )

        # Step 6: Execute with tracing
        outputs = {}
        error = None
        trace_id = None

        with self.tracer.trace_skill_execution(skill_id, skill_version, inputs) as span:
            try:
                # Set trace attributes
                span.set_attribute("validation.input_passed", input_validation.valid)
                span.set_attribute("decision.type", decision.type.value)
                span.set_attribute("decision.confidence", confidence)
                span.set_attribute("risk.level", risk_assessment["risk_level"])

                # Execute skill logic
                outputs = skill_logic(inputs)

                # Mark as successful
                span.set_attribute("execution.success", True)
                trace_id = span.trace_id

            except Exception as e:
                error = str(e)
                span.set_status("error", error)
                span.set_attribute("execution.success", False)
                span.set_attribute("error.type", type(e).__name__)
                trace_id = span.trace_id

        # Step 7: Validate outputs (if execution succeeded)
        output_validation = ValidationResult(valid=False)
        if not error and outputs:
            output_validation = self.validator.validate_output(skill_id, outputs)

        # Step 8: Record metrics
        duration_ms = (time.time() - start_time) * 1000
        success = error is None and output_validation.valid

        self.metrics_collector.record_execution(
            skill_id=skill_id,
            skill_version=skill_version,
            duration_ms=duration_ms,
            success=success,
            validation_passed=input_validation.valid and output_validation.valid,
            decision_type=decision.type.value,
            error_type=type(error).__name__ if error else None,
            error_message=error,
            metadata={
                "confidence": confidence,
                "risk_level": risk_assessment["risk_level"],
                "trace_id": trace_id,
            },
        )

        # Step 9: Record execution outcome for history tracking
        self.decision_engine.record_execution_outcome(
            skill_id=skill_id, success=success, confidence=confidence
        )

        return ExecutionResult(
            success=success,
            outputs=outputs,
            decision=decision,
            input_validation=input_validation,
            output_validation=output_validation,
            duration_ms=duration_ms,
            error=error,
            trace_id=trace_id,
        )


class InstrumentedWorkflowExecutor:
    """
    Instrumented executor for workflows (chains of skills).

    Provides workflow-level tracing and validation of chain compatibility.
    """

    def __init__(
        self,
        skill_executor: Optional[InstrumentedSkillExecutor] = None,
        validator: Optional[SkillValidator] = None,
        tracer: Optional[SkillTracer] = None,
    ):
        """
        Initialize instrumented workflow executor.

        Args:
            skill_executor: Optional custom skill executor
            validator: Optional custom validator
            tracer: Optional custom tracer
        """
        self.skill_executor = skill_executor or InstrumentedSkillExecutor()
        self.validator = validator or self.skill_executor.validator
        self.tracer = tracer or self.skill_executor.tracer

    def execute_workflow(
        self,
        workflow_id: str,
        workflow_version: str,
        steps: list,  # List of (skill_id, skill_logic, field_mappings)
        initial_inputs: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute workflow with instrumentation.

        Args:
            workflow_id: Workflow identifier
            workflow_version: Workflow version
            steps: List of workflow steps
            initial_inputs: Initial input data

        Returns:
            Final workflow outputs
        """
        with self.tracer.trace_workflow_execution(workflow_id, workflow_version) as workflow_span:
            outputs = {}
            previous_outputs = initial_inputs

            for step_idx, (skill_id, skill_logic, field_mappings) in enumerate(steps):
                # Validate chain compatibility
                if step_idx > 0:
                    prev_skill_id = steps[step_idx - 1][0]
                    chain_validation = self.validator.validate_chain_compatibility(
                        producer_skill_id=prev_skill_id,
                        consumer_skill_id=skill_id,
                        field_mappings=field_mappings,
                    )

                    if not chain_validation.valid:
                        workflow_span.set_attribute(
                            f"step_{step_idx}.chain_validation_failed", True
                        )
                        print(f"Warning: Chain validation failed: {chain_validation.errors}")

                # Map inputs from previous outputs
                step_inputs = self._map_inputs(previous_outputs, field_mappings)

                # Execute step
                result = self.skill_executor.execute_skill(
                    skill_id=skill_id,
                    skill_version="1.0.0",  # TODO: Get from workflow config
                    inputs=step_inputs,
                    skill_logic=skill_logic,
                    context={"workflow_id": workflow_id, "step_idx": step_idx},
                )

                if not result.success:
                    workflow_span.set_status("error", result.error)
                    raise RuntimeError(f"Step {step_idx} failed: {result.error}")

                outputs = result.outputs
                previous_outputs = {**previous_outputs, **outputs}

                workflow_span.set_attribute(f"step_{step_idx}.success", True)

            workflow_span.set_attribute("workflow.steps_completed", len(steps))
            return outputs

    def _map_inputs(
        self, outputs: Dict[str, Any], field_mappings: Optional[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Map outputs from previous step to inputs for next step.

        Args:
            outputs: Outputs from previous step
            field_mappings: Field mappings (e.g., {'output.partner_id': 'input.partnerId'})

        Returns:
            Mapped inputs
        """
        if not field_mappings:
            return outputs

        mapped = {}
        for output_field, input_field in field_mappings.items():
            output_key = output_field.split(".")[-1]
            input_key = input_field.split(".")[-1]

            if output_key in outputs:
                mapped[input_key] = outputs[output_key]

        return mapped
