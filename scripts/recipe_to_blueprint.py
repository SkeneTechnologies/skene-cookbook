#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies
"""
Emit a workflow blueprint YAML stub from a recipe spec (list of skill_ids).
Use this to keep SKILL_CHAINS.md recipes and registry/blueprints/ in sync.

Usage:
  python scripts/recipe_to_blueprint.py --id workflow_my_chain \\
    --name "My Chain" --description "Does X then Y" --category "Sales" \\
    --skills lead_qualification,opportunity_scoring,deal_inspection

  Or with a spec file (YAML):
  python scripts/recipe_to_blueprint.py --spec docs/recipe_specs/my_chain.yaml
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import yaml


def main():
    parser = argparse.ArgumentParser(description="Generate blueprint YAML from recipe spec")
    parser.add_argument("--id", required=False, help="Workflow id (e.g. workflow_sales_qual)")
    parser.add_argument("--name", required=False, help="Human-readable name")
    parser.add_argument("--description", required=False, help="What this workflow accomplishes")
    parser.add_argument("--category", required=False, default="Workflow", help="Category")
    parser.add_argument(
        "--skills",
        required=False,
        help="Comma-separated skill_ids (e.g. revops_lead_qualification,revops_opportunity_scoring)",
    )
    parser.add_argument(
        "--spec",
        required=False,
        help="Path to YAML spec file (id, name, description, category, skill_ids)",
    )
    parser.add_argument(
        "--out", required=False, help="Output path (default: registry/blueprints/<id>.yaml)"
    )
    args = parser.parse_args()

    if args.spec:
        spec_path = Path(args.spec)
        if not spec_path.exists():
            print(f"Spec file not found: {spec_path}", file=sys.stderr)
            sys.exit(1)
        with open(spec_path) as f:
            spec = yaml.safe_load(f)
        workflow_id = spec.get("id")
        name = spec.get("name")
        description = spec.get("description", "")
        category = spec.get("category", "Workflow")
        skill_ids = spec.get("skill_ids", [])
    else:
        if not args.id or not args.name or not args.skills:
            parser.error("--id, --name, and --skills required when not using --spec")
        workflow_id = args.id
        name = args.name
        description = args.description or ""
        category = args.category or "Workflow"
        skill_ids = [s.strip() for s in args.skills.split(",") if s.strip()]

    if not workflow_id.startswith("workflow_"):
        workflow_id = f"workflow_{workflow_id}"

    chain_sequence = []
    for i, skill_id in enumerate(skill_ids, 1):
        step_id = f"step_{i}_{skill_id.replace('/', '_').replace('-', '_')}"
        if len(step_id) > 50:
            step_id = f"step_{i}"
        chain_sequence.append(
            {
                "step_id": step_id,
                "skill_id": skill_id,
                "action": "execute",
                "description": f"Execute {skill_id}",
                "timeout_seconds": 300,
                "error_handling": {"on_failure": "continue", "max_retries": 2},
            }
        )

    blueprint = {
        "id": workflow_id,
        "version": "1.0.0",
        "name": name,
        "description": description,
        "category": category,
        "chain_sequence": chain_sequence,
        "metadata": {
            "author": "Skene Cookbook",
            "created_at": datetime.utcnow().strftime("%Y-%m-%d"),
            "generated_by": "recipe_to_blueprint.py",
        },
    }

    out_path = Path(args.out) if args.out else Path("registry/blueprints") / f"{workflow_id}.yaml"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        yaml.dump(blueprint, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
