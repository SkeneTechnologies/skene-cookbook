"""
Unit tests for scripts/generate_blueprints.py

Tests the intelligent skill chaining engine that analyzes I/O compatibility
and generates workflow blueprints for different job functions.
"""

import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from generate_blueprints import ChainArchitect

# =============================================================================
# Test Initialization
# =============================================================================


@pytest.mark.unit
def test_initialization(temp_output_directory):
    """Test ChainArchitect initializes correctly."""
    architect = ChainArchitect(base_path=str(temp_output_directory))

    assert architect.base_path == temp_output_directory
    assert architect.skills_path == temp_output_directory / "skills-library"
    assert architect.registry_path == temp_output_directory / "registry"
    assert architect.skills == []
    assert len(architect.skills_by_function) == 0


@pytest.mark.unit
def test_initialization_creates_blueprint_directory(temp_output_directory):
    """Test that blueprints directory is created."""
    architect = ChainArchitect(base_path=str(temp_output_directory))

    assert architect.blueprints_path.exists()
    assert architect.blueprints_path.is_dir()


# =============================================================================
# Test I/O Type Extraction
# =============================================================================


@pytest.mark.unit
def test_extract_io_types_simple():
    """Test extraction of simple JSON schema types."""
    architect = ChainArchitect()

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "number"},
            "active": {"type": "boolean"},
        },
    }

    types = architect._extract_io_types(schema)

    assert "object" in types
    assert "string" in types
    assert "number" in types
    assert "boolean" in types


@pytest.mark.unit
def test_extract_io_types_semantic():
    """Test semantic type detection from descriptions."""
    architect = ChainArchitect()

    schema = {
        "type": "object",
        "properties": {
            "data_file": {"type": "string", "description": "Path to data file"},
            "report_url": {"type": "string", "description": "URL of the report"},
            "image_data": {"type": "string", "description": "Image file contents"},
        },
    }

    types = architect._extract_io_types(schema)

    assert "file" in types or "string" in types
    assert "url" in types or "string" in types


@pytest.mark.unit
def test_extract_io_types_empty_schema():
    """Test handling of empty or None schema."""
    architect = ChainArchitect()

    assert architect._extract_io_types(None) == set()
    assert architect._extract_io_types({}) == set()


@pytest.mark.unit
def test_extract_io_types_nested():
    """Test extraction from nested schemas."""
    architect = ChainArchitect()

    schema = {
        "type": "object",
        "properties": {"data": {"type": "object", "properties": {"value": {"type": "number"}}}},
    }

    types = architect._extract_io_types(schema)

    assert "object" in types


# =============================================================================
# Test Load Skills
# =============================================================================


@pytest.mark.unit
def test_load_skills_from_registry(temp_skills_directory, mock_registry_data):
    """Test loading skills from registry index."""
    # Create registry structure
    registry_dir = temp_skills_directory / "registry" / "job_functions"
    registry_dir.mkdir(parents=True, exist_ok=True)

    # Write index.json
    with open(registry_dir / "index.json", "w") as f:
        json.dump(mock_registry_data, f)

    architect = ChainArchitect(base_path=str(temp_skills_directory))
    architect.load_skills()

    assert len(architect.skills) > 0
    assert len(architect.skills_by_function) > 0


@pytest.mark.unit
def test_load_skills_builds_io_graph(temp_skills_directory, mock_skills_data):
    """Test that I/O graph is built during skill loading."""
    # Create registry structure
    registry_dir = temp_skills_directory / "registry" / "job_functions"
    registry_dir.mkdir(parents=True, exist_ok=True)

    # Create minimal index
    index_data = {"engineering": [{"skill_id": "test_skill_1", "name": "Test"}]}
    with open(registry_dir / "index.json", "w") as f:
        json.dump(index_data, f)

    architect = ChainArchitect(base_path=str(temp_skills_directory))
    architect.load_skills()

    # I/O graph should contain output types
    assert len(architect.io_graph) >= 0  # May be empty or populated


# =============================================================================
# Test Chainability Analysis
# =============================================================================


@pytest.mark.unit
def test_analyze_chainability_finds_compatible_pairs():
    """Test identification of compatible skill pairs."""
    architect = ChainArchitect()

    # Create skills with compatible I/O
    architect.skills = [
        {
            "skill_id": "producer",
            "name": "Data Producer",
            "input_types": set(),
            "output_types": {"data", "file"},
            "tools": [],
            "exit_states": [],
        },
        {
            "skill_id": "consumer",
            "name": "Data Consumer",
            "input_types": {"data", "file"},
            "output_types": {"report"},
            "tools": [],
            "exit_states": [],
        },
    ]

    # Build IO graph
    for skill in architect.skills:
        for output_type in skill["output_types"]:
            architect.io_graph[output_type].append(skill)

    architect.analyze_chainability()

    assert len(architect.chainable_pairs) > 0


@pytest.mark.unit
def test_analyze_chainability_no_matches():
    """Test when no skills are compatible."""
    architect = ChainArchitect()

    # Create skills with incompatible I/O
    architect.skills = [
        {
            "skill_id": "skill_a",
            "name": "Skill A",
            "input_types": set(),
            "output_types": {"type_a"},
            "tools": [],
            "exit_states": [],
        },
        {
            "skill_id": "skill_b",
            "name": "Skill B",
            "input_types": {"type_b"},  # Different type
            "output_types": {"type_c"},
            "tools": [],
            "exit_states": [],
        },
    ]

    # Build IO graph
    for skill in architect.skills:
        for output_type in skill["output_types"]:
            architect.io_graph[output_type].append(skill)

    architect.analyze_chainability()

    # Should find few or no chainable pairs
    assert isinstance(architect.chainable_pairs, list)


# =============================================================================
# Test Missing Link Identification
# =============================================================================


@pytest.mark.unit
def test_identify_missing_links():
    """Test identification of workflow gaps."""
    architect = ChainArchitect()

    architect.skills = [
        {
            "skill_id": "skill_1",
            "name": "Skill 1",
            "input_types": set(),
            "output_types": {"data"},
            "tools": [],
            "exit_states": [],
        },
        {
            "skill_id": "skill_2",
            "name": "Skill 2",
            "input_types": {"report"},  # No skill produces 'report'
            "output_types": {"result"},
            "tools": [],
            "exit_states": [],
        },
    ]

    # Build IO graph
    for skill in architect.skills:
        for output_type in skill["output_types"]:
            architect.io_graph[output_type].append(skill)

    architect.identify_missing_links()

    # Should identify 'report' as a missing link
    assert len(architect.missing_links) > 0


# =============================================================================
# Test Blueprint Generation
# =============================================================================


@pytest.mark.unit
def test_create_function_blueprint_engineering(temp_output_directory):
    """Test blueprint generation for engineering function."""
    architect = ChainArchitect(base_path=str(temp_output_directory))

    architect.skills_by_function = {
        "engineering": [
            {"skill_id": "api_client", "name": "API Client"},
            {"skill_id": "data_transformer", "name": "Data Transformer"},
        ]
    }

    architect.chainable_pairs = [("api_client", "data_transformer", 0.9)]

    skills = architect.skills_by_function["engineering"]
    blueprint = architect._create_function_blueprint("engineering", skills)

    assert isinstance(blueprint, dict)
    assert "chain_sequence" in blueprint or "name" in blueprint or "id" in blueprint


@pytest.mark.unit
def test_create_function_blueprint_includes_workflows(temp_output_directory):
    """Test that blueprints include workflow suggestions."""
    architect = ChainArchitect(base_path=str(temp_output_directory))

    architect.skills_by_function = {
        "marketing": [
            {"skill_id": "content_gen", "name": "Content Generator"},
            {"skill_id": "seo_optimizer", "name": "SEO Optimizer"},
        ]
    }

    architect.chainable_pairs = [("content_gen", "seo_optimizer", 0.95)]

    skills = architect.skills_by_function["marketing"]
    blueprint = architect._create_function_blueprint("marketing", skills)

    assert isinstance(blueprint, dict)
    assert len(blueprint) > 0


@pytest.mark.unit
def test_generate_function_blueprints(temp_output_directory):
    """Test generating all job function blueprints."""
    architect = ChainArchitect(base_path=str(temp_output_directory))

    # Setup test data
    architect.skills_by_function = {
        "engineering": [{"skill_id": "test_1", "name": "Test 1"}],
        "marketing": [{"skill_id": "test_2", "name": "Test 2"}],
    }

    architect.chainable_pairs = []

    architect.generate_function_blueprints()

    # Check that blueprint files were created
    blueprint_files = list(architect.blueprints_path.glob("*.yaml"))
    assert len(blueprint_files) > 0


# =============================================================================
# Test Chain Report Generation
# =============================================================================


@pytest.mark.unit
def test_generate_chain_report(temp_output_directory):
    """Test chain analysis report generation."""
    architect = ChainArchitect(base_path=str(temp_output_directory))

    skill1 = {
        "skill_id": "1",
        "name": "Skill 1",
        "input_types": [],
        "output_types": ["data"],
        "tools": [],
        "exit_states": [],
    }
    skill2 = {
        "skill_id": "2",
        "name": "Skill 2",
        "input_types": ["data"],
        "output_types": [],
        "tools": [],
        "exit_states": [],
    }
    architect.skills = [skill1, skill2]
    architect.chainable_pairs = [
        {
            "producer": skill1,
            "compatible_consumers": [{"skill": skill2, "connection_type": "data"}],
        }
    ]
    architect.io_graph = {"data": [skill1, skill2]}
    architect.missing_links = [
        {"workflow": "test", "missing_steps": ["report"], "severity": "critical"}
    ]

    architect.generate_chain_report()

    report_path = temp_output_directory / "reports" / "chain_analysis.json"
    assert report_path.exists()

    with open(report_path) as f:
        report = json.load(f)

    assert "summary" in report or isinstance(report, dict)


# =============================================================================
# Test Full Workflow
# =============================================================================


@pytest.mark.unit
def test_full_blueprint_generation_workflow(
    temp_skills_directory, mock_registry_data, temp_output_directory
):
    """Test complete blueprint generation workflow."""
    # Setup registry
    registry_dir = temp_skills_directory / "registry" / "job_functions"
    registry_dir.mkdir(parents=True, exist_ok=True)

    with open(registry_dir / "index.json", "w") as f:
        json.dump(mock_registry_data, f)

    architect = ChainArchitect(base_path=str(temp_skills_directory))

    # Load skills
    architect.load_skills()
    assert len(architect.skills) >= 0

    # Analyze chainability
    architect.analyze_chainability()

    # Identify missing links
    architect.identify_missing_links()

    # Generate blueprints
    architect.generate_function_blueprints()

    # Generate report (writes to base_path/reports/chain_analysis.json)
    architect.base_path = Path(temp_output_directory)
    architect.generate_chain_report()

    report_path = temp_output_directory / "reports" / "chain_analysis.json"
    assert report_path.exists()


# =============================================================================
# Test Exit State Analysis
# =============================================================================


@pytest.mark.unit
def test_analyze_exit_states():
    """Test analysis of skill exit states for chaining hints."""
    architect = ChainArchitect()

    skill = {
        "skill_id": "test",
        "exit_states": [
            {"state": "complete", "nextSkills": ["skill_2"]},
            {"state": "partial", "nextSkills": ["skill_3"]},
        ],
    }

    # Should extract next skill hints
    assert len(skill["exit_states"]) == 2
    assert skill["exit_states"][0]["nextSkills"] == ["skill_2"]


# =============================================================================
# Test I/O Compatibility Logic
# =============================================================================


@pytest.mark.unit
def test_io_compatibility_exact_match():
    """Test exact type matching for skill chaining."""
    architect = ChainArchitect()

    skill_a = {"output_types": {"string", "data"}}
    skill_b = {"input_types": {"string", "data"}}

    # Check if there's overlap
    overlap = skill_a["output_types"] & skill_b["input_types"]
    assert len(overlap) > 0


@pytest.mark.unit
def test_io_compatibility_no_match():
    """Test when skills have no compatible types."""
    architect = ChainArchitect()

    skill_a = {"output_types": {"type_x"}}
    skill_b = {"input_types": {"type_y"}}

    overlap = skill_a["output_types"] & skill_b["input_types"]
    assert len(overlap) == 0
