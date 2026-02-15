#!/usr/bin/env python3
"""
Simple eval runner for CI/CD integration.

Runs basic evaluations on skill execution and chain consistency.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def load_skill(skill_path: Path) -> Dict[str, Any]:
    """Load skill.json from a skill directory."""
    skill_json = skill_path / "skill.json"
    if not skill_json.exists():
        return None

    with open(skill_json) as f:
        return json.load(f)


def eval_skill_schema_validity(skills_dir: Path) -> Dict[str, Any]:
    """
    Eval: Verify all skills have valid schema structure.

    Checks:
    - skill.json exists
    - Required fields present (id, name, description, version, domain)
    - Valid risk_level values
    """
    results = {
        "eval_id": "skill-schema-validity",
        "total_skills": 0,
        "passed": 0,
        "failed": 0,
        "errors": [],
    }

    required_fields = ["id", "name", "description", "version", "domain"]
    valid_risk_levels = ["Low", "Medium", "High", "Critical"]

    # Find all skill.json files
    for skill_json_path in skills_dir.rglob("skill.json"):
        results["total_skills"] += 1

        try:
            with open(skill_json_path) as f:
                skill = json.load(f)

            # Check required fields
            missing_fields = [f for f in required_fields if f not in skill]
            if missing_fields:
                results["failed"] += 1
                results["errors"].append(
                    {
                        "skill": str(skill_json_path.relative_to(skills_dir)),
                        "error": f"Missing required fields: {', '.join(missing_fields)}",
                    }
                )
                continue

            # Check risk_level if present
            if "risk_level" in skill and skill["risk_level"] not in valid_risk_levels:
                results["failed"] += 1
                results["errors"].append(
                    {
                        "skill": str(skill_json_path.relative_to(skills_dir)),
                        "error": f"Invalid risk_level: {skill['risk_level']} (must be one of {valid_risk_levels})",
                    }
                )
                continue

            results["passed"] += 1

        except json.JSONDecodeError as e:
            results["failed"] += 1
            results["errors"].append(
                {
                    "skill": str(skill_json_path.relative_to(skills_dir)),
                    "error": f"Invalid JSON: {str(e)}",
                }
            )

    results["pass_rate"] = (
        results["passed"] / results["total_skills"] if results["total_skills"] > 0 else 0
    )
    return results


def eval_instructions_completeness(skills_dir: Path) -> Dict[str, Any]:
    """
    Eval: Verify all skills have complete instructions.md.

    Checks:
    - instructions.md exists
    - File is not empty
    - Contains key sections (heuristic check)
    """
    results = {
        "eval_id": "instructions-completeness",
        "total_skills": 0,
        "passed": 0,
        "failed": 0,
        "errors": [],
    }

    for skill_json_path in skills_dir.rglob("skill.json"):
        results["total_skills"] += 1
        skill_dir = skill_json_path.parent
        instructions_path = skill_dir / "instructions.md"

        if not instructions_path.exists():
            results["failed"] += 1
            results["errors"].append(
                {
                    "skill": str(skill_dir.relative_to(skills_dir)),
                    "error": "instructions.md missing",
                }
            )
            continue

        try:
            content = instructions_path.read_text()

            # Check if empty
            if len(content.strip()) < 50:
                results["failed"] += 1
                results["errors"].append(
                    {
                        "skill": str(skill_dir.relative_to(skills_dir)),
                        "error": "instructions.md is too short (< 50 chars)",
                    }
                )
                continue

            # Heuristic: Check for common section headers
            has_sections = any(
                keyword in content.lower() for keyword in ["purpose", "step", "usage", "example"]
            )
            if not has_sections:
                results["failed"] += 1
                results["errors"].append(
                    {
                        "skill": str(skill_dir.relative_to(skills_dir)),
                        "error": "instructions.md lacks common sections (Purpose, Steps, Usage, Example)",
                    }
                )
                continue

            results["passed"] += 1

        except Exception as e:
            results["failed"] += 1
            results["errors"].append(
                {
                    "skill": str(skill_dir.relative_to(skills_dir)),
                    "error": f"Error reading instructions.md: {str(e)}",
                }
            )

    results["pass_rate"] = (
        results["passed"] / results["total_skills"] if results["total_skills"] > 0 else 0
    )
    return results


def eval_chain_compatibility(registry_dir: Path) -> Dict[str, Any]:
    """
    Eval: Verify workflow blueprints reference valid skills.

    Checks:
    - All skill_ids in blueprints exist in registry
    - Chain sequences are valid
    """
    results = {
        "eval_id": "chain-compatibility",
        "total_workflows": 0,
        "passed": 0,
        "failed": 0,
        "errors": [],
    }

    # Load skills registry
    skills_json = registry_dir / "skills.json"
    if not skills_json.exists():
        results["errors"].append(
            {"workflow": "N/A", "error": f"Skills registry not found at {skills_json}"}
        )
        results["pass_rate"] = 0
        return results

    with open(skills_json) as f:
        registry = json.load(f)

    valid_skill_ids = {skill["id"] for skill in registry.get("skills", [])}

    # Check blueprints
    blueprints_dir = registry_dir / "blueprints"
    if not blueprints_dir.exists():
        return results

    import yaml

    for blueprint_path in blueprints_dir.glob("*.yaml"):
        results["total_workflows"] += 1

        try:
            with open(blueprint_path) as f:
                blueprint = yaml.safe_load(f)

            # Check chain_sequence
            if "chain_sequence" not in blueprint:
                results["failed"] += 1
                results["errors"].append(
                    {"workflow": blueprint_path.name, "error": "Missing chain_sequence"}
                )
                continue

            # Verify all skill_ids exist
            invalid_skills = []
            for step in blueprint["chain_sequence"]:
                skill_id = step.get("skill_id")
                if skill_id and skill_id not in valid_skill_ids:
                    invalid_skills.append(skill_id)

            if invalid_skills:
                results["failed"] += 1
                results["errors"].append(
                    {
                        "workflow": blueprint_path.name,
                        "error": f"Invalid skill_ids: {', '.join(invalid_skills)}",
                    }
                )
                continue

            results["passed"] += 1

        except Exception as e:
            results["failed"] += 1
            results["errors"].append(
                {"workflow": blueprint_path.name, "error": f"Error parsing blueprint: {str(e)}"}
            )

    results["pass_rate"] = (
        results["passed"] / results["total_workflows"] if results["total_workflows"] > 0 else 0
    )
    return results


def main():
    """Run all evals and print results."""
    repo_root = Path(__file__).parent.parent
    skills_dir = repo_root / "skills-library"
    registry_dir = repo_root / "registry"

    print("🧪 Running Evaluation Harness")
    print("=" * 60)
    print()

    # Run evals
    evals = [
        eval_skill_schema_validity(skills_dir),
        eval_instructions_completeness(skills_dir),
        eval_chain_compatibility(registry_dir),
    ]

    # Print results
    all_passed = True
    for eval_result in evals:
        eval_id = eval_result["eval_id"]
        passed = eval_result["passed"]
        total = eval_result.get("total_skills", eval_result.get("total_workflows", 0))
        pass_rate = eval_result["pass_rate"]

        status = "✅ PASS" if pass_rate == 1.0 else "⚠️  PARTIAL" if pass_rate > 0.8 else "❌ FAIL"
        print(f"{status} {eval_id}")
        print(f"   {passed}/{total} passed ({pass_rate*100:.1f}%)")

        if eval_result["errors"]:
            all_passed = False
            print(f"   Errors: {len(eval_result['errors'])}")
            for error in eval_result["errors"][:5]:  # Show first 5 errors
                print(f"     • {error.get('skill', error.get('workflow'))}: {error['error']}")
            if len(eval_result["errors"]) > 5:
                print(f"     ... and {len(eval_result['errors']) - 5} more")
        print()

    # Summary
    print("=" * 60)
    if all_passed:
        print("✅ All evals passed!")
        return 0
    else:
        print("⚠️  Some evals failed or have warnings")
        return 1


if __name__ == "__main__":
    sys.exit(main())
