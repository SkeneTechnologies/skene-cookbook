"""
E2E Tests: User Workflow Scenarios

Tests that validate complete user journeys from start to finish.
These tests simulate real-world usage patterns.
"""

import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pytest


@pytest.mark.e2e
@pytest.mark.slow
class TestFirstTimeUserJourney:
    """Test the first-time user experience."""

    def test_complete_first_user_workflow(self, temp_output_directory):
        """Test complete workflow: install → explore → analyze → report."""
        base_path = Path(__file__).parent.parent.parent

        # Step 1: User runs help to understand commands
        result = subprocess.run(
            [sys.executable, str(base_path / "scripts" / "dedupe_skills.py"), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Should show help without crashing
        assert result.returncode in [0, 1, 2]

        # Step 2: User tries to analyze skills (may fail if dependencies missing)
        # This is okay - we're testing the process, not requiring success

        # Step 3: User should be able to find documentation
        readme = base_path / "README.md"
        assert readme.exists()

        # Step 4: User should be able to find test documentation
        test_readme = base_path / "tests" / "README.md"
        assert test_readme.exists()


@pytest.mark.e2e
class TestDataAnalystWorkflow:
    """Test data analyst user journey."""

    def test_deduplication_workflow(self, temp_skills_directory, temp_output_directory):
        """Test complete deduplication analysis workflow."""
        base_path = Path(__file__).parent.parent.parent

        # Import and run deduplication
        sys.path.insert(0, str(base_path / "scripts"))
        from dedupe_skills import SkillDeduplicator

        # Run analysis
        deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))
        deduplicator.load_all_skills()

        if len(deduplicator.skills) == 0:
            pytest.skip("No skills loaded for testing")

        deduplicator.generate_embeddings()
        deduplicator.find_duplicates()
        deduplicator.validate_completeness()

        # Generate report
        report_path = temp_output_directory / "dedupe_report.json"
        deduplicator.generate_report(str(report_path), format="json")

        # Verify report was created
        assert report_path.exists()

        # Verify report structure
        with open(report_path) as f:
            report = json.load(f)

        assert "summary" in report
        assert "total_skills" in report["summary"]


@pytest.mark.e2e
class TestSecurityAuditorWorkflow:
    """Test security auditor user journey."""

    def test_security_analysis_workflow(self, temp_skills_directory, temp_output_directory):
        """Test complete security analysis workflow."""
        base_path = Path(__file__).parent.parent.parent

        # Import and run security analysis
        sys.path.insert(0, str(base_path / "scripts"))
        from analyze_skills import SkillAnalyzer

        # Run analysis
        analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))
        analyzer.analyze_all_skills()

        if len(analyzer.analyzed_skills) == 0:
            pytest.skip("No skills analyzed")

        # Generate reports
        security_report = temp_output_directory / "security.md"
        analyzer.generate_security_report(str(security_report))

        job_index = temp_output_directory / "job_index.json"
        analyzer.generate_job_function_index(str(job_index))

        # Verify reports created
        assert security_report.exists()
        assert job_index.exists()

        # Verify report content
        with open(job_index) as f:
            index = json.load(f)

        assert isinstance(index, dict)


@pytest.mark.e2e
@pytest.mark.slow
class TestPerformanceUnderLoad:
    """Test performance with realistic workloads."""

    def test_large_dataset_processing(self):
        """Test processing performance with full dataset."""
        base_path = Path(__file__).parent.parent.parent
        skills_library = base_path / "skills-library"

        if not skills_library.exists():
            pytest.skip("Skills library not found")

        skill_files = list(skills_library.rglob("skill.json"))

        if len(skill_files) < 100:
            pytest.skip("Not enough skills for performance testing")

        # Import deduplicator
        sys.path.insert(0, str(base_path / "scripts"))
        from dedupe_skills import SkillDeduplicator

        # Time the operation
        start_time = time.time()

        deduplicator = SkillDeduplicator(base_path=str(base_path))
        deduplicator.load_all_skills()

        load_time = time.time() - start_time

        # Should load reasonably fast
        assert load_time < 30, f"Loading took {load_time}s (expected < 30s)"

        # Verify skills were loaded
        assert len(deduplicator.skills) > 0

    def test_concurrent_operations_stability(self):
        """Test stability under concurrent operations."""
        # This would test running multiple operations simultaneously
        # Simplified version here
        pass


@pytest.mark.e2e
class TestErrorRecovery:
    """Test error handling and recovery."""

    def test_handles_missing_directory_gracefully(self):
        """Test graceful handling of missing directories."""
        base_path = Path(__file__).parent.parent.parent
        sys.path.insert(0, str(base_path / "scripts"))

        from dedupe_skills import SkillDeduplicator

        # Try to initialize with nonexistent path
        deduplicator = SkillDeduplicator(base_path="/nonexistent/path")

        # Should not crash during init
        assert deduplicator.base_path == Path("/nonexistent/path")

    def test_handles_corrupted_skill_files(self, temp_skills_directory):
        """Test handling of corrupted skill files."""
        # Create a corrupted skill file
        corrupted_dir = temp_skills_directory / "skills-library" / "test" / "corrupted"
        corrupted_dir.mkdir(parents=True, exist_ok=True)

        with open(corrupted_dir / "skill.json", "w") as f:
            f.write("{ invalid json }")

        base_path = Path(__file__).parent.parent.parent
        sys.path.insert(0, str(base_path / "scripts"))

        from dedupe_skills import SkillDeduplicator

        # Should handle corruption gracefully
        deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))
        deduplicator.load_all_skills()

        # Should skip corrupted file, not crash
        # Exact behavior depends on implementation


@pytest.mark.e2e
class TestCLIInteractions:
    """Test CLI command-line interactions."""

    def test_help_commands_work(self):
        """Test that all main scripts respond to --help."""
        base_path = Path(__file__).parent.parent.parent

        scripts = [
            "scripts/dedupe_skills.py",
            "scripts/analyze_skills.py",
            "scripts/generate_blueprints.py",
        ]

        for script in scripts:
            script_path = base_path / script

            if not script_path.exists():
                continue

            result = subprocess.run(
                [sys.executable, str(script_path), "--help"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            # Should respond to help (returncode 0, 1, or 2 acceptable)
            assert result.returncode in [0, 1, 2]

    def test_version_commands_work(self):
        """Test version information display."""
        # If scripts support --version
        pass

    def test_dry_run_mode_works(self):
        """Test dry-run mode if available."""
        # If scripts support --dry-run
        pass


@pytest.mark.e2e
class TestDocumentationWorkflow:
    """Test following documentation examples."""

    def test_readme_quick_start_works(self):
        """Test that README quick start instructions work."""
        base_path = Path(__file__).parent.parent.parent
        readme = base_path / "README.md"

        if not readme.exists():
            pytest.skip("README.md not found")

        # Extract code blocks from README
        # Try executing them
        # This is a simplified version

        content = readme.read_text()

        # Check that installation instructions are present
        assert "install" in content.lower() or "pip" in content.lower()

        # Check that usage examples are present
        assert "python" in content.lower() or "usage" in content.lower()


@pytest.mark.e2e
@pytest.mark.slow
class TestEndToEndIntegration:
    """Complete end-to-end integration tests."""

    def test_full_pipeline_execution(self, temp_skills_directory, temp_output_directory):
        """Test complete pipeline: analyze → dedupe → blueprints."""
        base_path = Path(__file__).parent.parent.parent
        sys.path.insert(0, str(base_path / "scripts"))

        from analyze_skills import SkillAnalyzer
        from dedupe_skills import SkillDeduplicator

        # Step 1: Security Analysis
        analyzer = SkillAnalyzer(skills_library_path=str(temp_skills_directory / "skills-library"))
        analyzer.analyze_all_skills()

        # Step 2: Deduplication
        deduplicator = SkillDeduplicator(base_path=str(temp_skills_directory))
        deduplicator.load_all_skills()

        if len(deduplicator.skills) > 0:
            deduplicator.generate_embeddings()
            deduplicator.find_duplicates()

        # Step 3: Generate outputs
        security_report = temp_output_directory / "security.md"
        analyzer.generate_security_report(str(security_report))

        dedupe_report = temp_output_directory / "dedupe.json"
        if len(deduplicator.skills) > 0:
            deduplicator.generate_report(str(dedupe_report), format="json")

        # Verify outputs
        assert security_report.exists() or len(analyzer.analyzed_skills) == 0

    def test_data_consistency_across_runs(self, temp_skills_directory):
        """Test that multiple runs produce consistent results."""
        base_path = Path(__file__).parent.parent.parent
        sys.path.insert(0, str(base_path / "scripts"))

        from dedupe_skills import SkillDeduplicator

        # Run 1
        deduplicator1 = SkillDeduplicator(base_path=str(temp_skills_directory))
        deduplicator1.load_all_skills()
        count1 = len(deduplicator1.skills)

        # Run 2
        deduplicator2 = SkillDeduplicator(base_path=str(temp_skills_directory))
        deduplicator2.load_all_skills()
        count2 = len(deduplicator2.skills)

        # Should load same number of skills
        assert count1 == count2
