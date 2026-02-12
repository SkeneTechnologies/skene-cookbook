#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
CLI for running evaluation harness.

Usage:
    python scripts/run_eval_harness.py eval-skill --skill-id elg_mdf_tracker
    python scripts/run_eval_harness.py eval-workflow --workflow-id test_workflow
    python scripts/run_eval_harness.py eval-session --config eval_config.yaml
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from eval_harness.core import SkillValidator, SkillTracer, MetricsCollector, EvalSession
from eval_harness.instrumented_executor import InstrumentedSkillExecutor
from eval_harness.reporters import MarkdownReporter, JSONReporter
from eval_harness.core.eval_session import EvalConfig


def eval_skill(args):
    """Evaluate a single skill."""
    print(f"\n{'='*60}")
    print(f"Evaluating Skill: {args.skill_id}")
    print(f"{'='*60}\n")

    # Initialize components
    validator = SkillValidator()
    tracer = SkillTracer(provider='console')
    metrics_collector = MetricsCollector()
    executor = InstrumentedSkillExecutor(
        validator=validator,
        tracer=tracer,
        metrics_collector=metrics_collector
    )

    # Example: Simple test cases for demonstration
    test_cases = [
        {
            'partnerId': 'test-partner-123',
            'action': 'check_budget'
        },
        {
            'partnerId': 'test-partner-456',
            'action': 'request',
            'requestData': {'amount': 5000}
        },
        {
            'partnerId': 'test-partner-789',
            'action': 'report'
        }
    ]

    # Dummy skill logic (in real usage, this would be actual skill implementation)
    def dummy_skill_logic(inputs):
        return {
            'available_budget': 10000.0,
            'allocated': 5000.0,
            'spent': 2000.0
        }

    # Execute test cases
    for idx, test_case in enumerate(test_cases):
        print(f"\nTest Case {idx + 1}:")
        result = executor.execute_skill(
            skill_id=args.skill_id,
            skill_version='1.0.0',
            inputs=test_case,
            skill_logic=dummy_skill_logic
        )

        print(f"  Success: {result.success}")
        print(f"  Decision: {result.decision.type.value}")
        print(f"  Duration: {result.duration_ms:.2f}ms")
        if result.error:
            print(f"  Error: {result.error}")

    # Get aggregated metrics
    metrics = metrics_collector.get_aggregated_metrics(args.skill_id)

    if metrics:
        print(f"\n{'='*60}")
        print("Aggregated Metrics")
        print(f"{'='*60}")
        print(f"Success Rate: {metrics.success_rate:.1%}")
        print(f"Validation Pass Rate: {metrics.validation_pass_rate:.1%}")
        print(f"Auto-Act Rate: {metrics.auto_act_rate:.1%}")
        print(f"Avg Duration: {metrics.avg_duration_ms:.2f}ms")
        print(f"P95 Duration: {metrics.p95_duration_ms:.2f}ms")

        # Generate reports
        if args.report_dir:
            report_dir = Path(args.report_dir)
            md_reporter = MarkdownReporter(output_dir=report_dir)
            json_reporter = JSONReporter(output_dir=report_dir)

            md_path = md_reporter.save_skill_report(
                skill_id=args.skill_id,
                metrics=metrics,
                session_id='cli_eval'
            )
            json_path = json_reporter.save_skill_report(
                skill_id=args.skill_id,
                metrics=metrics,
                session_id='cli_eval'
            )

            print(f"\nReports saved:")
            print(f"  Markdown: {md_path}")
            print(f"  JSON: {json_path}")


def eval_workflow(args):
    """Evaluate a workflow."""
    print(f"Evaluating workflow: {args.workflow_id}")
    print("(Not yet implemented)")


def eval_session(args):
    """Run evaluation session from config."""
    print(f"Running eval session from: {args.config}")
    print("(Not yet implemented)")


def dashboard(args):
    """Generate evaluation dashboard."""
    print(f"Generating dashboard from: {args.session_dir}")
    print("(Not yet implemented)")


def ab_test(args):
    """Run A/B test between skill versions."""
    print(f"A/B testing {args.skill_id}: v{args.version_a} vs v{args.version_b}")
    print("(Not yet implemented)")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Evaluation Harness for skene-cookbook',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Evaluate single skill
  python scripts/run_eval_harness.py eval-skill --skill-id elg_mdf_tracker

  # Evaluate with reports
  python scripts/run_eval_harness.py eval-skill --skill-id elg_mdf_tracker \\
    --report-dir reports/evals/

  # Evaluate workflow
  python scripts/run_eval_harness.py eval-workflow --workflow-id test_workflow

  # Run eval session
  python scripts/run_eval_harness.py eval-session --config eval_config.yaml

  # Generate dashboard
  python scripts/run_eval_harness.py dashboard --session-dir reports/evals/sessions/

  # A/B test
  python scripts/run_eval_harness.py ab-test --skill-id elg_mdf_tracker \\
    --version-a 1.0.0 --version-b 1.1.0
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # eval-skill command
    parser_skill = subparsers.add_parser('eval-skill', help='Evaluate single skill')
    parser_skill.add_argument('--skill-id', required=True, help='Skill ID to evaluate')
    parser_skill.add_argument('--test-data', help='Path to test data JSON file')
    parser_skill.add_argument('--report-dir', help='Directory for reports')
    parser_skill.set_defaults(func=eval_skill)

    # eval-workflow command
    parser_workflow = subparsers.add_parser('eval-workflow', help='Evaluate workflow')
    parser_workflow.add_argument('--workflow-id', required=True, help='Workflow ID')
    parser_workflow.add_argument('--test-data', help='Path to test data JSON file')
    parser_workflow.set_defaults(func=eval_workflow)

    # eval-session command
    parser_session = subparsers.add_parser('eval-session', help='Run eval session')
    parser_session.add_argument('--config', required=True, help='Session config file')
    parser_session.set_defaults(func=eval_session)

    # dashboard command
    parser_dashboard = subparsers.add_parser('dashboard', help='Generate dashboard')
    parser_dashboard.add_argument('--session-dir', required=True, help='Session dir')
    parser_dashboard.add_argument('--output', help='Output HTML path')
    parser_dashboard.set_defaults(func=dashboard)

    # ab-test command
    parser_ab = subparsers.add_parser('ab-test', help='A/B test skill versions')
    parser_ab.add_argument('--skill-id', required=True, help='Skill ID')
    parser_ab.add_argument('--version-a', required=True, help='Version A')
    parser_ab.add_argument('--version-b', required=True, help='Version B')
    parser_ab.add_argument('--test-data', help='Path to test data JSON file')
    parser_ab.set_defaults(func=ab_test)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
