#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Batch evaluation script for evaluating multiple skills at once.

Usage:
    # Evaluate all skills in a domain
    python scripts/batch_eval_skills.py --domain ecosystem --parallel 5

    # Evaluate specific skills
    python scripts/batch_eval_skills.py --skills elg_mdf_tracker,elg_partner_tier_manager

    # Evaluate all skills in multiple domains
    python scripts/batch_eval_skills.py --domains ecosystem,marketing,revops

    # Generate test data only (no evaluation)
    python scripts/batch_eval_skills.py --domain ecosystem --generate-only

    # Use existing test data
    python scripts/batch_eval_skills.py --domain ecosystem --test-data-dir test_cases/

Features:
- Parallel execution (configurable concurrency)
- Automatic test data generation from schemas
- Aggregate reporting (domain-level and master)
- Failure categorization
- Progress tracking
"""

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from eval_harness.core import SkillValidator, SkillTracer, MetricsCollector
from eval_harness.instrumented_executor import InstrumentedSkillExecutor
from eval_harness.test_data_generator import TestDataGenerator
from eval_harness.reporters import MarkdownReporter, JSONReporter


@dataclass
class SkillEvalResult:
    """Result of evaluating a single skill."""
    skill_id: str
    domain: str
    success: bool
    num_cases: int
    success_rate: float
    validation_pass_rate: float
    auto_act_rate: float
    avg_duration_ms: float
    p95_duration_ms: float
    error: Optional[str] = None
    test_data_generated: bool = False
    timestamp: str = ""


@dataclass
class DomainSummary:
    """Summary of evaluation results for a domain."""
    domain: str
    total_skills: int
    successful: int
    failed: int
    avg_success_rate: float
    avg_auto_act_rate: float
    total_duration_sec: float


class BatchSkillEvaluator:
    """
    Evaluates multiple skills in parallel with automatic test data generation.
    """

    def __init__(
        self,
        skills_library_path: Path,
        test_data_dir: Path,
        report_dir: Path,
        parallel: int = 5,
        verbose: bool = False
    ):
        """
        Initialize batch evaluator.

        Args:
            skills_library_path: Path to skills library
            test_data_dir: Directory for test data
            report_dir: Directory for evaluation reports
            parallel: Number of parallel evaluations
            verbose: Enable verbose output
        """
        self.skills_library_path = skills_library_path
        self.test_data_dir = test_data_dir
        self.report_dir = report_dir
        self.parallel = parallel
        self.verbose = verbose

        self.test_data_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

        self.generator = TestDataGenerator(skills_library_path)
        self.validator = SkillValidator()
        self.md_reporter = MarkdownReporter(output_dir=report_dir)
        self.json_reporter = JSONReporter(output_dir=report_dir)

    def discover_skills(
        self,
        domains: Optional[List[str]] = None,
        skill_ids: Optional[List[str]] = None
    ) -> Dict[str, List[str]]:
        """
        Discover skills to evaluate.

        Args:
            domains: List of domain names to evaluate (None = all)
            skill_ids: Specific skill IDs to evaluate

        Returns:
            Dictionary mapping domain to list of skill IDs
        """
        discovered = defaultdict(list)

        if skill_ids:
            # Find specific skills
            for skill_id in skill_ids:
                skill_path = self.generator._find_skill_path(skill_id)
                if skill_path:
                    domain = skill_path.parent.name
                    discovered[domain].append(skill_id)
                else:
                    print(f"Warning: Skill not found: {skill_id}")
            return dict(discovered)

        # Discover by domain
        # Support new directory structure (executable/ and context/)
        search_paths = []
        if (self.skills_library_path / 'executable').exists():
            search_paths.append(self.skills_library_path / 'executable')
        if (self.skills_library_path / 'context').exists():
            search_paths.append(self.skills_library_path / 'context')
        if not search_paths:
            # Fallback to root if new structure doesn't exist
            search_paths = [self.skills_library_path]

        domain_dirs = []
        for search_path in search_paths:
            if domains:
                domain_dirs.extend([search_path / d for d in domains if (search_path / d).exists()])
            else:
                domain_dirs.extend([d for d in search_path.iterdir() if d.is_dir() and not d.name.startswith('.')])

        for domain_dir in domain_dirs:
            domain_name = domain_dir.name

            # Recursively find all skill.json files in this domain (handles nested directories)
            for skill_json_path in domain_dir.rglob('skill.json'):
                try:
                    with open(skill_json_path, 'r') as f:
                        skill_def = json.load(f)
                        skill_id = skill_def.get('id')
                        if skill_id:
                            discovered[domain_name].append(skill_id)
                except Exception as e:
                    if self.verbose:
                        print(f"Warning: Failed to read {skill_json_path}: {e}")

        return dict(discovered)

    def evaluate_skill(
        self,
        skill_id: str,
        domain: str,
        use_existing_test_data: bool = False
    ) -> SkillEvalResult:
        """
        Evaluate a single skill.

        Args:
            skill_id: Skill identifier
            domain: Domain name
            use_existing_test_data: Use existing test data instead of generating

        Returns:
            SkillEvalResult with evaluation metrics
        """
        start_time = time.time()
        timestamp = datetime.now().isoformat()

        try:
            # Load or generate test data
            test_data_path = self.test_data_dir / f'{skill_id}_test_data.json'

            if use_existing_test_data and test_data_path.exists():
                with open(test_data_path, 'r') as f:
                    test_data = json.load(f)
                    test_cases = test_data.get('test_cases', [])
                test_data_generated = False
            else:
                # Generate test data
                test_cases = self.generator.generate_from_skill(skill_id, num_valid_cases=3)
                self.generator.save_test_cases(skill_id, test_cases, test_data_path)
                test_data_generated = True

            if not test_cases:
                return SkillEvalResult(
                    skill_id=skill_id,
                    domain=domain,
                    success=False,
                    num_cases=0,
                    success_rate=0.0,
                    validation_pass_rate=0.0,
                    auto_act_rate=0.0,
                    avg_duration_ms=0.0,
                    p95_duration_ms=0.0,
                    error="No test cases generated",
                    test_data_generated=test_data_generated,
                    timestamp=timestamp
                )

            # Initialize instrumented executor
            metrics_collector = MetricsCollector()
            tracer = SkillTracer(provider='console')
            executor = InstrumentedSkillExecutor(
                validator=self.validator,
                tracer=tracer,
                metrics_collector=metrics_collector
            )

            # Dummy skill logic (validation-only mode)
            def dummy_skill_logic(inputs):
                """Dummy logic for validation testing."""
                # Return a minimal valid output based on skill
                return {'result': 'success', 'data': {}}

            # Execute test cases
            for test_case in test_cases:
                inputs = test_case.get('inputs', {})
                try:
                    executor.execute_skill(
                        skill_id=skill_id,
                        skill_version='1.0.0',
                        inputs=inputs,
                        skill_logic=dummy_skill_logic
                    )
                except Exception as e:
                    if self.verbose:
                        print(f"  Test case failed: {e}")

            # Get metrics
            metrics = metrics_collector.get_aggregated_metrics(skill_id)

            if not metrics:
                return SkillEvalResult(
                    skill_id=skill_id,
                    domain=domain,
                    success=False,
                    num_cases=len(test_cases),
                    success_rate=0.0,
                    validation_pass_rate=0.0,
                    auto_act_rate=0.0,
                    avg_duration_ms=0.0,
                    p95_duration_ms=0.0,
                    error="No metrics collected",
                    test_data_generated=test_data_generated,
                    timestamp=timestamp
                )

            # Save reports
            self.md_reporter.save_skill_report(
                skill_id=skill_id,
                metrics=metrics,
                session_id='batch_eval'
            )
            self.json_reporter.save_skill_report(
                skill_id=skill_id,
                metrics=metrics,
                session_id='batch_eval'
            )

            duration_sec = time.time() - start_time

            return SkillEvalResult(
                skill_id=skill_id,
                domain=domain,
                success=True,
                num_cases=len(test_cases),
                success_rate=metrics.success_rate,
                validation_pass_rate=metrics.validation_pass_rate,
                auto_act_rate=metrics.auto_act_rate,
                avg_duration_ms=metrics.avg_duration_ms,
                p95_duration_ms=metrics.p95_duration_ms,
                test_data_generated=test_data_generated,
                timestamp=timestamp
            )

        except Exception as e:
            return SkillEvalResult(
                skill_id=skill_id,
                domain=domain,
                success=False,
                num_cases=0,
                success_rate=0.0,
                validation_pass_rate=0.0,
                auto_act_rate=0.0,
                avg_duration_ms=0.0,
                p95_duration_ms=0.0,
                error=str(e),
                timestamp=timestamp
            )

    def evaluate_batch(
        self,
        domains: Optional[List[str]] = None,
        skill_ids: Optional[List[str]] = None,
        use_existing_test_data: bool = False
    ) -> List[SkillEvalResult]:
        """
        Evaluate multiple skills in parallel.

        Args:
            domains: List of domains to evaluate
            skill_ids: Specific skill IDs to evaluate
            use_existing_test_data: Use existing test data

        Returns:
            List of SkillEvalResult objects
        """
        # Discover skills
        discovered_skills = self.discover_skills(domains=domains, skill_ids=skill_ids)

        total_skills = sum(len(skills) for skills in discovered_skills.values())
        print(f"\nDiscovered {total_skills} skills across {len(discovered_skills)} domains")

        if self.verbose:
            for domain, skills in discovered_skills.items():
                print(f"  {domain}: {len(skills)} skills")

        # Evaluate in parallel
        results = []
        completed = 0

        with ThreadPoolExecutor(max_workers=self.parallel) as executor:
            futures = {}

            for domain, skills in discovered_skills.items():
                for skill_id in skills:
                    future = executor.submit(
                        self.evaluate_skill,
                        skill_id,
                        domain,
                        use_existing_test_data
                    )
                    futures[future] = (skill_id, domain)

            for future in as_completed(futures):
                skill_id, domain = futures[future]
                result = future.result()
                results.append(result)

                completed += 1
                status = "✓" if result.success else "✗"
                print(f"[{completed}/{total_skills}] {status} {domain}/{skill_id}")

                if self.verbose and result.success:
                    print(f"    Success: {result.success_rate:.1%}, Auto-act: {result.auto_act_rate:.1%}")

        return results

    def generate_domain_summary(
        self,
        results: List[SkillEvalResult]
    ) -> Dict[str, DomainSummary]:
        """
        Generate summary statistics by domain.

        Args:
            results: List of skill evaluation results

        Returns:
            Dictionary mapping domain to summary
        """
        domain_results = defaultdict(list)
        for result in results:
            domain_results[result.domain].append(result)

        summaries = {}
        for domain, domain_res in domain_results.items():
            successful = sum(1 for r in domain_res if r.success)
            failed = sum(1 for r in domain_res if not r.success)

            avg_success_rate = sum(r.success_rate for r in domain_res if r.success) / max(successful, 1)
            avg_auto_act_rate = sum(r.auto_act_rate for r in domain_res if r.success) / max(successful, 1)

            summaries[domain] = DomainSummary(
                domain=domain,
                total_skills=len(domain_res),
                successful=successful,
                failed=failed,
                avg_success_rate=avg_success_rate,
                avg_auto_act_rate=avg_auto_act_rate,
                total_duration_sec=0.0
            )

        return summaries

    def save_aggregate_report(
        self,
        results: List[SkillEvalResult],
        summaries: Dict[str, DomainSummary],
        session_id: str = "batch_eval"
    ):
        """
        Save aggregate evaluation report.

        Args:
            results: List of skill evaluation results
            summaries: Domain summaries
            session_id: Session identifier
        """
        # JSON report
        json_path = self.report_dir / f'{session_id}_aggregate.json'
        with open(json_path, 'w') as f:
            json.dump({
                'session_id': session_id,
                'timestamp': datetime.now().isoformat(),
                'total_skills': len(results),
                'successful': sum(1 for r in results if r.success),
                'failed': sum(1 for r in results if not r.success),
                'domains': {d: asdict(s) for d, s in summaries.items()},
                'results': [asdict(r) for r in results]
            }, f, indent=2)

        # Markdown report
        md_path = self.report_dir / f'{session_id}_aggregate.md'
        with open(md_path, 'w') as f:
            f.write(f"# Batch Evaluation Report: {session_id}\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Overall summary
            total = len(results)
            successful = sum(1 for r in results if r.success)
            failed = total - successful

            f.write("## Overall Summary\n\n")
            f.write(f"- **Total Skills**: {total}\n")
            f.write(f"- **Successful**: {successful} ({successful/max(total,1):.1%})\n")
            f.write(f"- **Failed**: {failed} ({failed/max(total,1):.1%})\n")
            f.write(f"- **Domains**: {len(summaries)}\n\n")

            # Domain breakdown
            f.write("## Domain Breakdown\n\n")
            f.write("| Domain | Total | Success | Failed | Avg Success Rate | Avg Auto-Act Rate |\n")
            f.write("|--------|-------|---------|--------|------------------|-------------------|\n")

            for domain in sorted(summaries.keys()):
                summary = summaries[domain]
                f.write(f"| {domain} | {summary.total_skills} | {summary.successful} | {summary.failed} | "
                       f"{summary.avg_success_rate:.1%} | {summary.avg_auto_act_rate:.1%} |\n")

            # Failed skills
            failed_results = [r for r in results if not r.success]
            if failed_results:
                f.write("\n## Failed Skills\n\n")
                f.write("| Skill ID | Domain | Error |\n")
                f.write("|----------|--------|-------|\n")
                for result in failed_results:
                    error_msg = result.error[:50] if result.error else "Unknown"
                    f.write(f"| {result.skill_id} | {result.domain} | {error_msg} |\n")

        print(f"\nAggregate reports saved:")
        print(f"  Markdown: {md_path}")
        print(f"  JSON: {json_path}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Batch evaluation for multiple skills',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Evaluate all skills in ecosystem domain
  python scripts/batch_eval_skills.py --domain ecosystem

  # Evaluate multiple domains in parallel
  python scripts/batch_eval_skills.py --domains ecosystem,marketing,revops --parallel 10

  # Evaluate specific skills
  python scripts/batch_eval_skills.py --skills elg_mdf_tracker,elg_partner_tier_manager

  # Generate test data only
  python scripts/batch_eval_skills.py --domain ecosystem --generate-only

  # Use existing test data
  python scripts/batch_eval_skills.py --domain ecosystem --use-existing-test-data
        """
    )

    parser.add_argument('--domain', help='Single domain to evaluate')
    parser.add_argument('--domains', help='Comma-separated list of domains')
    parser.add_argument('--skills', help='Comma-separated list of skill IDs')
    parser.add_argument('--parallel', type=int, default=5, help='Number of parallel evaluations')
    parser.add_argument('--test-data-dir', default='test_cases', help='Test data directory')
    parser.add_argument('--report-dir', default='reports/evals', help='Report output directory')
    parser.add_argument('--use-existing-test-data', action='store_true', help='Use existing test data')
    parser.add_argument('--generate-only', action='store_true', help='Only generate test data')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Parse domains and skills
    domains = None
    if args.domains:
        domains = [d.strip() for d in args.domains.split(',')]
    elif args.domain:
        domains = [args.domain]

    skill_ids = None
    if args.skills:
        skill_ids = [s.strip() for s in args.skills.split(',')]

    if not domains and not skill_ids:
        print("Error: Must specify --domain, --domains, or --skills")
        sys.exit(1)

    # Initialize evaluator
    project_root = Path(__file__).parent.parent
    evaluator = BatchSkillEvaluator(
        skills_library_path=project_root / 'skills-library',
        test_data_dir=Path(args.test_data_dir),
        report_dir=Path(args.report_dir),
        parallel=args.parallel,
        verbose=args.verbose
    )

    # Generate test data only
    if args.generate_only:
        print("Generating test data only...")
        discovered_skills = evaluator.discover_skills(domains=domains, skill_ids=skill_ids)
        total_skills = sum(len(skills) for skills in discovered_skills.values())

        all_skill_ids = []
        for skill_list in discovered_skills.values():
            all_skill_ids.extend(skill_list)

        evaluator.generator.generate_batch(
            skill_ids=all_skill_ids,
            cases_per_skill=3,
            output_dir=evaluator.test_data_dir
        )
        print(f"Generated test data for {total_skills} skills in {args.test_data_dir}")
        return

    # Run batch evaluation
    print(f"\n{'='*60}")
    print(f"Batch Skill Evaluation")
    print(f"{'='*60}")
    print(f"Parallel workers: {args.parallel}")
    print(f"Test data dir: {args.test_data_dir}")
    print(f"Report dir: {args.report_dir}")

    results = evaluator.evaluate_batch(
        domains=domains,
        skill_ids=skill_ids,
        use_existing_test_data=args.use_existing_test_data
    )

    # Generate summaries
    summaries = evaluator.generate_domain_summary(results)

    # Save aggregate report
    session_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    evaluator.save_aggregate_report(results, summaries, session_id)

    # Print summary
    print(f"\n{'='*60}")
    print("Evaluation Complete")
    print(f"{'='*60}")
    successful = sum(1 for r in results if r.success)
    print(f"Total: {len(results)}, Successful: {successful}, Failed: {len(results) - successful}")
    print(f"Success Rate: {successful/max(len(results),1):.1%}")


if __name__ == '__main__':
    main()
