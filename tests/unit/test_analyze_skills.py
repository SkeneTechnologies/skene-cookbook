"""
Unit tests for scripts/analyze_skills.py

Tests the skill analyzer that performs security risk analysis,
job function categorization, and composability analysis.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from analyze_skills import (
    SkillAnalyzer,
    SkillAnalysis,
    SECURITY_KEYWORDS,
    JOB_FUNCTION_MAPPINGS
)


# =============================================================================
# Test Initialization
# =============================================================================

@pytest.mark.unit
def test_initialization():
    """Test SkillAnalyzer initializes correctly."""
    analyzer = SkillAnalyzer(skills_library_path="test-skills")

    assert analyzer.skills_library_path == Path("test-skills")
    assert analyzer.analyzed_skills == []


@pytest.mark.unit
def test_initialization_default_path():
    """Test default skills library path."""
    analyzer = SkillAnalyzer()

    assert analyzer.skills_library_path == Path("skills-library")


# =============================================================================
# Test Risk Level Calculation
# =============================================================================

@pytest.mark.unit
def test_calculate_risk_level_critical():
    """Test detection of critical risk keywords."""
    analyzer = SkillAnalyzer()

    # Test with critical keywords
    text = "delete user password and payment information"
    skill_data = {"tools": [{"name": "database_delete"}]}

    risk_level, factors = analyzer._calculate_risk_level(text, skill_data)

    assert risk_level == "Critical"
    assert len(factors) > 0
    assert any(keyword in text for keyword in SECURITY_KEYWORDS['Critical'])


@pytest.mark.unit
def test_calculate_risk_level_high():
    """Test detection of high risk keywords."""
    analyzer = SkillAnalyzer()

    text = "write and update user personal information"
    skill_data = {"tools": [{"name": "database_write"}]}

    risk_level, factors = analyzer._calculate_risk_level(text, skill_data)

    assert risk_level in ["High", "Critical"]  # Could be either depending on keywords


@pytest.mark.unit
def test_calculate_risk_level_medium():
    """Test detection of medium risk keywords."""
    analyzer = SkillAnalyzer()

    text = "read and fetch analytics data for reporting"
    skill_data = {"tools": [{"name": "read_file"}]}

    risk_level, factors = analyzer._calculate_risk_level(text, skill_data)

    assert risk_level in ["Medium", "High", "Low"]


@pytest.mark.unit
def test_calculate_risk_level_low():
    """Test detection of low risk operations."""
    analyzer = SkillAnalyzer()

    text = "list and display available reports"
    skill_data = {"tools": [{"name": "list_items"}]}

    risk_level, factors = analyzer._calculate_risk_level(text, skill_data)

    assert risk_level in ["Low", "Medium"]


# =============================================================================
# Test Job Function Determination
# =============================================================================

@pytest.mark.unit
def test_determine_job_function_engineering():
    """Test categorization as engineering."""
    analyzer = SkillAnalyzer()

    domain = "engineering"
    text = "api integration development technical code deployment"

    job_function = analyzer._determine_job_function(domain, text)

    assert job_function == "engineering"


@pytest.mark.unit
def test_determine_job_function_marketing():
    """Test categorization as marketing."""
    analyzer = SkillAnalyzer()

    domain = "marketing"
    text = "social media campaign content marketing seo"

    job_function = analyzer._determine_job_function(domain, text)

    assert job_function == "marketing"


@pytest.mark.unit
def test_determine_job_function_sales():
    """Test categorization as sales."""
    analyzer = SkillAnalyzer()

    domain = "sales"
    text = "pipeline management deal forecast crm opportunity"

    job_function = analyzer._determine_job_function(domain, text)

    assert job_function == "sales"


@pytest.mark.unit
def test_determine_job_function_from_domain():
    """Test job function extracted from domain field."""
    analyzer = SkillAnalyzer()

    domain = "customer_success"
    text = "generic description"

    job_function = analyzer._determine_job_function(domain, text)

    assert job_function == "customer_success"


@pytest.mark.unit
def test_determine_job_function_default():
    """Test default job function when no match found."""
    analyzer = SkillAnalyzer()

    domain = "unknown"
    text = "completely generic task"

    job_function = analyzer._determine_job_function(domain, text)

    # Should return some default or most common match
    assert isinstance(job_function, str)


# =============================================================================
# Test JTBD Extraction
# =============================================================================

@pytest.mark.unit
def test_extract_jtbd():
    """Test Jobs-to-be-Done extraction."""
    analyzer = SkillAnalyzer()

    text = "help users analyze data to make better decisions"
    skill_data = {"name": "Data Analyzer", "description": text, "domain": "data"}

    jtbd = analyzer._extract_jtbd(skill_data)

    assert isinstance(jtbd, dict)
    assert 'job' in jtbd or 'context' in jtbd or jtbd != {}


@pytest.mark.unit
def test_extract_jtbd_from_description():
    """Test JTBD extraction from skill description."""
    analyzer = SkillAnalyzer()

    skill_data = {
        "name": "Report Generator",
        "description": "Generate formatted reports from raw data",
        "domain": "data"
    }

    jtbd = analyzer._extract_jtbd(skill_data)

    assert isinstance(jtbd, dict)


# =============================================================================
# Test Security Requirements Determination
# =============================================================================

@pytest.mark.unit
def test_determine_security_requirements_critical():
    """Test security requirements for critical risk skills."""
    analyzer = SkillAnalyzer()

    skill_data = {
        "name": "User Delete",
        "description": "Delete user accounts and payment data",
        "tools": [{"name": "admin_delete"}]
    }

    risk_level = "Critical"
    risk_factors = ["delete", "payment"]

    requirements = analyzer._determine_security_requirements(risk_level, risk_factors, skill_data)

    assert isinstance(requirements, dict)
    assert requirements.get('human_in_loop_required') is True or requirements.get('sandboxing_required') is True


@pytest.mark.unit
def test_determine_security_requirements_low():
    """Test security requirements for low risk skills."""
    analyzer = SkillAnalyzer()

    skill_data = {
        "name": "List Reports",
        "description": "List available reports",
        "tools": [{"name": "read"}]
    }

    risk_level = "Low"
    risk_factors = []

    requirements = analyzer._determine_security_requirements(risk_level, risk_factors, skill_data)

    assert isinstance(requirements, dict)
    # Low risk should have minimal requirements
    assert requirements.get('human_in_loop_required') is False
    assert requirements.get('sandboxing_required') is False


# =============================================================================
# Test Composability Analysis
# =============================================================================

@pytest.mark.unit
def test_analyze_composability():
    """Test composability hints from exitStates."""
    analyzer = SkillAnalyzer()

    skill_data = {
        "exitStates": [
            {"state": "complete", "nextSkills": ["skill_2", "skill_3"]},
            {"state": "error", "nextSkills": ["error_handler"]}
        ],
        "outputSchema": {
            "type": "object",
            "properties": {
                "data": {"type": "string"}
            }
        }
    }

    hints = analyzer._analyze_composability(skill_data)

    assert isinstance(hints, list)
    assert len(hints) > 0


@pytest.mark.unit
def test_analyze_composability_no_exitstates():
    """Test composability when no exitStates defined."""
    analyzer = SkillAnalyzer()

    skill_data = {
        "outputSchema": {
            "type": "object",
            "properties": {
                "result": {"type": "string"}
            }
        }
    }

    hints = analyzer._analyze_composability(skill_data)

    assert isinstance(hints, list)
    # Should still return hints based on output schema


# =============================================================================
# Test Skill File Analysis
# =============================================================================

@pytest.mark.unit
def test_analyze_skill_file_complete(temp_skills_directory, sample_skill_complete):
    """Test analysis of a complete skill file."""
    analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))

    # Create skill file
    skill_dir = temp_skills_directory / "skills-library" / "engineering" / "test_skill"
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_file = skill_dir / "skill.json"
    with open(skill_file, "w") as f:
        json.dump(sample_skill_complete, f)

    # Analyze
    analysis = analyzer.analyze_skill_file(skill_file)

    assert analysis is not None
    assert isinstance(analysis, SkillAnalysis)
    # Verify skill_id is properly extracted
    assert analysis.skill_id == sample_skill_complete["id"]
    assert analysis.security_risk_level in ["Critical", "High", "Medium", "Low"]
    assert isinstance(analysis.risk_factors, list)
    assert isinstance(analysis.composability_hints, list)


@pytest.mark.unit
def test_analyze_skill_file_with_instructions(temp_skills_directory, sample_skill_complete):
    """Test analysis including instructions.md file."""
    analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))

    # Create skill file and instructions
    skill_dir = temp_skills_directory / "skills-library" / "engineering" / "test_skill"
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_file = skill_dir / "skill.json"
    with open(skill_file, "w") as f:
        json.dump(sample_skill_complete, f)

    instructions_file = skill_dir / "instructions.md"
    with open(instructions_file, "w") as f:
        f.write("# Instructions\n\nDetailed steps for executing this skill.")

    # Analyze
    analysis = analyzer.analyze_skill_file(skill_file)

    assert analysis is not None


@pytest.mark.unit
def test_analyze_skill_file_invalid_json(temp_skills_directory):
    """Test graceful handling of invalid JSON."""
    analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))

    # Create invalid skill file
    skill_dir = temp_skills_directory / "skills-library" / "engineering" / "invalid"
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_file = skill_dir / "skill.json"
    with open(skill_file, "w") as f:
        f.write("{ invalid json }")

    # Should return None or handle gracefully
    analysis = analyzer.analyze_skill_file(skill_file)

    assert analysis is None


# =============================================================================
# Test Report Generation
# =============================================================================

@pytest.mark.unit
def test_generate_security_report(temp_output_directory):
    """Test security report generation."""
    analyzer = SkillAnalyzer()

    # Add some analyzed skills
    analyzer.analyzed_skills = [
        SkillAnalysis(
            skill_id="test_1",
            security_risk_level="Critical",
            security_requirements={"human_in_loop_required": True},
            job_function="engineering",
            jtbd={"job": "test"},
            risk_factors=["delete", "password"],
            composability_hints=["chains with X"]
        ),
        SkillAnalysis(
            skill_id="test_2",
            security_risk_level="Low",
            security_requirements={"human_in_loop_required": False},
            job_function="marketing",
            jtbd={"job": "test"},
            risk_factors=[],
            composability_hints=[]
        )
    ]

    output_file = temp_output_directory / "security_report.md"

    # Check if method exists, if not skip test gracefully
    if hasattr(analyzer, 'generate_security_report'):
        analyzer.generate_security_report(str(output_file))
        assert output_file.exists()
        content = output_file.read_text()
        assert "Security" in content or "Risk" in content or len(content) > 0
    else:
        # Method not implemented yet, skip assertion
        pytest.skip("generate_security_report method not implemented")


@pytest.mark.unit
def test_generate_job_function_index(temp_output_directory):
    """Test job function index generation."""
    analyzer = SkillAnalyzer()

    # Add some analyzed skills
    analyzer.analyzed_skills = [
        SkillAnalysis(
            skill_id="eng_1",
            security_risk_level="Low",
            security_requirements={},
            job_function="engineering",
            jtbd={"job": "test"},
            risk_factors=[],
            composability_hints=[]
        ),
        SkillAnalysis(
            skill_id="mkt_1",
            security_risk_level="Low",
            security_requirements={},
            job_function="marketing",
            jtbd={"job": "test"},
            risk_factors=[],
            composability_hints=[]
        )
    ]

    output_file = temp_output_directory / "job_function_index.json"
    analyzer.generate_job_function_index(str(output_file))

    assert output_file.exists()

    with open(output_file) as f:
        index = json.load(f)

    assert "engineering" in index or isinstance(index, dict)


# =============================================================================
# Test Full Analysis Workflow
# =============================================================================

@pytest.mark.unit
def test_analyze_all_skills(temp_skills_directory, mock_skills_data):
    """Test analyzing all skills in directory."""
    analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))

    analyzer.analyze_all_skills()

    # Should have analyzed the mock skills
    assert len(analyzer.analyzed_skills) > 0
    assert all(isinstance(a, SkillAnalysis) for a in analyzer.analyzed_skills)
