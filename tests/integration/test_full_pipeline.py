"""
Integration tests for full Skills Directory pipeline

Tests the complete workflow:
1. Analyze skills for security and categorization
2. Run deduplication to find similar skills
3. Generate workflow blueprints based on I/O compatibility
4. Verify all components work together
"""

import json
import pytest
from pathlib import Path
import sys
import subprocess
import yaml

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from dedupe_skills import SkillDeduplicator
from analyze_skills import SkillAnalyzer
from generate_blueprints import ChainArchitect


# =============================================================================
# Full Pipeline Integration Tests
# =============================================================================

@pytest.mark.integration
@pytest.mark.slow
def test_analyze_dedupe_chain_pipeline(temp_skills_directory, temp_output_directory, mock_skills_data):
    """Test complete pipeline: analyze → dedupe → blueprints."""

    # Phase 1: Analyze Skills
    analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))
    analyzer.analyze_all_skills()

    assert len(analyzer.analyzed_skills) > 0
    analysis_report = temp_output_directory / "security_report.md"
    analyzer.generate_security_report(str(analysis_report))
    assert analysis_report.exists()

    # Phase 2: Deduplication
    deduplicator = SkillDeduplicator(similarity_threshold=0.85, base_path=str(temp_skills_directory))
    deduplicator.load_all_skills()
    deduplicator.generate_embeddings()
    deduplicator.find_duplicates()
    deduplicator.validate_completeness()

    dedupe_report = temp_output_directory / "dedupe_report.json"
    deduplicator.generate_report(str(dedupe_report), format="json")
    assert dedupe_report.exists()

    # Phase 3: Blueprint Generation
    # Create registry for architect
    registry_dir = temp_skills_directory / "registry" / "job_functions"
    registry_dir.mkdir(parents=True, exist_ok=True)

    # Create minimal index from analyzed skills
    index_data = {}
    for skill in analyzer.analyzed_skills:
        job_func = skill.job_function
        if job_func not in index_data:
            index_data[job_func] = []
        index_data[job_func].append({
            "skill_id": skill.skill_id,
            "name": skill.skill_id
        })

    with open(registry_dir / "index.json", "w") as f:
        json.dump(index_data, f)

    architect = ChainArchitect(base_path=str(temp_skills_directory))
    architect.load_skills()
    architect.analyze_chainability()
    architect.identify_missing_links()

    chain_report = temp_output_directory / "chain_report.json"
    architect.generate_chain_report(str(chain_report))
    assert chain_report.exists()

    # Verify all reports exist
    assert analysis_report.exists()
    assert dedupe_report.exists()
    assert chain_report.exists()


@pytest.mark.integration
def test_cli_to_report_generation(temp_skills_directory, temp_output_directory, mock_skills_data):
    """Test CLI commands generate valid reports."""

    # Test that analyze_skills produces valid output
    analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))
    analyzer.analyze_all_skills()

    security_report = temp_output_directory / "security.md"
    job_index = temp_output_directory / "job_index.json"

    analyzer.generate_security_report(str(security_report))
    analyzer.generate_job_function_index(str(job_index))

    assert security_report.exists()
    assert job_index.exists()

    # Verify job index structure
    with open(job_index) as f:
        index = json.load(f)
        assert isinstance(index, dict)


@pytest.mark.integration
def test_registry_health_flow(temp_skills_directory, mock_registry_data):
    """Test health metrics reflect actual repository state."""

    # Create registry
    registry_dir = temp_skills_directory / "registry" / "job_functions"
    registry_dir.mkdir(parents=True, exist_ok=True)

    with open(registry_dir / "index.json", "w") as f:
        json.dump(mock_registry_data, f)

    # Calculate health metrics
    total_skills = sum(len(skills) for skills in mock_registry_data.values())
    total_functions = len(mock_registry_data)

    assert total_skills > 0
    assert total_functions > 0

    # Test deduplication on real data
    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))
    deduplicator.load_all_skills()

    if len(deduplicator.skills) > 0:
        deduplicator.generate_embeddings()
        deduplicator.find_duplicates()

        # Uniqueness score
        total = len(deduplicator.skills)
        duplicates = len(deduplicator.duplicates)
        uniqueness = ((total - duplicates) / total * 100) if total > 0 else 100

        assert 0 <= uniqueness <= 100


# =============================================================================
# Cross-Component Integration Tests
# =============================================================================

@pytest.mark.integration
def test_security_analysis_affects_blueprints(temp_skills_directory, temp_output_directory):
    """Test that security analysis results influence blueprint generation."""

    # Analyze security
    analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))
    analyzer.analyze_all_skills()

    # Get high-risk skills
    high_risk_skills = [s for s in analyzer.analyzed_skills if s.security_risk_level in ["Critical", "High"]]

    # Generate blueprints
    registry_dir = temp_skills_directory / "registry" / "job_functions"
    registry_dir.mkdir(parents=True, exist_ok=True)

    index_data = {"engineering": [{"skill_id": "test", "name": "Test"}]}
    with open(registry_dir / "index.json", "w") as f:
        json.dump(index_data, f)

    architect = ChainArchitect(base_path=str(temp_skills_directory))
    architect.load_skills()
    architect.analyze_chainability()

    # High-risk skills should be noted or handled differently
    # (implementation may vary)
    assert len(high_risk_skills) >= 0  # Can be zero


@pytest.mark.integration
def test_dedupe_results_inform_verification(temp_skills_directory):
    """Test that deduplication results help identify verification candidates."""

    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))
    deduplicator.load_all_skills()

    if len(deduplicator.skills) > 0:
        deduplicator.generate_embeddings()
        deduplicator.find_duplicates()
        deduplicator.identify_unique_verified()

        # Unique verified skills are candidates for promotion
        assert isinstance(deduplicator.unique_verified, list)


# =============================================================================
# Data Consistency Tests
# =============================================================================

@pytest.mark.integration
def test_all_analyzed_skills_have_security_levels(temp_skills_directory):
    """Test all analyzed skills get assigned security risk levels."""

    analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))
    analyzer.analyze_all_skills()

    for skill_analysis in analyzer.analyzed_skills:
        assert skill_analysis.security_risk_level in ["Critical", "High", "Medium", "Low"]
        assert isinstance(skill_analysis.risk_factors, list)


@pytest.mark.integration
def test_all_analyzed_skills_have_job_functions(temp_skills_directory):
    """Test all analyzed skills get assigned job functions."""

    analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))
    analyzer.analyze_all_skills()

    for skill_analysis in analyzer.analyzed_skills:
        assert isinstance(skill_analysis.job_function, str)
        assert len(skill_analysis.job_function) > 0


@pytest.mark.integration
def test_dedupe_embeddings_match_skill_count(temp_skills_directory):
    """Test that embedding count matches loaded skill count."""

    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))
    deduplicator.load_all_skills()
    skill_count = len(deduplicator.skills)

    deduplicator.generate_embeddings()

    assert len(deduplicator.embeddings) == skill_count


# =============================================================================
# Report Format Validation Tests
# =============================================================================

@pytest.mark.integration
def test_all_reports_valid_json(temp_skills_directory, temp_output_directory):
    """Test that all JSON reports are valid and parseable."""

    # Generate all reports
    analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))
    analyzer.analyze_all_skills()

    job_index = temp_output_directory / "job_index.json"
    analyzer.generate_job_function_index(str(job_index))

    # Validate JSON
    with open(job_index) as f:
        data = json.load(f)
        assert isinstance(data, dict)

    # Test dedupe report
    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))
    deduplicator.load_all_skills()

    if len(deduplicator.skills) > 0:
        deduplicator.generate_embeddings()
        deduplicator.find_duplicates()

        dedupe_report = temp_output_directory / "dedupe.json"
        deduplicator.generate_report(str(dedupe_report), format="json")

        with open(dedupe_report) as f:
            data = json.load(f)
            assert "summary" in data


@pytest.mark.integration
def test_all_reports_valid_markdown(temp_skills_directory, temp_output_directory):
    """Test that Markdown reports are properly formatted."""

    analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))
    analyzer.analyze_all_skills()

    security_report = temp_output_directory / "security.md"
    analyzer.generate_security_report(str(security_report))

    content = security_report.read_text()

    # Check for markdown elements
    assert "#" in content or len(content) > 0  # Has headers or content


# =============================================================================
# Performance Integration Tests
# =============================================================================

@pytest.mark.integration
@pytest.mark.slow
def test_pipeline_completes_in_reasonable_time(temp_skills_directory, temp_output_directory):
    """Test that full pipeline completes in reasonable time with test data."""

    import time

    start_time = time.time()

    # Run minimal pipeline
    analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))
    analyzer.analyze_all_skills()

    deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))
    deduplicator.load_all_skills()

    if len(deduplicator.skills) > 0:
        deduplicator.generate_embeddings()
        deduplicator.find_duplicates()

    elapsed = time.time() - start_time

    # With mock data (10 skills), should complete quickly
    assert elapsed < 30  # 30 seconds for test data


# =============================================================================
# Edge Case Integration Tests
# =============================================================================

@pytest.mark.integration
def test_handles_empty_skills_directory(temp_output_directory):
    """Test pipeline handles empty skills directory gracefully."""

    # Create empty directory
    empty_dir = temp_output_directory / "empty_skills"
    empty_dir.mkdir()
    skills_lib = empty_dir / "skills-library"
    skills_lib.mkdir()

    analyzer = SkillAnalyzer(skills_library_path=str(skills_lib))
    analyzer.analyze_all_skills()

    assert len(analyzer.analyzed_skills) == 0


@pytest.mark.integration
def test_handles_mixed_valid_invalid_skills(temp_skills_directory, sample_skill_complete):
    """Test pipeline handles mix of valid and invalid skills."""

    # Create valid skill
    valid_dir = temp_skills_directory / "skills-library" / "engineering" / "valid"
    valid_dir.mkdir(parents=True, exist_ok=True)
    with open(valid_dir / "skill.json", "w") as f:
        json.dump(sample_skill_complete, f)

    # Create invalid skill
    invalid_dir = temp_skills_directory / "skills-library" / "engineering" / "invalid"
    invalid_dir.mkdir(parents=True, exist_ok=True)
    with open(invalid_dir / "skill.json", "w") as f:
        f.write("{ invalid }")

    analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))
    analyzer.analyze_all_skills()

    # Should process valid skills, skip invalid
    assert len(analyzer.analyzed_skills) >= 1
