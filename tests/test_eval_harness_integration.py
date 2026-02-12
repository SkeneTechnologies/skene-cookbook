"""
Integration tests for eval_harness end-to-end workflows.
"""

import json
from pathlib import Path

import pytest

from eval_harness.core import MetricsCollector, SkillTracer, SkillValidator
from eval_harness.decision import DecisionEngine, DecisionType
from eval_harness.instrumented_executor import InstrumentedSkillExecutor
from eval_harness.reporters import JSONReporter, MarkdownReporter


@pytest.fixture
def executor():
    """Create instrumented executor."""
    return InstrumentedSkillExecutor()


@pytest.fixture
def dummy_skill_logic():
    """Dummy skill implementation for testing."""

    def logic(inputs):
        # Simulate MDF tracker logic
        return {
            "available_budget": 10000.0,
            "allocated": 5000.0,
            "spent": 2000.0,
            "pending_requests": [],
            "roi_summary": {},
        }

    return logic


def test_full_instrumented_execution(executor, dummy_skill_logic):
    """Test complete instrumented execution flow."""
    result = executor.execute_skill(
        skill_id="elg_mdf_tracker",
        skill_version="1.0.0",
        inputs={"partnerId": "test-partner-123", "action": "check_budget"},
        skill_logic=dummy_skill_logic,
        context={"user_id": "user-456"},
        runtime_risk_factors={"financial_operation": True},
    )

    # Verify execution succeeded
    assert result.success is True
    assert result.outputs is not None
    assert "available_budget" in result.outputs

    # Verify decision was made
    assert result.decision is not None
    # With financial_operation=True, risk becomes Critical -> REQUIRE_APPROVAL
    assert result.decision.type in [
        DecisionType.AUTO_ACT,
        DecisionType.FLAG_FOR_REVIEW,
        DecisionType.REQUIRE_APPROVAL,
    ]
    assert 0.0 <= result.decision.confidence <= 1.0

    # Verify validation ran
    assert result.input_validation is not None
    assert result.input_validation.valid is True
    assert result.output_validation is not None
    assert result.output_validation.valid is True

    # Verify metrics recorded
    assert result.duration_ms > 0
    assert result.trace_id is not None


def test_validation_failure_blocks_execution(executor):
    """Test that validation failure blocks execution."""

    def should_not_execute(inputs):
        raise AssertionError("Should not execute with invalid inputs")

    result = executor.execute_skill(
        skill_id="elg_mdf_tracker",
        skill_version="1.0.0",
        inputs={"partnerId": "test-123", "action": "invalid_action"},  # Invalid enum value
        skill_logic=should_not_execute,
    )

    # Execution should be blocked
    assert result.success is False
    assert result.decision.is_blocked() is True
    assert result.input_validation.valid is False
    assert len(result.input_validation.errors) > 0


def test_metrics_aggregation(executor, dummy_skill_logic):
    """Test metrics are properly aggregated across multiple executions."""
    test_cases = [
        {"partnerId": "p1", "action": "check_budget"},
        {"partnerId": "p2", "action": "request", "requestData": {}},
        {"partnerId": "p3", "action": "report"},
    ]

    # Execute multiple test cases
    for test_case in test_cases:
        executor.execute_skill(
            skill_id="elg_mdf_tracker",
            skill_version="1.0.0",
            inputs=test_case,
            skill_logic=dummy_skill_logic,
        )

    # Get aggregated metrics
    metrics = executor.metrics_collector.get_aggregated_metrics("elg_mdf_tracker")

    assert metrics is not None
    assert metrics.total_executions == 3
    assert metrics.success_rate > 0.0
    assert metrics.avg_duration_ms > 0.0
    assert len(metrics.records) == 3


def test_decision_engine_integration(executor, dummy_skill_logic):
    """Test decision engine makes correct decisions."""
    # High confidence case (valid inputs) -> AUTO_ACT
    result = executor.execute_skill(
        skill_id="elg_mdf_tracker",
        skill_version="1.0.0",
        inputs={"partnerId": "test-123", "action": "check_budget"},
        skill_logic=dummy_skill_logic,
    )

    assert result.decision.type == DecisionType.AUTO_ACT
    assert result.decision.confidence >= 0.85

    # Invalid inputs -> BLOCK
    result = executor.execute_skill(
        skill_id="elg_mdf_tracker",
        skill_version="1.0.0",
        inputs={"partnerId": "test-123", "action": "invalid"},
        skill_logic=dummy_skill_logic,
    )

    assert result.decision.is_blocked() is True


def test_report_generation(executor, dummy_skill_logic, tmp_path):
    """Test report generation works end-to-end."""
    # Execute some test cases
    for i in range(5):
        executor.execute_skill(
            skill_id="elg_mdf_tracker",
            skill_version="1.0.0",
            inputs={"partnerId": f"p{i}", "action": "check_budget"},
            skill_logic=dummy_skill_logic,
        )

    # Get metrics
    metrics = executor.metrics_collector.get_aggregated_metrics("elg_mdf_tracker")

    # Generate reports
    md_reporter = MarkdownReporter(output_dir=tmp_path)
    json_reporter = JSONReporter(output_dir=tmp_path)

    md_path = md_reporter.save_skill_report(
        skill_id="elg_mdf_tracker", metrics=metrics, session_id="test_session"
    )

    json_path = json_reporter.save_skill_report(
        skill_id="elg_mdf_tracker", metrics=metrics, session_id="test_session"
    )

    # Verify files were created
    assert md_path.exists()
    assert json_path.exists()

    # Verify markdown content
    md_content = md_path.read_text()
    assert "elg_mdf_tracker" in md_content
    assert "Success Rate" in md_content
    assert "Performance Metrics" in md_content

    # Verify JSON content
    json_content = json.loads(json_path.read_text())
    assert json_content["skill_id"] == "elg_mdf_tracker"
    assert "summary" in json_content
    assert "records" in json_content


def test_chain_validation():
    """Test chain validation between skills."""
    validator = SkillValidator()

    # Test valid chain
    result = validator.validate_chain_compatibility(
        producer_skill_id="elg_partner_tier_manager",
        consumer_skill_id="elg_partner_influenced_revenue",
        field_mappings={"output.partnerId": "input.partnerId"},
    )

    # Should have result (may have warnings about optional fields)
    assert result is not None
    assert isinstance(result.valid, bool)


def test_error_handling(executor):
    """Test error handling in instrumented executor."""

    def failing_skill_logic(inputs):
        raise ValueError("Simulated skill error")

    result = executor.execute_skill(
        skill_id="elg_mdf_tracker",
        skill_version="1.0.0",
        inputs={"partnerId": "test-123", "action": "check_budget"},
        skill_logic=failing_skill_logic,
    )

    # Should capture error gracefully
    assert result.success is False
    assert result.error is not None
    assert "Simulated skill error" in result.error

    # Metrics should still be recorded
    metrics = executor.metrics_collector.get_aggregated_metrics("elg_mdf_tracker")
    assert metrics is not None
    assert metrics.total_executions >= 1


def test_tracing_captures_execution():
    """Test that tracing captures execution details."""
    tracer = SkillTracer(provider="none")  # Silent tracing for test

    with tracer.trace_skill_execution("elg_mdf_tracker", "1.0.0", {}) as span:
        span.set_attribute("test_attribute", "test_value")

    spans = tracer.get_spans()
    assert len(spans) == 1

    span = spans[0]
    assert span.name == "skill.elg_mdf_tracker"
    assert span.attributes["test_attribute"] == "test_value"
    assert span.duration_ms() is not None


def test_confidence_scoring():
    """Test confidence scoring with various inputs."""
    from eval_harness.decision import ConfidenceScorer

    scorer = ConfidenceScorer()

    # Complete, valid inputs -> high confidence
    confidence = scorer.calculate_confidence(
        skill_id="elg_mdf_tracker",
        input_data={"partnerId": "test-123", "action": "check_budget"},
        validation_passed=True,
    )

    assert 0.7 <= confidence <= 1.0  # Should be high

    # Empty inputs -> lower confidence
    confidence = scorer.calculate_confidence(
        skill_id="elg_mdf_tracker", input_data={}, validation_passed=False
    )

    assert 0.0 <= confidence <= 0.5  # Should be low


def test_risk_evaluation():
    """Test risk evaluation logic."""
    from eval_harness.decision import RiskEvaluator

    evaluator = RiskEvaluator()

    # Evaluate risk with runtime factors
    assessment = evaluator.evaluate_risk(
        static_risk_level="Medium",
        runtime_factors={"financial_operation": True, "has_external_api_calls": True},
    )

    assert assessment["risk_level"] in ["Low", "Medium", "High", "Critical"]
    assert assessment["static_risk"] == "Medium"
    assert assessment["risk_adjustment"] >= 0
    assert "requires_monitoring" in assessment
    assert "requires_audit_logging" in assessment
