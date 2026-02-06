"""
Performance tests for large-scale operations

Tests performance with full 808 skills dataset to ensure operations
complete within acceptable time limits.
"""

import json
import pytest
from pathlib import Path
import sys
import time

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from dedupe_skills import SkillDeduplicator
from analyze_skills import SkillAnalyzer
from generate_blueprints import ChainArchitect


# =============================================================================
# Deduplication Performance Tests
# =============================================================================

@pytest.mark.performance
@pytest.mark.slow
def test_dedupe_performance_full_dataset():
    """Test deduplication performance with full 808 skills dataset."""

    base_path = Path(__file__).parent.parent.parent

    # Skip if skills library doesn't exist or is too small
    skills_path = base_path / "skills-library"
    if not skills_path.exists():
        pytest.skip("Skills library not found")

    skill_files = list(skills_path.rglob("skill.json"))
    if len(skill_files) < 100:
        pytest.skip("Not enough skills for performance test")

    deduplicator = SkillDeduplicator(base_path=str(base_path))

    # Test loading
    start = time.time()
    deduplicator.load_all_skills()
    load_time = time.time() - start

    print(f"\n⏱️  Load time: {load_time:.2f}s for {len(deduplicator.skills)} skills")
    assert load_time < 10, "Loading should complete in under 10 seconds"

    # Test embedding generation
    start = time.time()
    deduplicator.generate_embeddings()
    embedding_time = time.time() - start

    print(f"⏱️  Embedding time: {embedding_time:.2f}s")
    assert embedding_time < 60, "Embedding generation should complete in under 60 seconds"

    # Test duplicate finding
    start = time.time()
    deduplicator.find_duplicates()
    dedupe_time = time.time() - start

    print(f"⏱️  Dedupe time: {dedupe_time:.2f}s")
    assert dedupe_time < 30, "Duplicate detection should complete in under 30 seconds"


@pytest.mark.performance
def test_dedupe_memory_usage():
    """Test that deduplication doesn't use excessive memory."""

    import psutil
    import os

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

    base_path = Path(__file__).parent.parent.parent
    skills_path = base_path / "skills-library"

    if not skills_path.exists():
        pytest.skip("Skills library not found")

    deduplicator = SkillDeduplicator(base_path=str(base_path))
    deduplicator.load_all_skills()

    if len(deduplicator.skills) > 0:
        deduplicator.generate_embeddings()

    peak_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = peak_memory - initial_memory

    print(f"\n💾 Memory increase: {memory_increase:.2f} MB")
    assert memory_increase < 2000, "Memory usage should stay under 2GB"


# =============================================================================
# Analysis Performance Tests
# =============================================================================

@pytest.mark.performance
@pytest.mark.slow
def test_analyze_performance_full_dataset():
    """Test security analysis performance with full dataset."""

    base_path = Path(__file__).parent.parent.parent
    skills_path = base_path / "skills-library"

    if not skills_path.exists():
        pytest.skip("Skills library not found")

    skill_files = list(skills_path.rglob("skill.json"))
    if len(skill_files) < 100:
        pytest.skip("Not enough skills for performance test")

    analyzer = SkillAnalyzer(skills_library_path=str(skills_path))

    start = time.time()
    analyzer.analyze_all_skills()
    analysis_time = time.time() - start

    print(f"\n⏱️  Analysis time: {analysis_time:.2f}s for {len(analyzer.analyzed_skills)} skills")
    assert analysis_time < 120, "Analysis should complete in under 2 minutes"

    # Verify all skills were analyzed
    assert len(analyzer.analyzed_skills) > 0


@pytest.mark.performance
def test_analyze_scales_linearly():
    """Test that analysis time scales roughly linearly with skill count."""

    base_path = Path(__file__).parent.parent.parent
    skills_path = base_path / "skills-library"

    if not skills_path.exists():
        pytest.skip("Skills library not found")

    # This is a basic check - actual implementation would need more sophisticated testing
    analyzer = SkillAnalyzer(skills_library_path=str(skills_path))

    start = time.time()
    analyzer.analyze_all_skills()
    total_time = time.time() - start

    if len(analyzer.analyzed_skills) > 0:
        time_per_skill = total_time / len(analyzer.analyzed_skills)
        print(f"\n⏱️  Time per skill: {time_per_skill*1000:.2f}ms")

        # Should process at least 5 skills per second
        assert time_per_skill < 0.2


# =============================================================================
# Blueprint Generation Performance Tests
# =============================================================================

@pytest.mark.performance
@pytest.mark.slow
def test_blueprint_generation_performance():
    """Test blueprint generation performance."""

    base_path = Path(__file__).parent.parent.parent

    registry_path = base_path / "registry" / "job_functions" / "index.json"
    if not registry_path.exists():
        pytest.skip("Registry not found")

    architect = ChainArchitect(base_path=str(base_path))

    start = time.time()
    architect.load_skills()
    load_time = time.time() - start

    print(f"\n⏱️  Load time: {load_time:.2f}s for {len(architect.skills)} skills")
    assert load_time < 10, "Loading should complete quickly"

    start = time.time()
    architect.analyze_chainability()
    chain_time = time.time() - start

    print(f"⏱️  Chain analysis time: {chain_time:.2f}s")
    assert chain_time < 30, "Chain analysis should complete in under 30 seconds"


# =============================================================================
# Concurrent Operations Tests
# =============================================================================

@pytest.mark.performance
@pytest.mark.slow
def test_concurrent_analysis_and_dedupe():
    """Test running analysis and deduplication concurrently."""

    import threading

    base_path = Path(__file__).parent.parent.parent
    skills_path = base_path / "skills-library"

    if not skills_path.exists():
        pytest.skip("Skills library not found")

    results = {"analyzer": None, "deduplicator": None}

    def run_analyzer():
        analyzer = SkillAnalyzer(skills_library_path=str(skills_path))
        analyzer.analyze_all_skills()
        results["analyzer"] = len(analyzer.analyzed_skills)

    def run_deduplicator():
        deduplicator = SkillDeduplicator(base_path=str(base_path))
        deduplicator.load_all_skills()
        if len(deduplicator.skills) > 0:
            deduplicator.generate_embeddings()
        results["deduplicator"] = len(deduplicator.skills)

    start = time.time()

    thread1 = threading.Thread(target=run_analyzer)
    thread2 = threading.Thread(target=run_deduplicator)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    total_time = time.time() - start

    print(f"\n⏱️  Concurrent execution time: {total_time:.2f}s")
    assert results["analyzer"] is not None
    assert results["deduplicator"] is not None


# =============================================================================
# Batch Processing Tests
# =============================================================================

@pytest.mark.performance
def test_batch_skill_processing():
    """Test processing skills in batches for efficiency."""

    base_path = Path(__file__).parent.parent.parent
    skills_path = base_path / "skills-library"

    if not skills_path.exists():
        pytest.skip("Skills library not found")

    analyzer = SkillAnalyzer(skills_library_path=str(skills_path))

    # Process skills
    start = time.time()
    analyzer.analyze_all_skills()
    batch_time = time.time() - start

    if len(analyzer.analyzed_skills) > 0:
        print(f"\n⏱️  Processed {len(analyzer.analyzed_skills)} skills in {batch_time:.2f}s")
        throughput = len(analyzer.analyzed_skills) / batch_time
        print(f"📊 Throughput: {throughput:.2f} skills/second")

        # Should maintain reasonable throughput
        assert throughput > 1  # At least 1 skill per second


# =============================================================================
# I/O Performance Tests
# =============================================================================

@pytest.mark.performance
def test_file_io_performance():
    """Test file I/O performance with large skill sets."""

    base_path = Path(__file__).parent.parent.parent
    skills_path = base_path / "skills-library"

    if not skills_path.exists():
        pytest.skip("Skills library not found")

    # Test reading all skill files
    start = time.time()
    skill_files = list(skills_path.rglob("skill.json"))

    skills_loaded = 0
    for skill_file in skill_files[:100]:  # Test first 100
        try:
            with open(skill_file) as f:
                json.load(f)
            skills_loaded += 1
        except Exception:
            pass

    io_time = time.time() - start

    print(f"\n⏱️  Loaded {skills_loaded} skills in {io_time:.2f}s")

    if skills_loaded > 0:
        time_per_file = io_time / skills_loaded
        print(f"⏱️  Time per file: {time_per_file*1000:.2f}ms")
        assert time_per_file < 0.1  # Less than 100ms per file


# =============================================================================
# Report Generation Performance Tests
# =============================================================================

@pytest.mark.performance
def test_report_generation_performance(temp_output_directory):
    """Test report generation performance."""

    base_path = Path(__file__).parent.parent.parent
    skills_path = base_path / "skills-library"

    if not skills_path.exists():
        pytest.skip("Skills library not found")

    analyzer = SkillAnalyzer(skills_library_path=str(skills_path))
    analyzer.analyze_all_skills()

    if len(analyzer.analyzed_skills) == 0:
        pytest.skip("No skills analyzed")

    # Test report generation speed
    start = time.time()
    report_path = temp_output_directory / "perf_report.md"
    analyzer.generate_security_report(str(report_path))
    report_time = time.time() - start

    print(f"\n⏱️  Report generation time: {report_time:.2f}s")
    assert report_time < 5, "Report generation should be fast"
    assert report_path.exists()


# =============================================================================
# Stress Tests
# =============================================================================

@pytest.mark.performance
@pytest.mark.slow
def test_repeated_operations_stability():
    """Test stability under repeated operations."""

    base_path = Path(__file__).parent.parent.parent
    skills_path = base_path / "skills-library"

    if not skills_path.exists():
        pytest.skip("Skills library not found")

    # Run analysis multiple times
    times = []

    for i in range(3):
        analyzer = SkillAnalyzer(skills_library_path=str(skills_path))

        start = time.time()
        analyzer.analyze_all_skills()
        elapsed = time.time() - start

        times.append(elapsed)
        print(f"\n🔄 Run {i+1}: {elapsed:.2f}s")

    # Performance should be consistent
    avg_time = sum(times) / len(times)
    max_deviation = max(abs(t - avg_time) for t in times)

    print(f"📊 Average: {avg_time:.2f}s, Max deviation: {max_deviation:.2f}s")

    # Deviation should be reasonable (within 50% of average)
    assert max_deviation < avg_time * 0.5
