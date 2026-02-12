# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
OpenTelemetry-based distributed tracing for skill execution.
"""

import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


@dataclass
class SpanContext:
    """Context for a trace span."""

    span_id: str
    trace_id: str
    parent_span_id: Optional[str]
    name: str
    start_time: float
    end_time: Optional[float] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    status: str = "ok"  # ok, error
    error_message: Optional[str] = None

    def duration_ms(self) -> Optional[float]:
        """Calculate duration in milliseconds."""
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time) * 1000

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'span_id': self.span_id,
            'trace_id': self.trace_id,
            'parent_span_id': self.parent_span_id,
            'name': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration_ms': self.duration_ms(),
            'attributes': self.attributes,
            'status': self.status,
            'error_message': self.error_message,
        }


class SkillTracer:
    """
    OpenTelemetry-based distributed tracing for skill execution.

    Captures hierarchical spans: Workflow → Steps → Skills
    """

    def __init__(
        self,
        provider: str = 'console',
        endpoint: Optional[str] = None,
        service_name: str = 'skene-cookbook'
    ):
        """
        Initialize tracer.

        Args:
            provider: 'console' for dev, 'otlp' for production, 'none' to disable
            endpoint: OTLP endpoint (e.g., 'http://localhost:4317')
            service_name: Service name for traces
        """
        self.provider = provider
        self.endpoint = endpoint
        self.service_name = service_name
        self._spans: List[SpanContext] = []
        self._current_trace_id: Optional[str] = None
        self._span_stack: List[SpanContext] = []

    def _generate_id(self) -> str:
        """Generate unique span/trace ID."""
        import uuid
        return uuid.uuid4().hex[:16]

    @contextmanager
    def trace_skill_execution(
        self,
        skill_id: str,
        skill_version: str,
        inputs: Dict[str, Any],
        parent_span: Optional[SpanContext] = None
    ):
        """
        Context manager for tracing skill execution.

        Usage:
            with tracer.trace_skill_execution('elg_mdf_tracker', '1.0.0', inputs) as span:
                outputs = execute_skill(inputs)
                span.set_attribute('validation.passed', True)
                span.set_attribute('decision.type', 'auto_act')

        Args:
            skill_id: Skill identifier
            skill_version: Skill version
            inputs: Input data
            parent_span: Parent span for hierarchical tracing

        Yields:
            SpanContext for the current execution
        """
        # Generate span and trace IDs
        span_id = self._generate_id()
        trace_id = self._current_trace_id or self._generate_id()
        self._current_trace_id = trace_id

        # Use parent span if provided, otherwise check span stack
        if parent_span:
            parent_span_id = parent_span.span_id
        elif self._span_stack:
            parent_span_id = self._span_stack[-1].span_id
        else:
            parent_span_id = None

        # Create span
        span = SpanContext(
            span_id=span_id,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            name=f"skill.{skill_id}",
            start_time=time.time(),
            attributes={
                'skill.id': skill_id,
                'skill.version': skill_version,
                'skill.input_keys': list(inputs.keys()) if inputs else [],
            }
        )

        self._span_stack.append(span)

        try:
            # Create span wrapper for user convenience
            span_wrapper = SpanWrapper(span)
            yield span_wrapper

            # Mark as successful
            span.status = "ok"

        except Exception as e:
            # Capture error
            span.status = "error"
            span.error_message = str(e)
            raise

        finally:
            # Complete span
            span.end_time = time.time()
            self._spans.append(span)
            self._span_stack.pop()

            # Export span
            self._export_span(span)

    @contextmanager
    def trace_workflow_execution(
        self,
        workflow_id: str,
        workflow_version: str
    ):
        """
        Context manager for tracing workflow execution.

        Args:
            workflow_id: Workflow identifier
            workflow_version: Workflow version

        Yields:
            SpanContext for the workflow
        """
        span_id = self._generate_id()
        trace_id = self._generate_id()
        self._current_trace_id = trace_id

        span = SpanContext(
            span_id=span_id,
            trace_id=trace_id,
            parent_span_id=None,
            name=f"workflow.{workflow_id}",
            start_time=time.time(),
            attributes={
                'workflow.id': workflow_id,
                'workflow.version': workflow_version,
            }
        )

        self._span_stack.append(span)

        try:
            span_wrapper = SpanWrapper(span)
            yield span_wrapper
            span.status = "ok"

        except Exception as e:
            span.status = "error"
            span.error_message = str(e)
            raise

        finally:
            span.end_time = time.time()
            self._spans.append(span)
            self._span_stack.pop()
            self._export_span(span)

    def _export_span(self, span: SpanContext):
        """Export span to configured provider."""
        if self.provider == 'console':
            self._export_console(span)
        elif self.provider == 'otlp':
            self._export_otlp(span)
        # 'none' provider does nothing

    def _export_console(self, span: SpanContext):
        """Export span to console (for development)."""
        indent = "  " * len(self._span_stack)
        status_symbol = "✓" if span.status == "ok" else "✗"
        duration = f"{span.duration_ms():.2f}ms" if span.duration_ms() else "?"

        print(f"{indent}{status_symbol} {span.name} ({duration})")

        if span.error_message:
            print(f"{indent}  Error: {span.error_message}")

    def _export_otlp(self, span: SpanContext):
        """
        Export span to OTLP endpoint.

        In production, this would use the OpenTelemetry SDK to send
        traces to a collector like Jaeger, Tempo, or Honeycomb.
        """
        # TODO: Implement OTLP export using opentelemetry-exporter-otlp
        # For now, just log
        if self.endpoint:
            # Would send to self.endpoint
            pass

    def get_spans(self) -> List[SpanContext]:
        """Get all captured spans."""
        return self._spans

    def export_json(self) -> str:
        """Export all spans as JSON."""
        return json.dumps(
            [span.to_dict() for span in self._spans],
            indent=2
        )

    def reset(self):
        """Reset tracer state (useful for testing)."""
        self._spans = []
        self._current_trace_id = None
        self._span_stack = []


class SpanWrapper:
    """Wrapper for SpanContext to provide user-friendly API."""

    def __init__(self, span: SpanContext):
        self._span = span

    def set_attribute(self, key: str, value: Any):
        """Set span attribute."""
        self._span.attributes[key] = value

    def set_status(self, status: str, error_message: Optional[str] = None):
        """Set span status."""
        self._span.status = status
        if error_message:
            self._span.error_message = error_message

    @property
    def span_id(self) -> str:
        """Get span ID."""
        return self._span.span_id

    @property
    def trace_id(self) -> str:
        """Get trace ID."""
        return self._span.trace_id
