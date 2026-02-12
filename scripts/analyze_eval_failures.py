#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Failure analysis tool for evaluation harness results.

Analyzes failed evaluations, categorizes failures, and generates actionable recommendations.

Usage:
    # Analyze failures from batch eval session
    python scripts/analyze_eval_failures.py --session batch_20260211_123456

    # Analyze specific domain failures
    python scripts/analyze_eval_failures.py --domain ecosystem

    # Generate prioritized fix list
    python scripts/analyze_eval_failures.py --session batch_20260211_123456 --prioritize

    # Export failures to CSV
    python scripts/analyze_eval_failures.py --session batch_20260211_123456 --export failures.csv
"""

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class FailureCategory:
    """Category of failure with patterns and recommendations."""

    category: str
    description: str
    pattern: str
    fix_recommendation: str
    estimated_effort: str  # "Low", "Medium", "High"
    priority: int  # 1-5, 5 = highest


@dataclass
class AnalyzedFailure:
    """Analyzed failure with categorization."""

    skill_id: str
    domain: str
    error: str
    category: str
    fix_recommendation: str
    priority: int
    estimated_effort: str


class FailureAnalyzer:
    """
    Analyzes evaluation failures and categorizes them.
    """

    # Predefined failure categories
    CATEGORIES = [
        FailureCategory(
            category="schema_missing",
            description="Skill missing inputSchema or outputSchema",
            pattern=r"(schema.*not found|no.*schema)",
            fix_recommendation="Add inputSchema and outputSchema to skill.json",
            estimated_effort="Low",
            priority=5,
        ),
        FailureCategory(
            category="schema_invalid",
            description="Schema definition is invalid JSON Schema",
            pattern=r"(invalid.*schema|schema.*validation.*failed)",
            fix_recommendation="Fix schema definition to conform to JSON Schema spec",
            estimated_effort="Low",
            priority=4,
        ),
        FailureCategory(
            category="skill_not_found",
            description="Skill directory or skill.json not found",
            pattern=r"(skill not found|file not found|does not exist)",
            fix_recommendation="Verify skill directory structure and skill.json exists",
            estimated_effort="Low",
            priority=5,
        ),
        FailureCategory(
            category="metadata_missing",
            description="Missing metadata.yaml or security.risk_level",
            pattern=r"(metadata.*not found|risk_level.*not found)",
            fix_recommendation="Add metadata.yaml with security.risk_level field",
            estimated_effort="Low",
            priority=4,
        ),
        FailureCategory(
            category="test_data_generation",
            description="Failed to generate test data from schema",
            pattern=r"(test.*data.*generation.*failed|no test cases generated)",
            fix_recommendation="Review schema complexity; may need manual test cases",
            estimated_effort="Medium",
            priority=3,
        ),
        FailureCategory(
            category="validation_error",
            description="Validation logic error (not schema issue)",
            pattern=r"(validation.*error|validator.*failed)",
            fix_recommendation="Check validator implementation for bugs",
            estimated_effort="Medium",
            priority=3,
        ),
        FailureCategory(
            category="execution_error",
            description="Error during skill execution",
            pattern=r"(execution.*failed|runtime.*error)",
            fix_recommendation="Investigate skill logic or test harness integration",
            estimated_effort="High",
            priority=2,
        ),
        FailureCategory(
            category="permission_error",
            description="File permission or access error",
            pattern=r"(permission denied|access denied)",
            fix_recommendation="Check file permissions in skills library",
            estimated_effort="Low",
            priority=4,
        ),
        FailureCategory(
            category="json_parse_error",
            description="Failed to parse JSON file",
            pattern=r"(json.*decode.*error|invalid.*json|expecting.*value)",
            fix_recommendation="Fix malformed JSON in skill.json or test data",
            estimated_effort="Low",
            priority=5,
        ),
        FailureCategory(
            category="unknown",
            description="Uncategorized failure",
            pattern=r".*",
            fix_recommendation="Manual investigation required",
            estimated_effort="Medium",
            priority=1,
        ),
    ]

    def __init__(self, report_dir: Path):
        """
        Initialize failure analyzer.

        Args:
            report_dir: Directory containing evaluation reports
        """
        self.report_dir = Path(report_dir)

    def load_failures_from_session(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Load failures from batch evaluation session.

        Args:
            session_id: Session identifier

        Returns:
            List of failure dictionaries
        """
        # Load aggregate JSON report
        json_path = self.report_dir / f"{session_id}_aggregate.json"

        if not json_path.exists():
            raise FileNotFoundError(f"Session report not found: {json_path}")

        with open(json_path, "r") as f:
            data = json.load(f)

        # Extract failed results
        results = data.get("results", [])
        failures = [r for r in results if not r.get("success", False)]

        return failures

    def load_failures_from_domain(self, domain: str) -> List[Dict[str, Any]]:
        """
        Load all failures for a specific domain.

        Args:
            domain: Domain name

        Returns:
            List of failure dictionaries
        """
        failures = []

        # Search all aggregate reports for domain failures
        for json_file in self.report_dir.glob("*_aggregate.json"):
            with open(json_file, "r") as f:
                data = json.load(f)

            results = data.get("results", [])
            domain_failures = [
                r for r in results if r.get("domain") == domain and not r.get("success", False)
            ]
            failures.extend(domain_failures)

        return failures

    def categorize_failure(self, error_message: str) -> FailureCategory:
        """
        Categorize a failure based on error message.

        Args:
            error_message: Error message text

        Returns:
            FailureCategory matching the error
        """
        error_lower = error_message.lower()

        for category in self.CATEGORIES:
            if re.search(category.pattern, error_lower, re.IGNORECASE):
                return category

        # Default to unknown
        return self.CATEGORIES[-1]

    def analyze_failures(self, failures: List[Dict[str, Any]]) -> List[AnalyzedFailure]:
        """
        Analyze and categorize failures.

        Args:
            failures: List of failure dictionaries

        Returns:
            List of AnalyzedFailure objects
        """
        analyzed = []

        for failure in failures:
            skill_id = failure.get("skill_id", "unknown")
            domain = failure.get("domain", "unknown")
            error = failure.get("error", "No error message")

            category = self.categorize_failure(error)

            analyzed.append(
                AnalyzedFailure(
                    skill_id=skill_id,
                    domain=domain,
                    error=error,
                    category=category.category,
                    fix_recommendation=category.fix_recommendation,
                    priority=category.priority,
                    estimated_effort=category.estimated_effort,
                )
            )

        return analyzed

    def generate_summary_stats(self, analyzed_failures: List[AnalyzedFailure]) -> Dict[str, Any]:
        """
        Generate summary statistics for failures.

        Args:
            analyzed_failures: List of analyzed failures

        Returns:
            Dictionary with summary statistics
        """
        total = len(analyzed_failures)

        # Count by category
        category_counts = Counter(f.category for f in analyzed_failures)

        # Count by domain
        domain_counts = Counter(f.domain for f in analyzed_failures)

        # Count by priority
        priority_counts = Counter(f.priority for f in analyzed_failures)

        # Count by effort
        effort_counts = Counter(f.estimated_effort for f in analyzed_failures)

        return {
            "total_failures": total,
            "by_category": dict(category_counts.most_common()),
            "by_domain": dict(domain_counts.most_common()),
            "by_priority": dict(sorted(priority_counts.items(), reverse=True)),
            "by_effort": dict(effort_counts.most_common()),
        }

    def generate_action_plan(
        self, analyzed_failures: List[AnalyzedFailure], prioritize: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Generate actionable fix plan.

        Args:
            analyzed_failures: List of analyzed failures
            prioritize: Sort by priority

        Returns:
            List of action items
        """
        # Group by category and fix recommendation
        action_items = defaultdict(list)

        for failure in analyzed_failures:
            key = (failure.category, failure.fix_recommendation)
            action_items[key].append(failure)

        # Convert to list of action items
        actions = []
        for (category, recommendation), failures in action_items.items():
            priority = max(f.priority for f in failures)
            effort = failures[0].estimated_effort

            actions.append(
                {
                    "category": category,
                    "fix_recommendation": recommendation,
                    "affected_skills": len(failures),
                    "skill_ids": [f.skill_id for f in failures],
                    "domains": list(set(f.domain for f in failures)),
                    "priority": priority,
                    "estimated_effort": effort,
                }
            )

        # Sort by priority if requested
        if prioritize:
            actions.sort(key=lambda x: (-x["priority"], x["affected_skills"]), reverse=True)

        return actions

    def save_analysis_report(
        self,
        analyzed_failures: List[AnalyzedFailure],
        summary_stats: Dict[str, Any],
        action_plan: List[Dict[str, Any]],
        output_path: Path,
    ):
        """
        Save analysis report as Markdown.

        Args:
            analyzed_failures: List of analyzed failures
            summary_stats: Summary statistics
            action_plan: Action plan items
            output_path: Output file path
        """
        with open(output_path, "w") as f:
            f.write("# Evaluation Failure Analysis\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Summary statistics
            f.write("## Summary Statistics\n\n")
            f.write(f"- **Total Failures**: {summary_stats['total_failures']}\n\n")

            # By category
            f.write("### Failures by Category\n\n")
            f.write("| Category | Count | Percentage |\n")
            f.write("|----------|-------|------------|\n")
            total = summary_stats["total_failures"]
            for category, count in summary_stats["by_category"].items():
                pct = count / max(total, 1) * 100
                f.write(f"| {category} | {count} | {pct:.1f}% |\n")

            # By domain
            f.write("\n### Failures by Domain\n\n")
            f.write("| Domain | Count |\n")
            f.write("|--------|-------|\n")
            for domain, count in list(summary_stats["by_domain"].items())[:10]:
                f.write(f"| {domain} | {count} |\n")

            # Action plan
            f.write("\n## Action Plan (Prioritized)\n\n")
            for idx, action in enumerate(action_plan, 1):
                f.write(f"### {idx}. {action['category'].replace('_', ' ').title()}\n\n")
                f.write(f"**Priority**: {action['priority']}/5 | ")
                f.write(f"**Effort**: {action['estimated_effort']} | ")
                f.write(f"**Affected Skills**: {action['affected_skills']}\n\n")
                f.write(f"**Fix**: {action['fix_recommendation']}\n\n")
                f.write(f"**Domains**: {', '.join(action['domains'])}\n\n")

                if action["affected_skills"] <= 10:
                    f.write(f"**Skills**: {', '.join(action['skill_ids'])}\n\n")
                else:
                    f.write(
                        f"**Skills**: {', '.join(action['skill_ids'][:10])} (and {action['affected_skills'] - 10} more)\n\n"
                    )

            # Detailed failure list
            f.write("\n## Detailed Failure List\n\n")
            f.write("| Skill ID | Domain | Category | Error (first 50 chars) |\n")
            f.write("|----------|--------|----------|------------------------|\n")

            for failure in analyzed_failures[:100]:  # Limit to 100
                error_short = failure.error[:50].replace("|", "-")
                f.write(
                    f"| {failure.skill_id} | {failure.domain} | {failure.category} | {error_short} |\n"
                )

        print(f"Analysis report saved: {output_path}")

    def export_to_csv(self, analyzed_failures: List[AnalyzedFailure], output_path: Path):
        """
        Export failures to CSV.

        Args:
            analyzed_failures: List of analyzed failures
            output_path: Output CSV path
        """
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "skill_id",
                    "domain",
                    "category",
                    "priority",
                    "estimated_effort",
                    "fix_recommendation",
                    "error",
                ],
            )
            writer.writeheader()

            for failure in analyzed_failures:
                writer.writerow(asdict(failure))

        print(f"Failures exported to CSV: {output_path}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze evaluation failures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze batch eval session
  python scripts/analyze_eval_failures.py --session batch_20260211_123456

  # Analyze domain failures
  python scripts/analyze_eval_failures.py --domain ecosystem

  # Generate prioritized action plan
  python scripts/analyze_eval_failures.py --session batch_20260211_123456 --prioritize

  # Export to CSV
  python scripts/analyze_eval_failures.py --session batch_20260211_123456 --export failures.csv
        """,
    )

    parser.add_argument("--session", help="Batch eval session ID")
    parser.add_argument("--domain", help="Analyze specific domain")
    parser.add_argument("--report-dir", default="reports/evals", help="Report directory")
    parser.add_argument("--prioritize", action="store_true", help="Prioritize action plan")
    parser.add_argument("--export", help="Export failures to CSV")
    parser.add_argument("--output", help="Output report path")

    args = parser.parse_args()

    if not args.session and not args.domain:
        print("Error: Must specify --session or --domain")
        sys.exit(1)

    # Initialize analyzer
    analyzer = FailureAnalyzer(report_dir=Path(args.report_dir))

    # Load failures
    print("Loading failures...")
    if args.session:
        failures = analyzer.load_failures_from_session(args.session)
        report_name = f"failure_analysis_{args.session}"
    else:
        failures = analyzer.load_failures_from_domain(args.domain)
        report_name = f"failure_analysis_{args.domain}"

    if not failures:
        print("No failures found!")
        return

    print(f"Found {len(failures)} failures")

    # Analyze failures
    print("Analyzing failures...")
    analyzed = analyzer.analyze_failures(failures)

    # Generate summary
    summary = analyzer.generate_summary_stats(analyzed)

    # Generate action plan
    action_plan = analyzer.generate_action_plan(analyzed, prioritize=args.prioritize)

    # Save report
    output_path = Path(args.output) if args.output else Path(args.report_dir) / f"{report_name}.md"
    analyzer.save_analysis_report(analyzed, summary, action_plan, output_path)

    # Export CSV if requested
    if args.export:
        analyzer.export_to_csv(analyzed, Path(args.export))

    # Print summary
    print(f"\n{'='*60}")
    print("Failure Analysis Complete")
    print(f"{'='*60}")
    print(f"Total Failures: {summary['total_failures']}")
    print(f"\nTop Categories:")
    for category, count in list(summary["by_category"].items())[:5]:
        print(f"  {category}: {count}")
    print(f"\nAction Items: {len(action_plan)}")
    print(f"Report: {output_path}")


if __name__ == "__main__":
    main()
