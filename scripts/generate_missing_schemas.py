#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Batch schema generation script.

Uses Claude API to generate missing schemas for skills.

Usage:
    # Generate for specific domains
    python scripts/generate_missing_schemas.py --domains security,development

    # Generate for all skills with empty schemas
    python scripts/generate_missing_schemas.py --all

    # Dry run (no file modifications)
    python scripts/generate_missing_schemas.py --domains security --dry-run
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from eval_harness.schema_generator import SchemaGenerator, generate_for_skill_file


def find_skills_needing_schemas(
    skills_library_path: Path,
    domains: List[str] = None
) -> List[Path]:
    """
    Find all skills with empty schemas.

    Args:
        skills_library_path: Path to skills library
        domains: Optional list of domains to filter

    Returns:
        List of paths to skill.json files needing schemas
    """
    skills_needing_schemas = []

    executable_path = skills_library_path / 'executable'
    if not executable_path.exists():
        return []

    for domain_dir in executable_path.iterdir():
        if not domain_dir.is_dir():
            continue

        # Filter by domain if specified
        if domains and domain_dir.name not in domains:
            continue

        for skill_dir in domain_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_json_path = skill_dir / 'skill.json'
            if not skill_json_path.exists():
                continue

            # Check if schemas are empty
            with open(skill_json_path, 'r') as f:
                skill = json.load(f)

            # Skip if already marked to skip validation
            if skill.get('skipSchemaValidation'):
                continue

            input_schema = skill.get('inputSchema', {})
            output_schema = skill.get('outputSchema', {})

            # Check if schemas are empty or just placeholder
            input_empty = not input_schema or input_schema.get('properties', {}) == {}
            output_empty = not output_schema or output_schema.get('properties', {}) == {}

            if input_empty or output_empty:
                skills_needing_schemas.append(skill_json_path)

    return skills_needing_schemas


def generate_batch(
    skill_paths: List[Path],
    generator: SchemaGenerator,
    dry_run: bool = False,
    delay_ms: int = 1000
) -> Dict[str, List]:
    """
    Generate schemas for multiple skills.

    Args:
        skill_paths: List of skill.json paths
        generator: SchemaGenerator instance
        dry_run: If True, don't modify files
        delay_ms: Delay between API calls (rate limiting)

    Returns:
        Dictionary with success/failure lists
    """
    results = {
        'success': [],
        'failed': [],
        'stats': defaultdict(int)
    }

    total = len(skill_paths)

    for i, skill_path in enumerate(skill_paths, 1):
        print(f"\n[{i}/{total}] Processing {skill_path.parent.parent.name}/{skill_path.parent.name}...")

        try:
            result = generate_for_skill_file(skill_path, generator, dry_run=dry_run)

            if result['success']:
                print(f"  ✓ Generated schemas (confidence: {result['confidence']:.2f})")
                print(f"    Input fields: {result['input_fields']}, Output fields: {result['output_fields']}")
                results['success'].append(result)
                results['stats']['success'] += 1
            else:
                print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")
                results['failed'].append(result)
                results['stats']['failed'] += 1

        except Exception as e:
            print(f"  ✗ Error: {e}")
            results['failed'].append({
                'skill_id': skill_path.parent.name,
                'error': str(e)
            })
            results['stats']['failed'] += 1

        # Rate limiting
        if i < total:
            time.sleep(delay_ms / 1000.0)

    return results


def print_summary(results: Dict, dry_run: bool = False):
    """Print generation summary."""
    print("\n" + "=" * 70)
    print("SCHEMA GENERATION SUMMARY")
    print("=" * 70)

    print(f"\nTotal processed: {results['stats']['success'] + results['stats']['failed']}")
    print(f"Successful: {results['stats']['success']}")
    print(f"Failed: {results['stats']['failed']}")

    if dry_run:
        print("\n⚠ DRY RUN: No files were modified")

    if results['success']:
        avg_confidence = sum(r['confidence'] for r in results['success']) / len(results['success'])
        print(f"\nAverage confidence: {avg_confidence:.2f}")

        # Confidence distribution
        high_conf = sum(1 for r in results['success'] if r['confidence'] >= 0.8)
        med_conf = sum(1 for r in results['success'] if 0.6 <= r['confidence'] < 0.8)
        low_conf = sum(1 for r in results['success'] if r['confidence'] < 0.6)

        print(f"\nConfidence distribution:")
        print(f"  High (≥0.8): {high_conf}")
        print(f"  Medium (0.6-0.8): {med_conf}")
        print(f"  Low (<0.6): {low_conf}")

    if results['failed']:
        print(f"\nFailed skills:")
        for failure in results['failed'][:10]:
            print(f"  - {failure.get('skill_id', 'unknown')}: {failure.get('error', 'Unknown')}")
        if len(results['failed']) > 10:
            print(f"  ... and {len(results['failed']) - 10} more")


def main():
    parser = argparse.ArgumentParser(description='Generate missing schemas using Claude API')
    parser.add_argument('--domains', type=str, help='Comma-separated list of domains')
    parser.add_argument('--all', action='store_true', help='Generate for all skills with empty schemas')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be generated without modifying files')
    parser.add_argument('--yes', '-y', action='store_true', help='Skip confirmation prompt')
    parser.add_argument('--skills-library', type=str, default='skills-library', help='Path to skills library')
    parser.add_argument('--model', type=str, default='claude-sonnet-4-5-20250929', help='Claude model to use')
    parser.add_argument('--delay', type=int, default=1000, help='Delay between API calls (ms)')

    args = parser.parse_args()

    if not (args.domains or args.all):
        parser.error("Must specify --domains or --all")

    # Parse domains
    domains = None
    if args.domains:
        domains = [d.strip() for d in args.domains.split(',')]

    # Find skills needing schemas
    print("Scanning for skills with empty schemas...")
    skills_library_path = Path(args.skills_library)
    skill_paths = find_skills_needing_schemas(skills_library_path, domains)

    if not skill_paths:
        print("No skills found needing schema generation")
        return

    print(f"\nFound {len(skill_paths)} skills needing schemas")

    if args.dry_run:
        print("\n⚠ DRY RUN MODE: No files will be modified")

    # Initialize generator
    try:
        generator = SchemaGenerator(model=args.model)
    except ValueError as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease set ANTHROPIC_API_KEY environment variable:")
        print("  export ANTHROPIC_API_KEY=your-api-key")
        sys.exit(1)

    # Confirm with user
    if not args.dry_run and not args.yes:
        print(f"\nThis will make ~{len(skill_paths)} API calls to Claude")
        response = input("Continue? [y/N]: ")
        if response.lower() != 'y':
            print("Aborted")
            return

    # Generate schemas
    results = generate_batch(skill_paths, generator, dry_run=args.dry_run, delay_ms=args.delay)

    # Print summary
    print_summary(results, dry_run=args.dry_run)

    if not args.dry_run and results['stats']['success'] > 0:
        print("\n" + "=" * 70)
        print("NEXT STEPS")
        print("=" * 70)
        print("\n1. Review generated schemas: git diff skills-library/executable/")
        print("2. Re-run evaluation: python scripts/batch_eval_skills.py --domains <domains>")
        print("3. Commit changes: git add skills-library/ && git commit -m 'Add AI-generated schemas'")


if __name__ == '__main__':
    main()
