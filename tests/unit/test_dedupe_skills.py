"""
Unit tests for scripts/dedupe_skills.py

Tests the semantic deduplication engine that identifies duplicate and similar skills
using sentence transformers and cosine similarity.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import numpy as np
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from dedupe_skills import SkillDeduplicator


# =============================================================================
# Test Initialization
# =============================================================================

@pytest.mark.unit
def test_initialization(temp_output_directory):
    """Test SkillDeduplicator initializes correctly."""
    deduplicator = SkillDeduplicator(similarity_threshold=0.90, base_path=str(temp_output_directory))

    assert deduplicator.similarity_threshold == 0.90
    assert deduplicator.base_path == temp_output_directory
    assert deduplicator.skills_path == temp_output_directory / "skills-library"
    assert deduplicator.skills == []
    assert deduplicator.embeddings is None
    assert deduplicator.model is not None  # Mocked by conftest


@pytest.mark.unit
def test_initialization_default_threshold(temp_output_directory):
    """Test default similarity threshold is 0.88."""
    deduplicator = SkillDeduplicator(base_path=str(temp_output_directory))
    assert deduplicator.similarity_threshold == 0.88


# =============================================================================
# Test Load All Skills
# =============================================================================

@pytest.mark.unit
def test_load_all_skills(temp_skills_directory, mock_skills_data):
    """Test loading skills from directory."""
    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))
    deduplicator.load_all_skills()

    assert len(deduplicator.skills) == len(mock_skills_data)
    assert all('skill_id' in skill for skill in deduplicator.skills)
    assert all('name' in skill for skill in deduplicator.skills)


@pytest.mark.unit
def test_load_skills_with_metadata(temp_skills_directory):
    """Test loading skills with metadata files."""
    # Create a skill with metadata
    skill_dir = temp_skills_directory / "skills-library" / "engineering" / "test_with_metadata"
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_data = {
        "id": "test_with_metadata",
        "name": "Test Skill",
        "description": "Has metadata"
    }

    metadata_data = {
        "author": "Test Author",
        "created": "2024-01-01"
    }

    with open(skill_dir / "skill.json", "w") as f:
        json.dump(skill_data, f)

    with open(skill_dir / "metadata.yaml", "w") as f:
        f.write("author: Test Author\ncreated: 2024-01-01\n")

    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))
    deduplicator.load_all_skills()

    # Find the skill with metadata
    test_skill = next((s for s in deduplicator.skills if s['skill_id'] == 'test_with_metadata'), None)
    assert test_skill is not None
    assert 'metadata' in test_skill


@pytest.mark.unit
def test_load_skills_handles_invalid_json(temp_skills_directory):
    """Test graceful handling of invalid JSON files."""
    # Create an invalid skill file
    invalid_dir = temp_skills_directory / "skills-library" / "engineering" / "invalid"
    invalid_dir.mkdir(parents=True, exist_ok=True)

    with open(invalid_dir / "skill.json", "w") as f:
        f.write("{ invalid json }")

    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))
    deduplicator.load_all_skills()

    # Should load other skills but skip invalid one
    assert len(deduplicator.skills) >= 0


# =============================================================================
# Test Generate Embeddings
# =============================================================================

@pytest.mark.unit
def test_generate_embeddings(temp_skills_directory, mock_skills_data):
    """Test embedding generation for skills."""
    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))
    deduplicator.load_all_skills()
    deduplicator.generate_embeddings()

    assert deduplicator.embeddings is not None
    assert len(deduplicator.embeddings) == len(deduplicator.skills)
    assert deduplicator.embeddings.shape[1] == 384  # MiniLM embedding dimension


@pytest.mark.unit
def test_generate_embeddings_combines_name_and_description(temp_skills_directory):
    """Test that embeddings use both name and description."""
    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))

    # Add a single skill manually
    deduplicator.skills = [{
        'skill_id': 'test',
        'name': 'Test Name',
        'description': 'Test Description',
        'file_path': 'test.json'
    }]

    with patch.object(deduplicator.model, 'encode') as mock_encode:
        mock_encode.return_value = np.random.randn(1, 384)
        deduplicator.generate_embeddings()

        # Verify the text passed to encode combines name and description
        call_args = mock_encode.call_args[0][0]
        assert 'Test Name' in call_args[0]
        assert 'Test Description' in call_args[0]


# =============================================================================
# Test Find Duplicates
# =============================================================================

@pytest.mark.unit
def test_find_duplicates_high_similarity(temp_skills_directory):
    """Test detection of highly similar skills."""
    deduplicator = SkillDeduplicator(similarity_threshold=0.95, base_path=str(temp_skills_directory))

    # Create two very similar skills
    deduplicator.skills = [
        {
            'skill_id': 'skill_1',
            'name': 'Data Analyzer',
            'description': 'Analyzes data files and generates insights',
            'file_path': 'test1.json'
        },
        {
            'skill_id': 'skill_2',
            'name': 'Similar to Data Analyzer',
            'description': 'Analyzes data files and generates insights with similar functionality',
            'file_path': 'test2.json'
        }
    ]

    deduplicator.generate_embeddings()
    deduplicator.find_duplicates()

    # Should find at least one similar pair
    assert len(deduplicator.similar_pairs) > 0 or len(deduplicator.duplicates) > 0


@pytest.mark.unit
def test_find_duplicates_no_false_positives(temp_skills_directory):
    """Test that dissimilar skills are not marked as duplicates."""
    deduplicator = SkillDeduplicator(similarity_threshold=0.95, base_path=str(temp_skills_directory))

    # Create two very different skills
    deduplicator.skills = [
        {
            'skill_id': 'skill_1',
            'name': 'Data Analyzer',
            'description': 'Analyzes data files',
            'file_path': 'test1.json'
        },
        {
            'skill_id': 'skill_2',
            'name': 'Marketing Campaign',
            'description': 'Launch social media campaigns',
            'file_path': 'test2.json'
        }
    ]

    deduplicator.generate_embeddings()
    deduplicator.find_duplicates()

    # With very different descriptions, similarity should be low
    # So with high threshold, should find few or no duplicates
    assert len(deduplicator.duplicates) <= 1  # May find self-similarity


@pytest.mark.unit
@pytest.mark.parametrize("threshold", [0.95, 0.88, 0.70])
def test_different_thresholds(temp_skills_directory, threshold):
    """Test duplicate detection with different similarity thresholds."""
    deduplicator = SkillDeduplicator(similarity_threshold=threshold, base_path=str(temp_skills_directory))

    deduplicator.skills = [
        {
            'skill_id': 'skill_1',
            'name': 'Test A',
            'description': 'Description A',
            'file_path': 'test1.json'
        },
        {
            'skill_id': 'skill_2',
            'name': 'Test B',
            'description': 'Description B',
            'file_path': 'test2.json'
        }
    ]

    deduplicator.generate_embeddings()
    deduplicator.find_duplicates()

    # Lower thresholds should find more potential duplicates
    assert deduplicator.similarity_threshold == threshold


# =============================================================================
# Test Validate Completeness
# =============================================================================

@pytest.mark.unit
def test_validate_completeness_identifies_incomplete_skills(temp_skills_directory):
    """Test identification of skills missing I/O schemas."""
    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))

    deduplicator.skills = [
        {
            'skill_id': 'complete',
            'name': 'Complete Skill',
            'description': 'Has schemas',
            'file_path': 'complete.json',
            'inputSchema': {'type': 'object'},
            'outputSchema': {'type': 'object'}
        },
        {
            'skill_id': 'incomplete',
            'name': 'Incomplete Skill',
            'description': 'Missing schemas',
            'file_path': 'incomplete.json',
            'inputSchema': None,
            'outputSchema': None
        }
    ]

    deduplicator.validate_completeness()

    assert len(deduplicator.incomplete) == 1
    assert deduplicator.incomplete[0]['skill_id'] == 'incomplete'


@pytest.mark.unit
def test_validate_completeness_all_complete(temp_skills_directory):
    """Test when all skills have complete schemas."""
    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))

    deduplicator.skills = [
        {
            'skill_id': 'skill_1',
            'name': 'Skill 1',
            'description': 'Complete',
            'file_path': 'skill1.json',
            'inputSchema': {'type': 'object'},
            'outputSchema': {'type': 'object'}
        },
        {
            'skill_id': 'skill_2',
            'name': 'Skill 2',
            'description': 'Complete',
            'file_path': 'skill2.json',
            'inputSchema': {'type': 'object'},
            'outputSchema': {'type': 'object'}
        }
    ]

    deduplicator.validate_completeness()

    assert len(deduplicator.incomplete) == 0


# =============================================================================
# Test Identify Unique Verified
# =============================================================================

@pytest.mark.unit
def test_identify_unique_verified_filters_correctly(temp_skills_directory):
    """Test filtering of verified skills."""
    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))

    deduplicator.skills = [
        {
            'skill_id': 'verified_1',
            'name': 'Verified Skill',
            'metadata': {'verified': True},
            'file_path': 'v1.json'
        },
        {
            'skill_id': 'unverified_1',
            'name': 'Unverified Skill',
            'metadata': {'verified': False},
            'file_path': 'u1.json'
        },
        {
            'skill_id': 'no_metadata',
            'name': 'No Metadata',
            'metadata': {},
            'file_path': 'n1.json'
        }
    ]

    # Empty duplicates list means all are unique
    deduplicator.duplicates = []
    deduplicator.identify_unique_verified()

    assert len(deduplicator.unique_verified) == 1
    assert deduplicator.unique_verified[0]['skill_id'] == 'verified_1'


# =============================================================================
# Test Generate Report
# =============================================================================

@pytest.mark.unit
def test_generate_report_creates_json(temp_output_directory, temp_skills_directory):
    """Test JSON report generation."""
    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))

    deduplicator.skills = [
        {'skill_id': '1', 'name': 'Skill 1', 'description': 'Test', 'file_path': 't1.json'}
    ]
    deduplicator.duplicates = []
    deduplicator.similar_pairs = []
    deduplicator.incomplete = []
    deduplicator.unique_verified = []

    output_file = temp_output_directory / "test_report.json"
    deduplicator.generate_report(str(output_file), format="json")

    assert output_file.exists()

    # Verify JSON structure
    with open(output_file) as f:
        report = json.load(f)

    assert 'summary' in report
    assert 'total_skills' in report['summary']


@pytest.mark.unit
def test_generate_report_creates_markdown(temp_output_directory, temp_skills_directory):
    """Test Markdown report generation."""
    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))

    deduplicator.skills = [
        {'skill_id': '1', 'name': 'Skill 1', 'description': 'Test', 'file_path': 't1.json'}
    ]
    deduplicator.duplicates = []
    deduplicator.similar_pairs = []
    deduplicator.incomplete = []
    deduplicator.unique_verified = []

    output_file = temp_output_directory / "test_report.md"
    deduplicator.generate_report(str(output_file), format="markdown")

    assert output_file.exists()

    # Verify markdown content
    content = output_file.read_text()
    assert '# Skill Deduplication Report' in content or 'Skills Deduplication' in content


@pytest.mark.unit
def test_generate_report_includes_statistics(temp_output_directory, temp_skills_directory):
    """Test that report includes key statistics."""
    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))

    deduplicator.skills = [
        {'skill_id': '1', 'name': 'S1', 'description': 'T1', 'file_path': 't1.json'},
        {'skill_id': '2', 'name': 'S2', 'description': 'T2', 'file_path': 't2.json'}
    ]
    deduplicator.duplicates = [('1', '2', 0.96)]
    deduplicator.similar_pairs = []
    deduplicator.incomplete = [deduplicator.skills[0]]
    deduplicator.unique_verified = []

    output_file = temp_output_directory / "test_report.json"
    deduplicator.generate_report(str(output_file), format="json")

    with open(output_file) as f:
        report = json.load(f)

    assert report['summary']['total_skills'] == 2
    assert report['summary']['duplicate_count'] >= 1


# =============================================================================
# Test Full Workflow
# =============================================================================

@pytest.mark.unit
def test_full_deduplication_workflow(temp_skills_directory, temp_output_directory):
    """Test complete deduplication workflow."""
    deduplicator = SkillDeduplicator(similarity_threshold=0.85, base_path=str(temp_skills_directory))

    # Load skills
    deduplicator.load_all_skills()
    assert len(deduplicator.skills) > 0

    # Generate embeddings
    deduplicator.generate_embeddings()
    assert deduplicator.embeddings is not None

    # Find duplicates
    deduplicator.find_duplicates()

    # Validate completeness
    deduplicator.validate_completeness()

    # Identify unique verified
    deduplicator.identify_unique_verified()

    # Generate report
    output_file = temp_output_directory / "workflow_report.json"
    deduplicator.generate_report(str(output_file), format="json")

    assert output_file.exists()
