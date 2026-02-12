"""
Unit tests for eval_harness SkillValidator.
"""

from pathlib import Path

import pytest

from eval_harness.core.validator import SkillValidator, ValidationResult


@pytest.fixture
def validator():
    """Create validator instance."""
    # Use the actual skills library
    return SkillValidator()


def test_validator_initialization(validator):
    """Test validator initializes correctly."""
    assert validator is not None
    assert validator.skills_library_path.exists()


def test_validate_input_valid(validator):
    """Test validation of valid input."""
    # Valid input for mdf_tracker
    input_data = {"partnerId": "test-partner-123", "action": "check_budget"}

    result = validator.validate_input("elg_mdf_tracker", input_data)

    assert result.valid is True
    assert len(result.errors) == 0


def test_validate_input_missing_required_field(validator):
    """Test validation fails when required field is missing."""
    # Missing 'action' field
    input_data = {"partnerId": "test-partner-123"}

    result = validator.validate_input("elg_mdf_tracker", input_data)

    assert result.valid is False
    assert len(result.errors) > 0
    assert any("action" in error.lower() for error in result.errors)


def test_validate_input_invalid_enum_value(validator):
    """Test validation fails for invalid enum value."""
    input_data = {"partnerId": "test-partner-123", "action": "invalid_action"}  # Not in enum

    result = validator.validate_input("elg_mdf_tracker", input_data)

    assert result.valid is False
    assert len(result.errors) > 0


def test_validate_output_valid(validator):
    """Test validation of valid output."""
    output_data = {"available_budget": 10000.0, "allocated": 5000.0, "spent": 2000.0}

    result = validator.validate_output("elg_mdf_tracker", output_data)

    assert result.valid is True
    assert len(result.errors) == 0


def test_validate_output_invalid_type(validator):
    """Test validation fails for wrong type."""
    output_data = {"available_budget": "not-a-number", "allocated": 5000.0}  # Should be number

    result = validator.validate_output("elg_mdf_tracker", output_data)

    assert result.valid is False
    assert len(result.errors) > 0


def test_get_risk_level(validator):
    """Test getting risk level from metadata."""
    risk_level = validator.get_risk_level("elg_mdf_tracker")

    assert risk_level in ["Low", "Medium", "High", "Critical"]
    # mdf_tracker has High risk level
    assert risk_level == "High"


def test_skill_not_found(validator):
    """Test validation fails gracefully for non-existent skill."""
    result = validator.validate_input("nonexistent_skill", {})

    assert result.valid is False
    assert any("not found" in error.lower() for error in result.errors)


def test_validation_result_repr():
    """Test ValidationResult string representation."""
    result = ValidationResult(valid=True)
    assert "✓ VALID" in repr(result)

    result = ValidationResult(valid=False, errors=["Error 1", "Error 2"])
    assert "✗ INVALID" in repr(result)
    assert "Error 1" in repr(result)


def test_validate_chain_compatibility(validator):
    """Test chain compatibility validation."""
    # Test that partner_tier_manager output can feed partner_influenced_revenue
    result = validator.validate_chain_compatibility(
        producer_skill_id="elg_partner_tier_manager",
        consumer_skill_id="elg_partner_influenced_revenue",
        field_mappings={"output.partnerId": "input.partnerId"},
    )

    # Should have validation result (may have warnings about missing fields)
    assert result is not None
    assert isinstance(result, ValidationResult)
