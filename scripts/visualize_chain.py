#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Workflow Chain Visualizer
Generates Mermaid diagrams from workflow blueprint YAML files
"""

import yaml
import sys
import argparse
from pathlib import Path


def generate_mermaid_diagram(workflow_file: Path, output_file: Path):
    """Generate Mermaid diagram from workflow YAML"""

    # Load workflow
    with open(workflow_file, 'r') as f:
        workflow = yaml.safe_load(f)

    # Generate output
    output = []
    output.append(f"# Workflow: {workflow.get('name', 'Unnamed')}\n\n")
    output.append(f"**Version:** {workflow.get('version', '1.0.0')}\n\n")
    output.append(f"{workflow.get('description', '')}\n\n")

    output.append("## Workflow Diagram\n\n")
    output.append("```mermaid\n")
    output.append("graph TD\n")

    # Generate nodes for each step
    steps = workflow.get('chain_sequence', [])
    for i, step in enumerate(steps):
        step_id = step.get('step_id', f'step_{i}')
        skill_id = step.get('skill_id', 'unknown')
        action = step.get('action', 'execute')

        # Node definition
        label = f"{step_id}<br/>{skill_id}<br/>{action}"
        output.append(f"    {step_id}[\"{label}\"]\n")

        # Connect to next step
        if i < len(steps) - 1:
            next_step = steps[i + 1].get('step_id', f'step_{i+1}')

            # Check for conditional
            if 'conditions' in step:
                output.append(f"    {step_id} -->|conditional| {next_step}\n")
            else:
                output.append(f"    {step_id} --> {next_step}\n")

        # Error handling
        if 'error_handling' in step:
            on_failure = step['error_handling'].get('on_failure', 'stop')
            if on_failure == 'fallback' and 'fallback_step' in step['error_handling']:
                fallback = step['error_handling']['fallback_step']
                output.append(f"    {step_id} -.->|error| {fallback}\n")

    # Add parallel groups
    if 'logic_gates' in workflow and 'parallel_groups' in workflow['logic_gates']:
        for group in workflow['logic_gates']['parallel_groups']:
            group_id = group.get('group_id', 'parallel')
            steps_in_group = group.get('step_ids', [])
            if len(steps_in_group) > 1:
                output.append(f"\n    subgraph {group_id}[\"Parallel Execution\"]\n")
                for step_id in steps_in_group:
                    output.append(f"        {step_id}\n")
                output.append(f"    end\n")

    output.append("```\n\n")

    # Add step details
    output.append("## Step Details\n\n")
    for i, step in enumerate(steps, 1):
        step_id = step.get('step_id', f'step_{i}')
        skill_id = step.get('skill_id', 'unknown')
        action = step.get('action', 'execute')

        output.append(f"### {i}. {step_id}\n\n")
        output.append(f"- **Skill:** `{skill_id}`\n")
        output.append(f"- **Action:** {action}\n")

        if 'timeout_seconds' in step:
            output.append(f"- **Timeout:** {step['timeout_seconds']}s\n")

        if 'error_handling' in step:
            output.append(f"- **On Failure:** {step['error_handling'].get('on_failure', 'stop')}\n")

        output.append("\n")

    # Write output
    with open(output_file, 'w') as f:
        f.writelines(output)

    print(f"✅ Diagram generated: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Generate workflow visualization')
    parser.add_argument('workflow', help='Path to workflow YAML file')
    parser.add_argument('-o', '--output', default='workflow-diagram.md',
                       help='Output markdown file (default: workflow-diagram.md)')

    args = parser.parse_args()

    workflow_file = Path(args.workflow)
    if not workflow_file.exists():
        print(f"Error: Workflow file not found: {workflow_file}")
        sys.exit(1)

    output_file = Path(args.output)

    print("🔗 Generating workflow visualization...")
    print(f"   Input: {workflow_file}")
    print(f"   Output: {output_file}")
    print()

    generate_mermaid_diagram(workflow_file, output_file)

    print()
    print("✅ Visualization complete!")
    print(f"   View: cat {output_file}")


if __name__ == '__main__':
    main()
