#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Intelligent Skill Chaining - Blueprint Generator
Analyzes I/O compatibility and generates workflow blueprints
"""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

import yaml


class ChainArchitect:
    """Intelligent skill chaining and blueprint generation"""

    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.skills_path = self.base_path / "skills-library"
        self.registry_path = self.base_path / "registry"
        self.blueprints_path = self.registry_path / "blueprints"

        self.skills = []
        self.skills_by_function = defaultdict(list)
        self.io_graph = defaultdict(list)  # Output type -> skills that produce it
        self.chainable_pairs = []
        self.missing_links = []

        self.blueprints_path.mkdir(parents=True, exist_ok=True)

    def load_skills(self):
        """Load all skills with their I/O information"""
        print("📥 Loading skills for chain analysis...")

        # Load from job functions index
        index_path = self.registry_path / "job_functions" / "index.json"
        with open(index_path, "r") as f:
            job_functions = json.load(f)

        total_skills = 0
        for function, skills in job_functions.items():
            self.skills_by_function[function] = skills
            total_skills += len(skills)

        # Load detailed skill data
        skill_files = list(self.skills_path.rglob("skill.json"))
        for skill_file in skill_files:
            try:
                with open(skill_file, "r") as f:
                    skill_data = json.load(f)

                # Extract I/O types
                input_types = self._extract_io_types(skill_data.get("inputSchema"))
                output_types = self._extract_io_types(skill_data.get("outputSchema"))

                skill_record = {
                    "skill_id": skill_data.get("id"),
                    "name": skill_data.get("name", ""),
                    "domain": skill_data.get("domain", ""),
                    "input_types": input_types,
                    "output_types": output_types,
                    "tools": skill_data.get("tools", []),
                    "exit_states": skill_data.get("exitStates", []),
                }

                self.skills.append(skill_record)

                # Build I/O graph
                for output_type in output_types:
                    self.io_graph[output_type].append(skill_record)

            except Exception as e:
                pass  # Skip problematic files

        print(f"   ✅ Loaded {len(self.skills)} skills")
        print(f"   📊 {len(job_functions)} job functions")
        print(f"   🔗 {len(self.io_graph)} unique output types")

    def _extract_io_types(self, schema: Dict) -> Set[str]:
        """Extract data types from JSON Schema"""
        if not schema:
            return set()

        types = set()

        # Get top-level type
        if "type" in schema:
            types.add(schema["type"])

        # Get property types
        if "properties" in schema:
            for prop_name, prop_schema in schema["properties"].items():
                if "type" in prop_schema:
                    types.add(prop_schema["type"])
                # Add semantic type hints from description
                if "description" in prop_schema and prop_schema["description"]:
                    desc = (prop_schema["description"] or "").lower()
                    if "file" in desc:
                        types.add("file")
                    if "url" in desc or "link" in desc:
                        types.add("url")
                    if "email" in desc:
                        types.add("email")
                    if "data" in desc:
                        types.add("data")

        return types

    def analyze_chainability(self):
        """Analyze which skills can be chained together"""
        print("\n🔗 Analyzing skill chainability...")

        # For each skill, find skills that can follow it
        for skill in self.skills:
            if not skill["output_types"]:
                continue

            compatible_followers = []

            for output_type in skill["output_types"]:
                # Find skills that accept this output type
                for potential_follower in self.skills:
                    if skill["skill_id"] == potential_follower["skill_id"]:
                        continue

                    if output_type in potential_follower["input_types"]:
                        compatible_followers.append(
                            {"skill": potential_follower, "connection_type": output_type}
                        )

            if compatible_followers:
                self.chainable_pairs.append(
                    {"producer": skill, "compatible_consumers": compatible_followers}
                )

        print(f"   ✅ Found {len(self.chainable_pairs)} chainable skill patterns")

    def identify_missing_links(self):
        """Identify gaps in the skill chain"""
        print("\n🔍 Identifying missing links...")

        # Common JTBD workflows
        common_workflows = {
            "data_analysis": ["extract", "transform", "analyze", "visualize"],
            "content_creation": ["research", "draft", "edit", "publish"],
            "customer_onboarding": ["signup", "verify", "setup", "activate"],
            "incident_response": ["detect", "triage", "remediate", "report"],
            "recruitment": ["source", "screen", "interview", "offer"],
        }

        # Check for missing steps
        for workflow_name, steps in common_workflows.items():
            missing_steps = []

            for step in steps:
                # Check if we have skills for this step
                matching_skills = [
                    s
                    for s in self.skills
                    if step.lower() in (s.get("name") or "").lower()
                    or step.lower() in (s.get("skill_id") or "").lower()
                ]

                if not matching_skills:
                    missing_steps.append(step)

            if missing_steps:
                self.missing_links.append(
                    {
                        "workflow": workflow_name,
                        "missing_steps": missing_steps,
                        "severity": (
                            "critical" if len(missing_steps) > len(steps) / 2 else "moderate"
                        ),
                    }
                )

        print(f"   ⚠️  Found {len(self.missing_links)} workflow gaps")

    def generate_function_blueprints(self):
        """Generate blueprint for each major job function"""
        print("\n📐 Generating job function blueprints...")

        # Priority job functions for blueprints
        priority_functions = ["engineering", "marketing", "customer_success", "sales", "data"]

        blueprints_created = 0

        for function in priority_functions:
            if function not in self.skills_by_function:
                continue

            skills = self.skills_by_function[function][:10]  # Top 10 skills

            # Create a sample workflow blueprint
            blueprint = self._create_function_blueprint(function, skills)

            if blueprint:
                output_path = self.blueprints_path / f"{function}_workflow.yaml"
                with open(output_path, "w") as f:
                    yaml.dump(blueprint, f, default_flow_style=False, sort_keys=False)

                print(f"   ✅ Created: {output_path.name}")
                blueprints_created += 1

        print(f"   📋 Generated {blueprints_created} blueprint files")

    def _create_function_blueprint(self, function: str, skills: List[Dict]) -> Dict:
        """Create a workflow blueprint for a job function"""

        # Define common workflows by function
        workflow_patterns = {
            "engineering": {
                "name": "Code Review & Deployment Pipeline",
                "description": "Automated code review, testing, and deployment workflow",
                "steps": ["code_review", "run_tests", "security_scan", "deploy"],
            },
            "marketing": {
                "name": "Content Marketing Campaign",
                "description": "Research, create, optimize, and distribute content",
                "steps": [
                    "keyword_research",
                    "content_creation",
                    "seo_optimization",
                    "distribution",
                ],
            },
            "customer_success": {
                "name": "Customer Health Monitoring",
                "description": "Monitor customer health, detect churn risk, and intervene",
                "steps": ["health_scoring", "churn_prediction", "intervention", "follow_up"],
            },
            "sales": {
                "name": "Lead Qualification Pipeline",
                "description": "Qualify, score, route, and follow up on leads",
                "steps": ["lead_scoring", "qualification", "routing", "follow_up"],
            },
            "data": {
                "name": "Data Analysis Pipeline",
                "description": "Extract, transform, analyze, and visualize data",
                "steps": ["extraction", "transformation", "analysis", "visualization"],
            },
        }

        if function not in workflow_patterns:
            return None

        pattern = workflow_patterns[function]

        # Build chain sequence
        chain_sequence = []
        for i, step_name in enumerate(pattern["steps"], 1):
            # Try to find a matching skill
            matching_skill = None
            for skill in skills:
                if any(
                    keyword in (skill.get("jtbd") or "").lower() for keyword in step_name.split("_")
                ):
                    matching_skill = skill
                    break

            if not matching_skill and skills:
                matching_skill = skills[min(i - 1, len(skills) - 1)]

            if matching_skill:
                step = {
                    "step_id": f"step_{i}_{step_name}",
                    "skill_id": matching_skill["skill_id"],
                    "action": "execute",
                    "description": f'Execute {step_name.replace("_", " ")}',
                    "timeout_seconds": 300,
                    "error_handling": {
                        "on_failure": "stop" if i < len(pattern["steps"]) / 2 else "continue",
                        "max_retries": 2,
                    },
                    "opinionated_prompts": {"system_context": "", "input_guidance": {}},
                }
                chain_sequence.append(step)

        blueprint = {
            "id": f"workflow_{function}_automated",
            "version": "1.0.0",
            "name": pattern["name"],
            "description": pattern["description"],
            "category": function.replace("_", " ").title(),
            "icp": {"name": "", "company": {}, "team": {}, "priorities": []},
            "integration_reference": {"description": "", "schemas": []},
            "chain_sequence": chain_sequence,
            "metadata": {
                "author": "Chain Architect",
                "created_at": datetime.now().isoformat(),
                "job_function": function,
                "auto_generated": True,
            },
        }

        return blueprint

    def generate_jtbd_blueprints(self):
        """Generate blueprints based on common Jobs-to-be-Done"""
        print("\n🎯 Generating JTBD-based blueprints...")

        jtbd_patterns = {
            "partner_onboarding": {
                "name": "Complete Partner Onboarding",
                "description": "End-to-end partner onboarding from signup to revenue tracking",
                "skill_sequence": [
                    "partner.*onboard",
                    "integration.*setup",
                    ".*health.*monitor",
                    "revenue.*track",
                ],
            },
            "customer_churn_prevention": {
                "name": "Proactive Churn Prevention",
                "description": "Detect at-risk customers and intervene",
                "skill_sequence": [
                    "health.*scor",
                    "churn.*predict",
                    ".*intervention",
                    ".*follow.*up",
                ],
            },
            "lead_to_revenue": {
                "name": "Lead to Revenue Pipeline",
                "description": "Capture, qualify, nurture, and close leads",
                "skill_sequence": ["lead.*captur", ".*qualification", ".*nurture", "deal.*clos"],
            },
        }

        blueprints_created = 0

        for jtbd_id, pattern in jtbd_patterns.items():
            # Find matching skills
            matched_skills = []
            for skill_pattern in pattern["skill_sequence"]:
                # Find skill matching pattern
                import re

                for skill in self.skills:
                    if re.search(skill_pattern, skill["skill_id"], re.IGNORECASE):
                        matched_skills.append(skill)
                        break

            if len(matched_skills) >= len(pattern["skill_sequence"]) / 2:
                blueprint = {
                    "id": f"workflow_{jtbd_id}",
                    "version": "1.0.0",
                    "name": pattern["name"],
                    "description": pattern["description"],
                    "category": "JTBD Workflow",
                    "icp": {"name": "", "company": {}, "team": {}, "priorities": []},
                    "integration_reference": {"description": "", "schemas": []},
                    "chain_sequence": [
                        {
                            "step_id": f"step_{i+1}",
                            "skill_id": skill["skill_id"],
                            "action": "execute",
                            "timeout_seconds": 300,
                            "opinionated_prompts": {"system_context": "", "input_guidance": {}},
                        }
                        for i, skill in enumerate(matched_skills)
                    ],
                    "metadata": {
                        "author": "Chain Architect",
                        "created_at": datetime.now().isoformat(),
                        "jtbd_pattern": jtbd_id,
                        "auto_generated": True,
                    },
                }

                output_path = self.blueprints_path / f"{jtbd_id}.yaml"
                with open(output_path, "w") as f:
                    yaml.dump(blueprint, f, default_flow_style=False, sort_keys=False)

                print(f"   ✅ Created: {output_path.name}")
                blueprints_created += 1

        print(f"   📋 Generated {blueprints_created} JTBD blueprints")

    def generate_chain_report(self):
        """Generate comprehensive chaining analysis report"""
        print("\n📊 Generating chain analysis report...")

        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_skills_analyzed": len(self.skills),
            },
            "summary": {
                "chainable_patterns": len(self.chainable_pairs),
                "missing_workflow_links": len(self.missing_links),
                "output_types_identified": len(self.io_graph),
                "job_functions": len(self.skills_by_function),
            },
            "chainability": {
                "patterns": self.chainable_pairs[:50],  # Top 50
                "io_graph": {k: [s["skill_id"] for s in v] for k, v in self.io_graph.items()},
            },
            "missing_links": self.missing_links,
            "recommendations": {
                "high_priority_skills_needed": [
                    link.get("missing_steps", [])
                    for link in self.missing_links
                    if link.get("severity") == "critical"
                ]
            },
        }

        report_path = self.base_path / "reports" / "chain_analysis.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"   ✅ Report saved: {report_path}")

        # Generate summary
        self._generate_chain_summary(report)

    def _generate_chain_summary(self, report):
        """Generate human-readable chain summary"""
        summary_path = self.base_path / "reports" / "chain_summary.md"

        with open(summary_path, "w") as f:
            f.write("# Skill Chain Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Summary\n\n")
            f.write(f"- **Total Skills:** {report['metadata']['total_skills_analyzed']}\n")
            f.write(f"- **Chainable Patterns:** {report['summary']['chainable_patterns']}\n")
            f.write(f"- **Missing Links:** {report['summary']['missing_workflow_links']}\n")
            f.write(f"- **Output Types:** {report['summary']['output_types_identified']}\n\n")

            f.write("## Chainability Analysis\n\n")
            f.write(
                f"Found {report['summary']['chainable_patterns']} skills that can be chained together.\n\n"
            )

            if self.chainable_pairs:
                f.write("### Example Chains\n\n")
                for i, pattern in enumerate(self.chainable_pairs[:10], 1):
                    f.write(f"**{i}. {pattern['producer']['name']}**\n")
                    f.write(f"   → Can chain to {len(pattern['compatible_consumers'])} skills:\n")
                    for consumer in pattern["compatible_consumers"][:3]:
                        f.write(
                            f"   - {consumer['skill']['name']} (via {consumer['connection_type']})\n"
                        )
                    f.write("\n")

            if self.missing_links:
                f.write("## ⚠️  Missing Links (Workflow Gaps)\n\n")
                for gap in self.missing_links:
                    severity_emoji = "🔴" if gap["severity"] == "critical" else "🟡"
                    f.write(f"### {severity_emoji} {gap['workflow'].replace('_', ' ').title()}\n\n")
                    f.write(f"**Missing Steps:** {', '.join(gap['missing_steps'])}\n\n")

            f.write("## Recommendations\n\n")
            f.write("1. Build missing workflow skills identified above\n")
            f.write("2. Add I/O schema definitions to enable better chaining\n")
            f.write("3. Test generated blueprints with real workflows\n")

        print(f"   ✅ Summary saved: {summary_path}")

    def print_summary(self):
        """Print summary to console"""
        print("\n" + "=" * 70)
        print("  SKILL CHAIN ANALYSIS COMPLETE")
        print("=" * 70)

        print(f"\n📊 RESULTS")
        print(f"   Skills Analyzed:          {len(self.skills)}")
        print(f"   Chainable Patterns:       {len(self.chainable_pairs)}")
        print(f"   Missing Workflow Links:   {len(self.missing_links)}")
        print(f"   Output Types:             {len(self.io_graph)}")

        print(f"\n🔗 BLUEPRINTS")
        blueprint_files = list(self.blueprints_path.glob("*.yaml"))
        print(f"   Total Blueprints: {len(blueprint_files)}")
        for bp in blueprint_files:
            print(f"   • {bp.name}")

        print("\n📁 REPORTS")
        print("   • reports/chain_analysis.json")
        print("   • reports/chain_summary.md")

        print("\n" + "=" * 70 + "\n")


def main():
    print("🔗 Intelligent Skill Chain Architect")
    print("=" * 70)

    architect = ChainArchitect()

    # Execute pipeline
    architect.load_skills()
    architect.analyze_chainability()
    architect.identify_missing_links()
    architect.generate_function_blueprints()
    architect.generate_jtbd_blueprints()
    architect.generate_chain_report()

    architect.print_summary()

    print("✅ Chain analysis complete!")
    print("\nNext: Review reports/chain_summary.md and registry/blueprints/")


if __name__ == "__main__":
    main()
