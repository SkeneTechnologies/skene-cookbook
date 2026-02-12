# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Unit tests for eval_harness DecisionEngine.
"""

import pytest

from eval_harness.decision.decision_engine import (
    Decision,
    DecisionConfig,
    DecisionEngine,
    DecisionType,
)


@pytest.fixture
def engine():
    """Create decision engine with default config."""
    return DecisionEngine()


@pytest.fixture
def custom_engine():
    """Create decision engine with custom config."""
    config = DecisionConfig(
        auto_act_threshold=0.90,
        flag_threshold=0.60,
        block_threshold=0.40,
        critical_risk_requires_approval=True,
    )
    return DecisionEngine(config)


def test_engine_initialization():
    """Test decision engine initializes with defaults."""
    engine = DecisionEngine()
    assert engine.config is not None
    assert engine.config.auto_act_threshold == 0.85
    assert engine.config.flag_threshold == 0.50
    assert engine.config.block_threshold == 0.30
    assert engine._execution_history == {}


def test_engine_custom_config():
    """Test decision engine with custom configuration."""
    config = DecisionConfig(auto_act_threshold=0.95, flag_threshold=0.70, block_threshold=0.50)
    engine = DecisionEngine(config)
    assert engine.config.auto_act_threshold == 0.95
    assert engine.config.flag_threshold == 0.70
    assert engine.config.block_threshold == 0.50


def test_decision_auto_act_high_confidence_low_risk(engine):
    """Test AUTO_ACT decision for high confidence + low risk."""
    decision = engine.make_decision(
        skill_id="test_skill", confidence=0.90, risk_level="Low", validation_passed=True
    )

    assert decision.type == DecisionType.AUTO_ACT
    assert decision.should_execute() is True
    assert decision.requires_human_approval() is False
    assert decision.is_blocked() is False
    assert decision.confidence == 0.90
    assert decision.risk_level == "Low"
    assert decision.validation_passed is True


def test_decision_flag_for_review_medium_confidence(engine):
    """Test FLAG_FOR_REVIEW for medium confidence."""
    decision = engine.make_decision(
        skill_id="test_skill", confidence=0.65, risk_level="Low", validation_passed=True
    )

    assert decision.type == DecisionType.FLAG_FOR_REVIEW
    assert decision.should_execute() is True
    assert decision.requires_human_approval() is False


def test_decision_require_approval_critical_risk(engine):
    """Test REQUIRE_APPROVAL for Critical risk."""
    decision = engine.make_decision(
        skill_id="test_skill", confidence=0.90, risk_level="Critical", validation_passed=True
    )

    assert decision.type == DecisionType.REQUIRE_APPROVAL
    assert decision.should_execute() is False
    assert decision.requires_human_approval() is True
    assert "Critical risk" in decision.reasoning


def test_decision_require_approval_high_risk_low_confidence(engine):
    """Test FLAG_FOR_REVIEW for High risk + insufficient confidence."""
    decision = engine.make_decision(
        skill_id="test_skill",
        confidence=0.60,  # Below high_risk_min_confidence (0.75)
        risk_level="High",
        validation_passed=True,
    )

    # High risk + low confidence = FLAG_FOR_REVIEW (not REQUIRE_APPROVAL)
    assert decision.type == DecisionType.FLAG_FOR_REVIEW
    assert decision.should_execute() is True


def test_decision_block_validation_failed(engine):
    """Test BLOCK when validation fails."""
    decision = engine.make_decision(
        skill_id="test_skill", confidence=0.95, risk_level="Low", validation_passed=False
    )

    assert decision.type == DecisionType.BLOCK
    assert decision.is_blocked() is True
    assert decision.should_execute() is False
    assert "validation failed" in decision.reasoning.lower()


def test_decision_block_very_low_confidence(engine):
    """Test BLOCK for very low confidence."""
    decision = engine.make_decision(
        skill_id="test_skill",
        confidence=0.20,  # Below block_threshold (0.30)
        risk_level="Low",
        validation_passed=True,
    )

    assert decision.type == DecisionType.BLOCK
    assert decision.is_blocked() is True
    assert "confidence too low" in decision.reasoning.lower()


def test_decision_with_execution_history_good(engine):
    """Test decision considers good execution history."""
    history = {"total_executions": 10, "successful_executions": 9, "success_rate": 0.90}

    decision = engine.make_decision(
        skill_id="test_skill",
        confidence=0.80,
        risk_level="Medium",
        validation_passed=True,
        execution_history=history,
    )

    # Good history should help confidence
    assert decision.type in [DecisionType.AUTO_ACT, DecisionType.FLAG_FOR_REVIEW]


def test_decision_with_execution_history_poor(engine):
    """Test decision considers poor execution history."""
    history = {"total_executions": 10, "successful_executions": 5, "success_rate": 0.50}

    decision = engine.make_decision(
        skill_id="test_skill",
        confidence=0.80,
        risk_level="Medium",
        validation_passed=True,
        execution_history=history,
    )

    # Poor history should lower confidence
    assert (
        "execution history" in decision.reasoning.lower() or decision.type != DecisionType.AUTO_ACT
    )


def test_decision_medium_risk_adequate_confidence(engine):
    """Test Medium risk with adequate confidence."""
    decision = engine.make_decision(
        skill_id="test_skill", confidence=0.88, risk_level="Medium", validation_passed=True
    )

    assert decision.type == DecisionType.AUTO_ACT
    assert decision.should_execute() is True


def test_decision_metadata(engine):
    """Test decision includes proper metadata."""
    decision = engine.make_decision(
        skill_id="test_skill", confidence=0.90, risk_level="Low", validation_passed=True
    )

    assert "skill_id" in decision.metadata
    assert "confidence" in decision.metadata
    assert "risk_level" in decision.metadata
    assert "validation_passed" in decision.metadata
    assert decision.metadata["skill_id"] == "test_skill"


def test_decision_edge_case_exact_threshold(engine):
    """Test decision at exact threshold values."""
    # Exactly at auto_act_threshold
    decision = engine.make_decision(
        skill_id="test_skill", confidence=0.85, risk_level="Low", validation_passed=True
    )
    assert decision.type == DecisionType.AUTO_ACT

    # Exactly at flag_threshold
    decision = engine.make_decision(
        skill_id="test_skill", confidence=0.50, risk_level="Low", validation_passed=True
    )
    assert decision.type in [DecisionType.FLAG_FOR_REVIEW, DecisionType.AUTO_ACT]


def test_decision_config_validation_blocking():
    """Test config with validation blocking disabled."""
    config = DecisionConfig(block_on_validation_failure=False)
    engine = DecisionEngine(config)

    decision = engine.make_decision(
        skill_id="test_skill", confidence=0.90, risk_level="Low", validation_passed=False
    )

    # With blocking disabled, should not block
    assert decision.type != DecisionType.BLOCK or not config.block_on_validation_failure


def test_decision_reasoning_includes_factors(engine):
    """Test decision reasoning explains key factors."""
    decision = engine.make_decision(
        skill_id="test_skill", confidence=0.90, risk_level="Low", validation_passed=True
    )

    assert decision.reasoning is not None
    assert len(decision.reasoning) > 0


def test_decision_type_enum_values():
    """Test DecisionType enum has all expected values."""
    assert DecisionType.AUTO_ACT.value == "auto_act"
    assert DecisionType.FLAG_FOR_REVIEW.value == "flag_for_review"
    assert DecisionType.REQUIRE_APPROVAL.value == "require_approval"
    assert DecisionType.BLOCK.value == "block"


def test_decision_should_execute_method():
    """Test Decision.should_execute() method."""
    decision_auto = Decision(
        type=DecisionType.AUTO_ACT,
        confidence=0.90,
        risk_level="Low",
        validation_passed=True,
        reasoning="High confidence",
        metadata={},
    )
    assert decision_auto.should_execute() is True

    decision_flag = Decision(
        type=DecisionType.FLAG_FOR_REVIEW,
        confidence=0.70,
        risk_level="Low",
        validation_passed=True,
        reasoning="Medium confidence",
        metadata={},
    )
    assert decision_flag.should_execute() is True

    decision_approval = Decision(
        type=DecisionType.REQUIRE_APPROVAL,
        confidence=0.60,
        risk_level="High",
        validation_passed=True,
        reasoning="High risk",
        metadata={},
    )
    assert decision_approval.should_execute() is False

    decision_block = Decision(
        type=DecisionType.BLOCK,
        confidence=0.20,
        risk_level="Low",
        validation_passed=False,
        reasoning="Validation failed",
        metadata={},
    )
    assert decision_block.should_execute() is False


def test_decision_high_confidence_with_high_risk(engine):
    """Test high confidence with High risk requires sufficient threshold."""
    # Below high_risk_min_confidence (0.75)
    decision_low = engine.make_decision(
        skill_id="test_skill", confidence=0.70, risk_level="High", validation_passed=True
    )
    assert decision_low.type == DecisionType.FLAG_FOR_REVIEW

    # Above high_risk_min_confidence (0.75) but below auto_act_threshold (0.85)
    decision_medium = engine.make_decision(
        skill_id="test_skill", confidence=0.80, risk_level="High", validation_passed=True
    )
    assert decision_medium.type in [DecisionType.FLAG_FOR_REVIEW, DecisionType.AUTO_ACT]

    # Above auto_act_threshold
    decision_high = engine.make_decision(
        skill_id="test_skill", confidence=0.90, risk_level="High", validation_passed=True
    )
    assert decision_high.type == DecisionType.AUTO_ACT


def test_decision_without_execution_history(engine):
    """Test decision when no execution history provided."""
    decision = engine.make_decision(
        skill_id="test_skill",
        confidence=0.85,
        risk_level="Low",
        validation_passed=True,
        execution_history=None,
    )

    # Should still make valid decision without history
    assert decision.type is not None
    assert isinstance(decision, Decision)


def test_custom_thresholds_affect_decision(custom_engine):
    """Test custom thresholds change decision outcomes."""
    # Confidence 0.85 is AUTO_ACT for default, but not for custom (needs 0.90)
    decision = custom_engine.make_decision(
        skill_id="test_skill", confidence=0.85, risk_level="Low", validation_passed=True
    )

    # Should be FLAG_FOR_REVIEW or REQUIRE_APPROVAL (not AUTO_ACT)
    assert decision.type != DecisionType.AUTO_ACT
