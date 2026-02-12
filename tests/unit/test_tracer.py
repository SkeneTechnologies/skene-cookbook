# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Unit tests for eval_harness SkillTracer.
"""

import time

import pytest

from eval_harness.core.tracer import SkillTracer, SpanContext, SpanWrapper


@pytest.fixture
def tracer():
    """Create tracer instance."""
    return SkillTracer(provider="none", service_name="test-service")


def test_tracer_initialization():
    """Test tracer initializes with correct defaults."""
    tracer = SkillTracer()
    assert tracer.provider == "console"
    assert tracer.service_name == "skene-cookbook"
    assert tracer._spans == []
    assert tracer._current_trace_id is None


def test_tracer_custom_initialization():
    """Test tracer with custom configuration."""
    tracer = SkillTracer(
        provider="otlp", endpoint="http://localhost:4317", service_name="custom-service"
    )
    assert tracer.provider == "otlp"
    assert tracer.endpoint == "http://localhost:4317"
    assert tracer.service_name == "custom-service"


def test_span_context_creation():
    """Test SpanContext dataclass creation."""
    span = SpanContext(
        span_id="span123",
        trace_id="trace456",
        parent_span_id="parent789",
        name="test-skill",
        start_time=time.time(),
    )

    assert span.span_id == "span123"
    assert span.trace_id == "trace456"
    assert span.parent_span_id == "parent789"
    assert span.name == "test-skill"
    assert span.status == "ok"
    assert span.error_message is None


def test_span_context_duration():
    """Test span duration calculation."""
    start = time.time()
    span = SpanContext(
        span_id="span1", trace_id="trace1", parent_span_id=None, name="test", start_time=start
    )

    # Initially no duration
    assert span.duration_ms() is None

    # After ending
    time.sleep(0.01)  # Sleep 10ms
    span.end_time = time.time()
    duration = span.duration_ms()

    assert duration is not None
    assert duration >= 10.0  # At least 10ms


def test_span_context_to_dict():
    """Test span conversion to dictionary."""
    span = SpanContext(
        span_id="span1",
        trace_id="trace1",
        parent_span_id="parent1",
        name="test-skill",
        start_time=1000.0,
        end_time=1001.5,
        attributes={"key": "value"},
        status="ok",
    )

    result = span.to_dict()

    assert result["span_id"] == "span1"
    assert result["trace_id"] == "trace1"
    assert result["parent_span_id"] == "parent1"
    assert result["name"] == "test-skill"
    assert result["start_time"] == 1000.0
    assert result["end_time"] == 1001.5
    assert result["duration_ms"] == 1500.0
    assert result["attributes"] == {"key": "value"}
    assert result["status"] == "ok"


def test_span_context_error_status():
    """Test span with error status."""
    span = SpanContext(
        span_id="span1",
        trace_id="trace1",
        parent_span_id=None,
        name="failed-skill",
        start_time=time.time(),
        status="error",
        error_message="Test error occurred",
    )

    assert span.status == "error"
    assert span.error_message == "Test error occurred"

    result = span.to_dict()
    assert result["status"] == "error"
    assert result["error_message"] == "Test error occurred"


def test_generate_id(tracer):
    """Test ID generation is unique."""
    id1 = tracer._generate_id()
    id2 = tracer._generate_id()

    assert id1 != id2
    assert len(id1) == 16
    assert len(id2) == 16
    assert all(c in "0123456789abcdef" for c in id1)
    assert all(c in "0123456789abcdef" for c in id2)


def test_trace_skill_execution_success(tracer):
    """Test successful skill execution tracing."""
    inputs = {"partnerId": "test-123", "action": "check_budget"}

    with tracer.trace_skill_execution("elg_mdf_tracker", "1.0.0", inputs) as span_wrapper:
        assert span_wrapper is not None
        assert isinstance(span_wrapper, SpanWrapper)
        assert span_wrapper.span_id is not None
        assert span_wrapper.trace_id is not None

        # Simulate work
        time.sleep(0.01)

    # After context exit, tracer should have recorded the span
    assert len(tracer.get_spans()) >= 1
    last_span = tracer.get_spans()[-1]
    assert last_span.status == "ok"
    assert last_span.duration_ms() is not None
    assert last_span.duration_ms() >= 10.0


def test_trace_skill_execution_with_error(tracer):
    """Test skill execution tracing with error."""
    inputs = {"partnerId": "test-123"}

    try:
        with tracer.trace_skill_execution("elg_mdf_tracker", "1.0.0", inputs) as span_wrapper:
            # Simulate error
            raise ValueError("Test error")
    except ValueError:
        pass

    # Check recorded span has error status
    last_span = tracer.get_spans()[-1]
    assert last_span.status == "error"
    assert "Test error" in last_span.error_message


def test_span_attributes(tracer):
    """Test setting span attributes via SpanWrapper."""
    inputs = {"partnerId": "test-123"}

    with tracer.trace_skill_execution("elg_mdf_tracker", "1.0.0", inputs) as span_wrapper:
        span_wrapper.set_attribute("validation.passed", True)
        span_wrapper.set_attribute("decision.type", "auto_act")
        span_wrapper.set_attribute("risk_level", "Low")

    # Check recorded span has attributes
    last_span = tracer.get_spans()[-1]
    assert last_span.attributes["validation.passed"] is True
    assert last_span.attributes["decision.type"] == "auto_act"
    assert last_span.attributes["risk_level"] == "Low"


def test_get_active_traces(tracer):
    """Test retrieving active traces."""
    inputs = {"partnerId": "test-123"}

    # Initially no traces
    assert len(tracer.get_spans()) == 0

    # Create some spans
    with tracer.trace_skill_execution("skill1", "1.0.0", inputs):
        pass

    with tracer.trace_skill_execution("skill2", "1.0.0", inputs):
        pass

    # Should have recorded spans
    assert len(tracer.get_spans()) >= 2


def test_span_serialization():
    """Test span can be serialized to JSON."""
    import json

    span = SpanContext(
        span_id="span1",
        trace_id="trace1",
        parent_span_id=None,
        name="test-skill",
        start_time=1000.0,
        end_time=1001.0,
    )

    # Should be JSON serializable
    json_str = json.dumps(span.to_dict())
    assert json_str is not None

    # Should be deserializable
    data = json.loads(json_str)
    assert data["span_id"] == "span1"
    assert data["trace_id"] == "trace1"


def test_multiple_traces(tracer):
    """Test multiple independent traces."""
    inputs1 = {"partnerId": "test-123"}
    inputs2 = {"partnerId": "test-456"}

    with tracer.trace_skill_execution("skill1", "1.0.0", inputs1) as span1:
        pass

    # Reset trace context to start new trace
    tracer._current_trace_id = None

    with tracer.trace_skill_execution("skill2", "1.0.0", inputs2) as span2:
        pass

    # Check we have 2 spans recorded
    assert len(tracer.get_spans()) >= 2


def test_tracer_reset(tracer):
    """Test tracer reset clears state."""
    inputs = {"partnerId": "test-123"}

    with tracer.trace_skill_execution("skill1", "1.0.0", inputs):
        pass

    assert len(tracer.get_spans()) >= 1

    tracer.reset()

    assert len(tracer.get_spans()) == 0
    assert tracer._current_trace_id is None
    assert tracer._span_stack == []


def test_tracer_export_json(tracer):
    """Test exporting spans as JSON."""
    inputs = {"partnerId": "test-123"}

    with tracer.trace_skill_execution("skill1", "1.0.0", inputs):
        pass

    json_output = tracer.export_json()
    assert json_output is not None

    import json

    data = json.loads(json_output)
    assert isinstance(data, list)
    assert len(data) >= 1


def test_span_wrapper_properties(tracer):
    """Test SpanWrapper properties."""
    inputs = {"partnerId": "test-123"}

    with tracer.trace_skill_execution("skill1", "1.0.0", inputs) as span_wrapper:
        # Test properties are accessible
        assert span_wrapper.span_id is not None
        assert span_wrapper.trace_id is not None
        assert len(span_wrapper.span_id) == 16
        assert len(span_wrapper.trace_id) == 16
