"""
Unit tests for eval_harness SkillTracer.
"""

import pytest

from eval_harness.core.tracer import SkillTracer, SpanContext


@pytest.fixture
def tracer():
    """Create tracer instance."""
    return SkillTracer(provider="none")  # Disable output for tests


def test_tracer_initialization(tracer):
    """Test tracer initializes correctly."""
    assert tracer is not None
    assert tracer.provider == "none"


def test_trace_skill_execution(tracer):
    """Test tracing a skill execution."""
    inputs = {"partnerId": "test-123", "action": "check_budget"}

    with tracer.trace_skill_execution("elg_mdf_tracker", "1.0.0", inputs) as span:
        # Simulate work
        span.set_attribute("validation.passed", True)
        span.set_attribute("decision.type", "auto_act")

    spans = tracer.get_spans()
    assert len(spans) == 1

    span = spans[0]
    assert span.name == "skill.elg_mdf_tracker"
    assert span.status == "ok"
    assert span.attributes["skill.id"] == "elg_mdf_tracker"
    assert span.attributes["skill.version"] == "1.0.0"
    assert span.attributes["validation.passed"] is True
    assert span.duration_ms() is not None


def test_trace_skill_execution_with_error(tracer):
    """Test tracing captures errors."""
    inputs = {"partnerId": "test-123", "action": "check_budget"}

    with pytest.raises(ValueError):
        with tracer.trace_skill_execution("elg_mdf_tracker", "1.0.0", inputs) as span:
            raise ValueError("Test error")

    spans = tracer.get_spans()
    assert len(spans) == 1

    span = spans[0]
    assert span.status == "error"
    assert "Test error" in span.error_message


def test_trace_workflow_execution(tracer):
    """Test tracing a workflow execution."""
    with tracer.trace_workflow_execution("test_workflow", "1.0.0") as workflow_span:
        workflow_span.set_attribute("steps", 3)

    spans = tracer.get_spans()
    assert len(spans) == 1

    span = spans[0]
    assert span.name == "workflow.test_workflow"
    assert span.attributes["workflow.id"] == "test_workflow"


def test_hierarchical_tracing(tracer):
    """Test hierarchical span relationships."""
    with tracer.trace_workflow_execution("test_workflow", "1.0.0") as workflow_span:
        # Nested skill execution
        with tracer.trace_skill_execution("elg_mdf_tracker", "1.0.0", {}) as skill_span:
            pass

    spans = tracer.get_spans()
    assert len(spans) == 2

    # Spans are added in completion order, so skill completes first
    skill_span = spans[0]
    workflow_span = spans[1]

    # Skill span should have workflow as parent
    assert skill_span.parent_span_id == workflow_span.span_id
    assert skill_span.trace_id == workflow_span.trace_id


def test_export_json(tracer):
    """Test exporting spans as JSON."""
    with tracer.trace_skill_execution("elg_mdf_tracker", "1.0.0", {}) as span:
        span.set_attribute("test", "value")

    json_output = tracer.export_json()
    assert "elg_mdf_tracker" in json_output
    assert "test" in json_output


def test_reset(tracer):
    """Test resetting tracer state."""
    with tracer.trace_skill_execution("elg_mdf_tracker", "1.0.0", {}) as span:
        pass

    assert len(tracer.get_spans()) == 1

    tracer.reset()
    assert len(tracer.get_spans()) == 0
