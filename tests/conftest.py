"""
Shared fixtures and configuration for the test suite.

This module provides:
- Mock sentence-transformers model (prevents 500MB+ loading)
- Mock Rich console output
- Temporary directory fixtures
- Sample skills data
"""

import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import numpy as np
import pytest


# =============================================================================
# Mock Sentence Transformers (Critical - Prevents Heavy ML Model Loading)
# =============================================================================

@pytest.fixture(autouse=True)
def mock_sentence_transformer(monkeypatch):
    """
    Mock sentence-transformers to avoid loading 500MB+ model.
    Returns deterministic numpy arrays for testing.
    """
    class MockSentenceTransformer:
        def __init__(self, *args, **kwargs):
            pass

        def encode(self, texts, **kwargs):
            """Return deterministic embeddings based on text content."""
            if isinstance(texts, str):
                texts = [texts]

            # Generate deterministic embeddings based on text hash
            embeddings = []
            for text in texts:
                # Use hash of text to create deterministic but varied embeddings
                np.random.seed(hash(text) % (2**32))
                embedding = np.random.randn(384)
                embeddings.append(embedding)

            return np.array(embeddings)

    # Patch at the module level
    monkeypatch.setattr('sentence_transformers.SentenceTransformer', MockSentenceTransformer)
    return MockSentenceTransformer


# =============================================================================
# Mock Rich Console & Pyfiglet (Prevents Interactive UI Rendering)
# =============================================================================

@pytest.fixture
def mock_console():
    """Mock Rich console to capture print statements without rendering."""
    console = MagicMock()
    console.print = MagicMock()
    console.clear = MagicMock()
    console.input = MagicMock(return_value="1")
    return console


@pytest.fixture(autouse=True)
def mock_pyfiglet(monkeypatch):
    """Mock pyfiglet to avoid ASCII art rendering in tests."""
    def mock_figlet_format(text, **kwargs):
        return f"MOCKED_BANNER: {text}"

    monkeypatch.setattr('pyfiglet.figlet_format', mock_figlet_format)


@pytest.fixture(autouse=True)
def mock_rich_prompt(monkeypatch):
    """Mock Rich Prompt to avoid interactive input in tests."""
    mock_prompt_class = MagicMock()
    mock_prompt_class.ask = MagicMock(return_value="1")
    monkeypatch.setattr('rich.prompt.Prompt', mock_prompt_class)


# =============================================================================
# Test Data Fixtures
# =============================================================================

@pytest.fixture
def mock_skills_data():
    """Load mock skills data from fixtures."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    with open(fixtures_dir / "mock_skills.json", "r") as f:
        return json.load(f)


@pytest.fixture
def mock_registry_data():
    """Load mock registry data from fixtures."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    with open(fixtures_dir / "mock_registry.json", "r") as f:
        return json.load(f)


@pytest.fixture
def sample_skill_complete():
    """A complete skill with all required fields."""
    return {
        "skill_id": "complete_skill",
        "name": "Complete Skill",
        "description": "A fully specified skill",
        "version": "1.0.0",
        "verified": True,
        "job_function": "engineering",
        "domains": ["testing"],
        "instructions": "Do something useful",
        "input_schema": {
            "type": "object",
            "properties": {
                "input": {"type": "string"}
            }
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "output": {"type": "string"}
            }
        },
        "tools": [{"name": "test_tool"}],
        "exitStates": [
            {"state": "complete", "description": "Done"}
        ]
    }


@pytest.fixture
def sample_skill_incomplete():
    """An incomplete skill missing I/O schemas."""
    return {
        "skill_id": "incomplete_skill",
        "name": "Incomplete Skill",
        "description": "Missing schemas",
        "version": "1.0.0",
        "verified": False,
        "job_function": "engineering",
        "domains": ["testing"],
        "instructions": "Do something"
    }


@pytest.fixture
def sample_skill_high_risk():
    """A high-risk skill with dangerous operations."""
    return {
        "skill_id": "high_risk_skill",
        "name": "Dangerous Operation",
        "description": "Delete user password and payment data",
        "version": "1.0.0",
        "verified": False,
        "job_function": "engineering",
        "domains": ["admin"],
        "instructions": "Delete all user data including passwords and payment information",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"}
            }
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "deleted": {"type": "boolean"}
            }
        },
        "tools": [{"name": "database_delete"}]
    }


# =============================================================================
# Temporary Directory Fixtures
# =============================================================================

@pytest.fixture
def temp_skills_directory(mock_skills_data):
    """
    Create a temporary skills directory with test data.
    Auto-cleanup after test completes.
    """
    temp_dir = tempfile.mkdtemp()
    skills_library = Path(temp_dir) / "skills-library"

    # Create job function directories
    for job_function in ["engineering", "marketing", "finops", "content"]:
        job_dir = skills_library / job_function
        job_dir.mkdir(parents=True, exist_ok=True)

    # Create skill directories and files
    for skill in mock_skills_data:
        skill_id = skill["skill_id"]
        job_function = skill.get("job_function", "engineering")
        skill_dir = skills_library / job_function / skill_id
        skill_dir.mkdir(parents=True, exist_ok=True)

        # Write skill.json
        with open(skill_dir / "skill.json", "w") as f:
            json.dump(skill, f, indent=2)

    yield Path(temp_dir)

    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_output_directory():
    """Create a temporary directory for test outputs."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


# =============================================================================
# Mock External Dependencies
# =============================================================================

@pytest.fixture
def mock_subprocess(monkeypatch):
    """Mock subprocess.run for CLI testing."""
    mock_run = MagicMock()
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "Success"
    mock_run.return_value.stderr = ""
    monkeypatch.setattr('subprocess.run', mock_run)
    return mock_run


# =============================================================================
# Parametrized Test Data
# =============================================================================

@pytest.fixture(params=[0.95, 0.88, 0.70])
def similarity_threshold(request):
    """Parametrized similarity thresholds for deduplication testing."""
    return request.param


@pytest.fixture(params=["Critical", "High", "Medium", "Low"])
def risk_level(request):
    """Parametrized risk levels for security testing."""
    return request.param


# =============================================================================
# Helper Functions
# =============================================================================

def create_mock_skill_file(directory: Path, skill_data: dict) -> Path:
    """Helper to create a mock skill file in a directory."""
    skill_id = skill_data["skill_id"]
    job_function = skill_data.get("job_function", "engineering")
    skill_dir = directory / "skills-library" / job_function / skill_id
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_file = skill_dir / "skill.json"
    with open(skill_file, "w") as f:
        json.dump(skill_data, f, indent=2)

    return skill_file


# Make helper available to tests
pytest.create_mock_skill_file = create_mock_skill_file
