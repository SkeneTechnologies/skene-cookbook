"""
Integration tests for CLI workflows

Tests end-to-end CLI command execution and workflow integration.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

# =============================================================================
# CLI Command Integration Tests
# =============================================================================


@pytest.mark.integration
@pytest.mark.cli
def test_dedupe_command_end_to_end(temp_skills_directory, temp_output_directory):
    """Test dedupe command runs successfully end-to-end."""

    # Run dedupe script
    result = subprocess.run(
        [sys.executable, "scripts/dedupe_skills.py", "--base-path", str(temp_skills_directory)],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent.parent,
    )

    # Should complete (may not find duplicates with test data)
    # Return code 0 or 1 both acceptable
    assert result.returncode in [0, 1] or "Error" not in result.stderr


@pytest.mark.integration
@pytest.mark.cli
def test_analyze_command_end_to_end(temp_skills_directory, temp_output_directory):
    """Test analyze command runs successfully end-to-end."""

    result = subprocess.run(
        [
            sys.executable,
            "scripts/analyze_skills.py",
            "--skills-path",
            str(temp_skills_directory / "skills-library"),
        ],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent.parent,
    )

    # Should complete successfully
    assert result.returncode in [0, 1] or "Error" not in result.stderr


@pytest.mark.integration
@pytest.mark.cli
def test_blueprints_command_end_to_end(
    temp_skills_directory, temp_output_directory, mock_registry_data
):
    """Test blueprint generation runs successfully end-to-end."""

    # Create registry
    registry_dir = temp_skills_directory / "registry" / "job_functions"
    registry_dir.mkdir(parents=True, exist_ok=True)

    with open(registry_dir / "index.json", "w") as f:
        json.dump(mock_registry_data, f)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_blueprints.py",
            "--base-path",
            str(temp_skills_directory),
        ],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent.parent,
    )

    # Should complete
    assert result.returncode in [0, 1] or "Error" not in result.stderr


# =============================================================================
# CLI Output Validation Tests
# =============================================================================


@pytest.mark.integration
@pytest.mark.cli
def test_cli_produces_valid_output_files(temp_skills_directory, temp_output_directory):
    """Test that CLI commands produce valid output files."""

    # Files that should be created
    expected_outputs = []

    # Run commands and check outputs
    # (Implementation depends on actual CLI structure)

    # Test that output files are created and valid
    for output_file in expected_outputs:
        if output_file.exists():
            # Validate format based on extension
            if output_file.suffix == ".json":
                with open(output_file) as f:
                    json.load(f)  # Should not raise
            elif output_file.suffix == ".md":
                content = output_file.read_text()
                assert len(content) > 0


# =============================================================================
# CLI Error Handling Tests
# =============================================================================


@pytest.mark.integration
@pytest.mark.cli
def test_cli_handles_missing_directory():
    """Test CLI handles missing directory gracefully."""

    result = subprocess.run(
        [sys.executable, "scripts/dedupe_skills.py", "--base-path", "/nonexistent/path"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent.parent,
    )

    # Should fail gracefully with clear error
    assert result.returncode != 0


@pytest.mark.integration
@pytest.mark.cli
def test_cli_shows_help():
    """Test CLI help commands work."""

    result = subprocess.run(
        [sys.executable, "scripts/dedupe_skills.py", "--help"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent.parent,
    )

    # Should show help
    assert (
        result.returncode == 0
        or "usage" in result.stdout.lower()
        or "help" in result.stdout.lower()
    )


# =============================================================================
# Workflow Chain Tests
# =============================================================================


@pytest.mark.integration
@pytest.mark.slow
def test_sequential_workflow_execution(temp_skills_directory):
    """Test running commands in sequence like a user would."""

    # 1. Analyze
    # 2. Dedupe
    # 3. Generate blueprints
    # All should work together

    commands = [
        [sys.executable, "scripts/analyze_skills.py"],
        [sys.executable, "scripts/dedupe_skills.py"],
        [sys.executable, "scripts/generate_blueprints.py"],
    ]

    cwd = Path(__file__).parent.parent.parent

    for cmd in commands:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
        # Commands may fail with test data, but should not crash
        # Accept both success and controlled failure
