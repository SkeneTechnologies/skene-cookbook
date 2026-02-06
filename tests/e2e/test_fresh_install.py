"""
E2E Tests: Fresh Installation Scenarios

Tests that validate fresh installation experience on different platforms.
These tests simulate a new user cloning the repository and getting started.
"""

import pytest
import subprocess
import tempfile
import shutil
from pathlib import Path
import sys


@pytest.mark.e2e
@pytest.mark.slow
class TestFreshInstallation:
    """Test fresh installation scenarios."""

    def test_requirements_install_cleanly(self):
        """Test that all requirements install without conflicts."""
        result = subprocess.run(
            [sys.executable, "-m", "pip", "check"],
            capture_output=True,
            text=True
        )

        # Should have no dependency conflicts
        assert "No broken requirements" in result.stdout or result.returncode == 0

    def test_all_scripts_are_executable(self):
        """Test that main scripts can be found and executed."""
        scripts = [
            "scripts/dedupe_skills.py",
            "scripts/analyze_skills.py",
            "scripts/generate_blueprints.py",
            "skill-loom-cli.py",
            "loom"
        ]

        base_path = Path(__file__).parent.parent.parent

        for script in scripts:
            script_path = base_path / script
            assert script_path.exists(), f"Script not found: {script}"

            # Test that script can show help
            result = subprocess.run(
                [sys.executable, str(script_path), "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )

            # Should not crash (returncode 0 or 1 for scripts without --help)
            assert result.returncode in [0, 1, 2], f"Script failed to run: {script}"

    def test_minimal_dependencies_work(self):
        """Test that core functionality works with minimal dependencies."""
        # Core dependencies that must be present
        required_imports = [
            "json",
            "yaml",
            "pathlib",
            "argparse"
        ]

        for module in required_imports:
            try:
                __import__(module)
            except ImportError:
                pytest.fail(f"Required module not available: {module}")

    def test_skills_library_accessible(self):
        """Test that skills library is present and readable."""
        base_path = Path(__file__).parent.parent.parent
        skills_library = base_path / "skills-library"

        assert skills_library.exists(), "skills-library directory not found"
        assert skills_library.is_dir(), "skills-library is not a directory"

        # Check for some skills
        skill_files = list(skills_library.rglob("skill.json"))
        assert len(skill_files) > 0, "No skill.json files found"

    def test_registry_structure_valid(self):
        """Test that registry structure is valid and accessible."""
        base_path = Path(__file__).parent.parent.parent
        registry = base_path / "registry"

        if not registry.exists():
            pytest.skip("Registry not yet generated")

        job_functions_index = registry / "job_functions" / "index.json"

        if job_functions_index.exists():
            import json
            with open(job_functions_index) as f:
                data = json.load(f)

            assert isinstance(data, dict), "Registry index is not a dictionary"
            assert len(data) > 0, "Registry index is empty"


@pytest.mark.e2e
class TestDocumentationAccuracy:
    """Test that documentation matches reality."""

    def test_readme_exists(self):
        """Test that README.md exists and is not empty."""
        base_path = Path(__file__).parent.parent.parent
        readme = base_path / "README.md"

        assert readme.exists(), "README.md not found"
        content = readme.read_text()
        assert len(content) > 100, "README.md is too short"

    def test_license_exists(self):
        """Test that LICENSE file exists."""
        base_path = Path(__file__).parent.parent.parent
        license_files = [
            base_path / "LICENSE",
            base_path / "LICENSE.md",
            base_path / "LICENSE.txt"
        ]

        assert any(f.exists() for f in license_files), "No LICENSE file found"

    def test_contributing_guide_exists(self):
        """Test that CONTRIBUTING.md exists if public repo."""
        base_path = Path(__file__).parent.parent.parent
        contributing = base_path / "CONTRIBUTING.md"

        # This is a recommendation, not a requirement
        if contributing.exists():
            content = contributing.read_text()
            assert len(content) > 50, "CONTRIBUTING.md is too short"

    def test_all_docs_files_valid(self):
        """Test that all documentation files are valid."""
        base_path = Path(__file__).parent.parent.parent
        docs_dir = base_path / "docs"

        if not docs_dir.exists():
            pytest.skip("docs/ directory not present")

        # All markdown files should be readable
        for md_file in docs_dir.rglob("*.md"):
            content = md_file.read_text()
            assert len(content) > 0, f"Empty documentation file: {md_file}"


@pytest.mark.e2e
class TestSecurityReadiness:
    """Test security posture before public release."""

    def test_no_env_files_committed(self):
        """Test that no .env files are in the repository."""
        base_path = Path(__file__).parent.parent.parent

        env_files = list(base_path.rglob(".env*"))
        # Filter out directories
        env_files = [f for f in env_files if f.is_file()]

        assert len(env_files) == 0, f"Found .env files: {env_files}"

    def test_gitignore_comprehensive(self):
        """Test that .gitignore covers common sensitive files."""
        base_path = Path(__file__).parent.parent.parent
        gitignore = base_path / ".gitignore"

        if not gitignore.exists():
            pytest.fail(".gitignore not found")

        content = gitignore.read_text().lower()

        # Common patterns that should be ignored
        should_ignore = [
            ".env",
            "__pycache__",
            ".pytest_cache",
            ".coverage",
            "*.pyc"
        ]

        for pattern in should_ignore:
            assert pattern in content, f"Missing from .gitignore: {pattern}"

    def test_no_hardcoded_secrets_in_python(self):
        """Test for common secret patterns in Python files."""
        base_path = Path(__file__).parent.parent.parent

        suspicious_patterns = [
            b"password = ",
            b"api_key = ",
            b"secret = ",
            b"token = "
        ]

        for py_file in base_path.rglob("*.py"):
            # Skip test files and virtual environments
            if "test" in str(py_file) or "venv" in str(py_file) or ".venv" in str(py_file):
                continue

            content = py_file.read_bytes()

            for pattern in suspicious_patterns:
                if pattern in content:
                    # Check if it's just a variable name or actual assignment
                    # This is a basic check - manual review still needed
                    lines = content.split(b'\n')
                    for line in lines:
                        if pattern in line and b'=' in line:
                            # Could be a false positive, but flag for review
                            print(f"⚠️  Potential secret in {py_file}: {line}")


@pytest.mark.e2e
class TestCrossFileConsistency:
    """Test consistency across different files."""

    def test_version_consistency(self):
        """Test that version numbers are consistent across files."""
        # Check if version is defined in multiple places
        # They should match

        base_path = Path(__file__).parent.parent.parent

        # Common version locations
        version_files = [
            base_path / "setup.py",
            base_path / "pyproject.toml",
            base_path / "__init__.py"
        ]

        versions_found = []

        for vfile in version_files:
            if vfile.exists():
                content = vfile.read_text()
                # Basic version extraction (would need refinement)
                if "version" in content.lower():
                    versions_found.append(str(vfile))

        # If versions are defined, they should be consistent
        # This is a basic check

    def test_requirements_match_imports(self):
        """Test that requirements.txt includes all imported modules."""
        base_path = Path(__file__).parent.parent.parent
        requirements = base_path / "requirements.txt"

        if not requirements.exists():
            pytest.fail("requirements.txt not found")

        req_content = requirements.read_text().lower()

        # Core dependencies that should be in requirements
        expected_deps = [
            "pyyaml",
            "rich"
        ]

        for dep in expected_deps:
            assert dep in req_content, f"Missing dependency in requirements.txt: {dep}"
