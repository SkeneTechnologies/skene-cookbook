#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Remediation Tracker Generator
Creates a prioritized task list for skill remediation with detailed analysis
"""

import json
import os
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import yaml


class RemediationPlanner:
    """Generates remediation plans for high-risk skills"""

    def __init__(self, skills_library_path="skills-library"):
        self.skills_library_path = Path(skills_library_path)
        self.skills = []
        self.remediation_tasks = []

    def load_all_skills(self):
        """Load all skills with their metadata"""
        print("📥 Loading skill metadata...")

        for skill_dir in self.skills_library_path.rglob("skill.json"):
            metadata_path = skill_dir.parent / "metadata.yaml"

            if not metadata_path.exists():
                continue

            with open(skill_dir, "r") as f:
                skill_data = json.load(f)

            with open(metadata_path, "r") as f:
                metadata = yaml.safe_load(f)

            self.skills.append(
                {
                    "skill_id": skill_data.get("id"),
                    "name": skill_data.get("name"),
                    "domain": skill_data.get("domain"),
                    "path": str(skill_dir.parent),
                    "risk_level": metadata["security"]["risk_level"],
                    "risk_factors": metadata["security"]["requirements"]["risk_factors"],
                    "requires_hitl": metadata["security"]["requirements"]["human_in_loop_required"],
                    "job_function": metadata["categorization"]["job_function"],
                }
            )

        print(f"✅ Loaded {len(self.skills)} skills")

    def analyze_remediations(self):
        """Analyze and categorize remediation needs"""
        print("\n🔍 Analyzing remediation opportunities...")

        for skill in self.skills:
            if skill["risk_level"] in ["Critical", "High"]:
                remediation = self._determine_remediation(skill)
                self.remediation_tasks.append(remediation)

        print(f"✅ Identified {len(self.remediation_tasks)} skills needing remediation")

    def _determine_remediation(self, skill):
        """Determine remediation strategy for a skill"""
        risk_factors = skill["risk_factors"]

        # Determine phase and category
        phase = self._determine_phase(skill, risk_factors)
        category = self._determine_category(risk_factors)
        effort = self._estimate_effort(phase, category)
        priority = self._calculate_priority(skill, phase, effort)
        strategy = self._recommend_strategy(category, risk_factors)

        return {
            "skill_id": skill["skill_id"],
            "name": skill["name"],
            "domain": skill["domain"],
            "path": skill["path"],
            "current_risk": skill["risk_level"],
            "target_risk": self._determine_target_risk(category, strategy),
            "phase": phase,
            "category": category,
            "effort_hours": effort,
            "priority_score": priority,
            "strategy": strategy,
            "risk_factors": risk_factors,
            "recommended_actions": self._generate_actions(category, risk_factors),
            "job_function": skill["job_function"],
        }

    def _determine_phase(self, skill, risk_factors):
        """Determine which phase this remediation belongs to"""
        # Phase 1: Quick wins
        if self._is_false_positive(risk_factors):
            return 1
        if self._is_easy_scoping(risk_factors):
            return 1

        # Phase 2: Medium effort
        if any(f in ["credential", "secret", "api_key", "password"] for f in risk_factors):
            return 2
        if any(f in ["payment", "financial"] for f in risk_factors):
            return 2
        if any(f in ["pii", "personal"] for f in risk_factors):
            return 2

        # Phase 3: Complex
        if any(f in ["delete", "drop", "truncate", "destroy"] for f in risk_factors):
            return 3
        if any(f in ["execute", "command", "shell", "eval"] for f in risk_factors):
            return 3
        if "external_api_calls" in risk_factors:
            return 3

        # Phase 4: Risk acceptance
        return 4

    def _determine_category(self, risk_factors):
        """Categorize the type of remediation needed"""
        if any(f in ["credential", "secret", "api_key", "password"] for f in risk_factors):
            return "credential_elimination"
        if any(f in ["payment", "financial"] for f in risk_factors):
            return "payment_hardening"
        if any(f in ["delete", "drop", "truncate", "destroy", "remove"] for f in risk_factors):
            return "destructive_operations"
        if any(f in ["execute", "command", "shell", "eval"] for f in risk_factors):
            return "system_commands"
        if "external_api_calls" in risk_factors:
            return "external_api"
        if any(f in ["pii", "personal", "sensitive"] for f in risk_factors):
            return "data_access_scoping"
        if any(f in ["write", "update", "modify", "change"] for f in risk_factors):
            return "write_operations"
        return "false_positive"

    def _estimate_effort(self, phase, category):
        """Estimate effort in hours"""
        effort_map = {
            1: {"false_positive": 1, "easy_scoping": 2},
            2: {"credential_elimination": 4, "payment_hardening": 5, "data_access_scoping": 3},
            3: {"destructive_operations": 8, "system_commands": 10, "external_api": 6},
            4: {"risk_acceptance": 3},
        }
        return effort_map.get(phase, {}).get(category, 5)

    def _calculate_priority(self, skill, phase, effort):
        """Calculate priority score (higher = more urgent)"""
        score = 0

        # Phase 1 highest priority (quick wins)
        score += (5 - phase) * 20

        # Critical risk higher than High
        if skill["risk_level"] == "Critical":
            score += 30
        else:
            score += 20

        # Lower effort = higher priority (quick wins)
        score += max(0, 10 - effort)

        # Certain categories get bonus priority
        critical_categories = [
            "credential_elimination",
            "destructive_operations",
            "payment_hardening",
        ]
        category = self._determine_category(skill["risk_factors"])
        if category in critical_categories:
            score += 15

        return score

    def _is_false_positive(self, risk_factors):
        """Check if likely a false positive"""
        # Simple heuristic: only low-risk keywords
        low_risk = [
            "list",
            "search",
            "filter",
            "sort",
            "format",
            "calculate",
            "view",
            "show",
            "display",
        ]
        return all(f in low_risk for f in risk_factors if f in low_risk)

    def _is_easy_scoping(self, risk_factors):
        """Check if easy to scope down"""
        read_only = ["read", "get", "fetch", "retrieve", "query"]
        return any(f in read_only for f in risk_factors) and not any(
            f in ["write", "update", "delete"] for f in risk_factors
        )

    def _determine_target_risk(self, category, strategy):
        """Determine target risk level after remediation"""
        targets = {
            "false_positive": "Low",
            "easy_scoping": "Low",
            "credential_elimination": "Medium",
            "data_access_scoping": "Medium",
            "write_operations": "Medium",
            "payment_hardening": "High",
            "destructive_operations": "High",
            "system_commands": "Medium",
            "external_api": "Medium",
        }
        return targets.get(category, "High")

    def _recommend_strategy(self, category, risk_factors):
        """Recommend remediation strategy"""
        strategies = {
            "false_positive": "Review and correct risk classification",
            "easy_scoping": "Convert to read-only, remove write permissions",
            "credential_elimination": "Implement OAuth delegation, remove credential handling",
            "payment_hardening": "Add two-phase commit, preview mode, per-transaction approval",
            "data_access_scoping": "Implement field-level access control, add filters",
            "destructive_operations": "Replace with soft delete, add undelete capability",
            "system_commands": "Sandbox execution, whitelist commands, add resource limits",
            "external_api": "Add API gateway, rate limiting, circuit breakers",
            "write_operations": "Add validation, preview mode, rollback capability",
        }
        return strategies.get(category, "Review and determine appropriate strategy")

    def _generate_actions(self, category, risk_factors):
        """Generate specific action items"""
        actions = {
            "false_positive": [
                "Manual review of skill operations",
                "Verify risk factors are accurate",
                "Update metadata.yaml with correct risk level",
                "Re-run security analysis",
            ],
            "credential_elimination": [
                "Replace direct credential handling with OAuth",
                "Implement token exchange pattern",
                "Remove credential storage from skill.json",
                "Update documentation",
                "Test with OAuth flow",
            ],
            "payment_hardening": [
                "Implement preview/dry-run mode",
                "Add per-transaction approval (not per-skill)",
                "Implement rollback capability",
                "Add amount limits and guardrails",
                "Add transaction logging",
            ],
            "destructive_operations": [
                "Replace hard delete with soft delete (archive)",
                "Add undelete capability (30-day window)",
                "Implement multi-party approval",
                "Add backup before delete",
                "Require explicit confirmation",
            ],
            "system_commands": [
                "Containerize execution environment",
                "Implement command whitelist",
                "Add resource limits (CPU, memory, time)",
                "Disable network access unless required",
                "Run as non-privileged user",
            ],
            "external_api": [
                "Route through API gateway",
                "Implement rate limiting",
                "Add circuit breaker pattern",
                "Add request/response validation",
                "Implement response caching",
            ],
            "data_access_scoping": [
                "Implement field-level access control",
                "Add tenant isolation filters",
                "Scope to specific data types only",
                "Add time-based access windows",
                "Remove unnecessary data access",
            ],
        }
        return actions.get(category, ["Review and determine specific actions needed"])

    def generate_tracker(self, output_path="reports/remediation_tracker.md"):
        """Generate markdown tracker with all remediation tasks"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Sort by priority
        sorted_tasks = sorted(
            self.remediation_tasks, key=lambda x: x["priority_score"], reverse=True
        )

        # Group by phase
        by_phase = defaultdict(list)
        for task in sorted_tasks:
            by_phase[task["phase"]].append(task)

        with open(output_path, "w") as f:
            f.write("# Skills Remediation Tracker\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Summary
            f.write("## Summary\n\n")
            f.write(f"**Total Skills to Remediate:** {len(sorted_tasks)}\n\n")
            f.write("| Phase | Skills | Estimated Hours | Priority Range |\n")
            f.write("|-------|--------|-----------------|----------------|\n")

            for phase in sorted([1, 2, 3, 4]):
                tasks = by_phase[phase]
                total_hours = sum(t["effort_hours"] for t in tasks)
                if tasks:
                    priority_range = f"{min(t['priority_score'] for t in tasks)}-{max(t['priority_score'] for t in tasks)}"
                else:
                    priority_range = "N/A"
                f.write(f"| Phase {phase} | {len(tasks)} | {total_hours}h | {priority_range} |\n")

            f.write("\n")

            # By category
            by_category = defaultdict(list)
            for task in sorted_tasks:
                by_category[task["category"]].append(task)

            f.write("## By Category\n\n")
            f.write("| Category | Count | Total Hours |\n")
            f.write("|----------|-------|-------------|\n")
            for category, tasks in sorted(
                by_category.items(), key=lambda x: len(x[1]), reverse=True
            ):
                total_hours = sum(t["effort_hours"] for t in tasks)
                f.write(f"| {category} | {len(tasks)} | {total_hours}h |\n")

            f.write("\n")

            # Detailed tasks by phase
            phase_names = {
                1: "Phase 1: Quick Wins (Weeks 1-2)",
                2: "Phase 2: Medium Effort (Weeks 3-6)",
                3: "Phase 3: Complex Remediation (Weeks 7-10)",
                4: "Phase 4: Risk Acceptance (Weeks 11-12)",
            }

            for phase in sorted([1, 2, 3, 4]):
                tasks = by_phase[phase]
                if not tasks:
                    continue

                f.write(f"\n## {phase_names[phase]}\n\n")
                f.write(f"**Skills in Phase:** {len(tasks)}\n")
                f.write(f"**Total Effort:** {sum(t['effort_hours'] for t in tasks)} hours\n\n")

                for i, task in enumerate(tasks, 1):
                    f.write(f"### {i}. {task['name']} ({task['skill_id']})\n\n")
                    f.write(f"- **Priority Score:** {task['priority_score']}\n")
                    f.write(f"- **Current Risk:** {task['current_risk']}\n")
                    f.write(f"- **Target Risk:** {task['target_risk']}\n")
                    f.write(f"- **Category:** {task['category']}\n")
                    f.write(f"- **Effort:** {task['effort_hours']} hours\n")
                    f.write(f"- **Domain:** {task['domain']}\n")
                    f.write(f"- **Job Function:** {task['job_function']}\n")
                    f.write(f"- **Path:** `{task['path']}`\n\n")

                    f.write(f"**Strategy:**\n{task['strategy']}\n\n")

                    f.write("**Risk Factors:**\n")
                    for factor in task["risk_factors"][:10]:  # Limit to top 10
                        f.write(f"- {factor}\n")
                    f.write("\n")

                    f.write("**Recommended Actions:**\n")
                    for action in task["recommended_actions"]:
                        f.write(f"- [ ] {action}\n")
                    f.write("\n")

                    f.write("**Status:** ⏳ Not Started\n\n")
                    f.write("---\n\n")

        print(f"\n✅ Remediation tracker generated: {output_path}")

    def generate_csv(self, output_path="reports/remediation_tracker.csv"):
        """Generate CSV for project management tools"""
        import csv

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        sorted_tasks = sorted(
            self.remediation_tasks, key=lambda x: x["priority_score"], reverse=True
        )

        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "skill_id",
                    "name",
                    "domain",
                    "phase",
                    "priority_score",
                    "current_risk",
                    "target_risk",
                    "category",
                    "effort_hours",
                    "strategy",
                    "status",
                    "assigned_to",
                    "path",
                ],
            )
            writer.writeheader()

            for task in sorted_tasks:
                writer.writerow(
                    {
                        "skill_id": task["skill_id"],
                        "name": task["name"],
                        "domain": task["domain"],
                        "phase": f"Phase {task['phase']}",
                        "priority_score": task["priority_score"],
                        "current_risk": task["current_risk"],
                        "target_risk": task["target_risk"],
                        "category": task["category"],
                        "effort_hours": task["effort_hours"],
                        "strategy": task["strategy"],
                        "status": "Not Started",
                        "assigned_to": "",
                        "path": task["path"],
                    }
                )

        print(f"✅ CSV tracker generated: {output_path}")

    def generate_summary_report(self):
        """Generate executive summary"""
        print("\n" + "=" * 60)
        print("  REMEDIATION PLAN EXECUTIVE SUMMARY")
        print("=" * 60)

        total_skills = len(self.remediation_tasks)
        total_hours = sum(t["effort_hours"] for t in self.remediation_tasks)

        by_phase = defaultdict(list)
        for task in self.remediation_tasks:
            by_phase[task["phase"]].append(task)

        print(f"\n📊 SCOPE")
        print(f"   Skills to Remediate: {total_skills}")
        print(f"   Total Effort: {total_hours} hours ({total_hours/40:.1f} FTE-weeks)")
        print(f"   Average per Skill: {total_hours/total_skills:.1f} hours")

        print(f"\n📅 PHASES")
        for phase in sorted([1, 2, 3, 4]):
            tasks = by_phase[phase]
            hours = sum(t["effort_hours"] for t in tasks)
            print(f"   Phase {phase}: {len(tasks)} skills, {hours}h")

        # Risk reduction
        current_critical = sum(1 for t in self.remediation_tasks if t["current_risk"] == "Critical")
        target_critical = sum(1 for t in self.remediation_tasks if t["target_risk"] == "Critical")
        reduction = current_critical - target_critical

        print(f"\n🎯 EXPECTED IMPACT")
        print(
            f"   Critical Skills: {current_critical} → {target_critical} (-{reduction}, -{reduction/current_critical*100:.0f}%)"
        )

        # Top categories
        by_category = defaultdict(list)
        for task in self.remediation_tasks:
            by_category[task["category"]].append(task)

        print(f"\n🔧 TOP CATEGORIES")
        for category, tasks in sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True)[
            :5
        ]:
            print(f"   {category}: {len(tasks)} skills")

        print("\n" + "=" * 60 + "\n")


def main():
    planner = RemediationPlanner()
    planner.load_all_skills()
    planner.analyze_remediations()
    planner.generate_tracker()
    planner.generate_csv()
    planner.generate_summary_report()

    print("✨ Remediation planning complete!\n")
    print("📄 Review the following files:")
    print("   - reports/remediation_tracker.md (detailed plan)")
    print("   - reports/remediation_tracker.csv (for project management)")
    print("\n🚀 Ready to begin Phase 1!")


if __name__ == "__main__":
    main()
