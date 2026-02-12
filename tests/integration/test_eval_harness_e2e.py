# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Integration tests for eval harness end-to-end workflows.

Tests the complete flow: Load → Validate → Execute → Trace → Decide
"""

import pytest
import json
import tempfile
from pathlib import Path
from eval_harness.core.validator import SkillValidator, ValidationResult
from eval_harness.core.tracer import SkillTracer
from eval_harness.decision.decision_engine import DecisionEngine, DecisionType


@pytest.fixture
def temp_skill():
    """Create a temporary test skill."""
    with tempfile.TemporaryDirectory() as tmpdir:
        skills_path = Path(tmpdir) / "skills-library"
        skills_path.mkdir()

        # Create test skill
        domain_path = skills_path / "test_domain"
        domain_path.mkdir()
        skill_path = domain_path / "test_skill"
        skill_path.mkdir()

        skill_data = {
            "id": "test_read_skill",
            "version": "1.0.0",
            "name": "Test Read Skill",
            "description": "Read and display test data",
            "domain": "test_domain",
            "tools": [{"name": "read_data", "required": True}],
            "inputSchema": {
                "type": "object",
                "properties": {
                    "data_id": {"type": "string"}
                },
                "required": ["data_id"]
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "data": {"type": "string"},
                    "status": {"type": "string"}
                },
                "required": ["data", "status"]
            }
        }

        metadata = {
            "security": {
                "risk_level": "Low"
            }
        }

        with open(skill_path / "skill.json", 'w') as f:
            json.dump(skill_data, f)

        with open(skill_path / "metadata.yaml", 'w') as f:
            import yaml
            yaml.dump(metadata, f)

        yield skills_path, skill_data


@pytest.mark.integration
def test_full_eval_harness_flow(temp_skill):
    """Test complete eval harness flow: validate → trace → decide."""
    skills_path, skill_data = temp_skill

    # Step 1: Initialize components
    validator = SkillValidator(skills_path)
    tracer = SkillTracer(provider='none')
    decision_engine = DecisionEngine()

    skill_id = skill_data['id']
    skill_version = skill_data['version']

    # Step 2: Validate input
    test_input = {"data_id": "test-123"}
    input_validation = validator.validate_input(skill_id, test_input)

    assert input_validation.valid is True, f"Input validation failed: {input_validation.errors}"

    # Step 3: Trace execution
    with tracer.trace_skill_execution(skill_id, skill_version, test_input) as span:
        # Simulate skill execution
        test_output = {
            "data": "Test data for test-123",
            "status": "success"
        }

        # Step 4: Validate output
        output_validation = validator.validate_output(skill_id, test_output)
        assert output_validation.valid is True, f"Output validation failed: {output_validation.errors}"

        # Step 5: Get risk level
        risk_level = validator.get_risk_level(skill_id)

        # Step 6: Make execution decision
        decision = decision_engine.make_decision(
            skill_id=skill_id,
            confidence=0.9,
            risk_level=risk_level,
            validation_passed=output_validation.valid
        )

        # Record decision in span
        span.set_attribute('validation.input_passed', input_validation.valid)
        span.set_attribute('validation.output_passed', output_validation.valid)
        span.set_attribute('decision.type', decision.type.value)
        span.set_attribute('decision.confidence', decision.confidence)

    # Verify end-to-end flow
    recorded_spans = tracer.get_spans()
    assert len(recorded_spans) > 0

    last_span = recorded_spans[-1]
    assert last_span.status == 'ok'
    assert last_span.attributes['validation.input_passed'] is True
    assert last_span.attributes['validation.output_passed'] is True
    assert last_span.attributes['decision.type'] == 'auto_act'


@pytest.mark.integration
def test_validation_failure_workflow(temp_skill):
    """Test workflow when validation fails."""
    skills_path, skill_data = temp_skill

    validator = SkillValidator(skills_path)
    tracer = SkillTracer(provider='none')
    decision_engine = DecisionEngine()

    skill_id = skill_data['id']
    skill_version = skill_data['version']

    # Invalid input (missing required field)
    invalid_input = {}

    # Step 1: Validate input (should fail)
    input_validation = validator.validate_input(skill_id, invalid_input)
    assert input_validation.valid is False
    assert len(input_validation.errors) > 0

    # Step 2: Make decision with failed validation
    decision = decision_engine.make_decision(
        skill_id=skill_id,
        confidence=0.9,
        risk_level='Low',
        validation_passed=False
    )

    # Should block execution due to validation failure
    assert decision.type == DecisionType.BLOCK
    assert decision.is_blocked() is True


@pytest.mark.integration
def test_high_risk_skill_workflow(temp_skill):
    """Test workflow with high-risk skill requiring approval."""
    skills_path, skill_data = temp_skill

    # Modify skill to be high risk
    skill_path = skills_path / "test_domain" / "test_skill"

    high_risk_skill = skill_data.copy()
    high_risk_skill['id'] = 'test_high_risk_skill'
    high_risk_skill['description'] = 'Delete user data and execute system commands'

    with open(skill_path / "high_risk_skill.json", 'w') as f:
        json.dump(high_risk_skill, f)

    # Update metadata
    with open(skill_path / "metadata.yaml", 'w') as f:
        import yaml
        yaml.dump({'security': {'risk_level': 'Critical'}}, f)

    validator = SkillValidator(skills_path)
    decision_engine = DecisionEngine()

    # Valid input
    test_input = {"data_id": "test-123"}
    input_validation = validator.validate_input(skill_data['id'], test_input)

    # Make decision for Critical risk
    decision = decision_engine.make_decision(
        skill_id='test_high_risk_skill',
        confidence=0.95,  # Even with high confidence
        risk_level='Critical',
        validation_passed=True
    )

    # Critical risk should require approval
    assert decision.type == DecisionType.REQUIRE_APPROVAL
    assert decision.requires_human_approval() is True


@pytest.mark.integration
def test_chain_compatibility_validation(temp_skill):
    """Test validating skill chain compatibility."""
    skills_path, skill_data = temp_skill

    # Create second skill that consumes first skill's output
    domain_path = skills_path / "test_domain"
    skill2_path = domain_path / "consumer_skill"
    skill2_path.mkdir()

    skill2_data = {
        "id": "consumer_skill",
        "version": "1.0.0",
        "name": "Consumer Skill",
        "description": "Consume data from producer",
        "domain": "test_domain",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data": {"type": "string"},
                "status": {"type": "string"}
            },
            "required": ["data"]
        },
        "outputSchema": {
            "type": "object",
            "properties": {
                "processed": {"type": "boolean"}
            }
        }
    }

    with open(skill2_path / "skill.json", 'w') as f:
        json.dump(skill2_data, f)

    # Validate chain compatibility
    validator = SkillValidator(skills_path)

    result = validator.validate_chain_compatibility(
        producer_skill_id=skill_data['id'],
        consumer_skill_id='consumer_skill',
        field_mappings={
            'output.data': 'input.data',
            'output.status': 'input.status'
        }
    )

    assert result is not None
    assert isinstance(result, ValidationResult)


@pytest.mark.integration
def test_error_handling_workflow(temp_skill):
    """Test error handling in eval harness workflow."""
    skills_path, skill_data = temp_skill

    validator = SkillValidator(skills_path)
    tracer = SkillTracer(provider='none')

    skill_id = skill_data['id']
    skill_version = skill_data['version']

    # Valid input
    test_input = {"data_id": "test-123"}

    # Trace execution with error
    try:
        with tracer.trace_skill_execution(skill_id, skill_version, test_input) as span:
            # Simulate execution error
            raise RuntimeError("Simulated execution error")
    except RuntimeError:
        pass

    # Verify error was captured
    recorded_spans = tracer.get_spans()
    assert len(recorded_spans) > 0

    last_span = recorded_spans[-1]
    assert last_span.status == 'error'
    assert 'Simulated execution error' in last_span.error_message


@pytest.mark.integration
def test_execution_history_workflow():
    """Test workflow with execution history tracking."""
    decision_engine = DecisionEngine()

    skill_id = 'historical_skill'

    # Record several successful executions
    for i in range(10):
        decision_engine.record_execution_outcome(
            skill_id=skill_id,
            success=True,
            confidence=0.9
        )

    # Get history
    history = decision_engine.get_execution_history(skill_id)

    assert history is not None
    assert history['total_executions'] == 10
    assert history['successful_executions'] == 10
    assert history['success_rate'] == 1.0

    # Make decision with history
    decision = decision_engine.make_decision(
        skill_id=skill_id,
        confidence=0.75,
        risk_level='Medium',
        validation_passed=True,
        execution_history=history
    )

    # Good history should support auto-execution
    assert decision.type in [DecisionType.AUTO_ACT, DecisionType.FLAG_FOR_REVIEW]


@pytest.mark.integration
def test_poor_history_workflow():
    """Test workflow with poor execution history."""
    decision_engine = DecisionEngine()

    skill_id = 'unreliable_skill'

    # Record mixed execution results (50% success)
    for i in range(10):
        decision_engine.record_execution_outcome(
            skill_id=skill_id,
            success=(i % 2 == 0),
            confidence=0.8
        )

    history = decision_engine.get_execution_history(skill_id)

    assert history['success_rate'] == 0.5

    # Make decision with poor history
    decision = decision_engine.make_decision(
        skill_id=skill_id,
        confidence=0.85,
        risk_level='Medium',
        validation_passed=True,
        execution_history=history
    )

    # Poor history should flag for review
    assert decision.type == DecisionType.FLAG_FOR_REVIEW


@pytest.mark.integration
def test_multi_span_tracing():
    """Test tracing multiple nested skill executions."""
    tracer = SkillTracer(provider='none')

    # Parent workflow
    with tracer.trace_skill_execution('workflow', '1.0.0', {}) as parent:
        # Child skill 1
        with tracer.trace_skill_execution('child1', '1.0.0', {}) as child1:
            child1.set_attribute('step', 1)

        # Child skill 2
        with tracer.trace_skill_execution('child2', '1.0.0', {}) as child2:
            child2.set_attribute('step', 2)

    # Verify all spans recorded
    spans = tracer.get_spans()
    assert len(spans) >= 3

    # Verify nesting
    workflow_span = spans[2]  # Last closed
    assert workflow_span.name == 'skill.workflow'


@pytest.mark.integration
def test_decision_threshold_boundaries():
    """Test decision making at threshold boundaries."""
    decision_engine = DecisionEngine()

    # Test at auto_act threshold (0.85)
    decision = decision_engine.make_decision(
        skill_id='test',
        confidence=0.85,
        risk_level='Low',
        validation_passed=True
    )
    assert decision.type == DecisionType.AUTO_ACT

    # Test just below auto_act threshold
    decision = decision_engine.make_decision(
        skill_id='test',
        confidence=0.84,
        risk_level='Low',
        validation_passed=True
    )
    assert decision.type in [DecisionType.FLAG_FOR_REVIEW, DecisionType.AUTO_ACT]

    # Test at block threshold (0.30)
    decision = decision_engine.make_decision(
        skill_id='test',
        confidence=0.29,
        risk_level='Low',
        validation_passed=True
    )
    assert decision.type == DecisionType.BLOCK
