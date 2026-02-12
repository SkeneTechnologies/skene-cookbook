#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Schema normalization and remediation tool.

Fixes common schema issues:
1. Marks context files with skipSchemaValidation flag
2. Normalizes empty schema formats
3. Identifies skills needing AI-generated schemas

Usage:
    # Analyze only
    python scripts/normalize_schemas.py --analyze

    # Fix context files
    python scripts/normalize_schemas.py --fix-context

    # Fix all empty schemas
    python scripts/normalize_schemas.py --fix-all --dry-run
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


class SchemaNormalizer:
    """Normalizes and remediates schema issues."""

    def __init__(self, skills_library_path: Path):
        self.skills_library_path = Path(skills_library_path)
        self.stats = {
            'total': 0,
            'context_files': 0,
            'executable_skills': 0,
            'empty_schemas': 0,
            'has_tools_but_empty_schemas': 0,
            'fixed': 0,
            'errors': []
        }

    def analyze(self) -> Dict[str, List[Dict]]:
        """
        Analyze all skills and categorize by remediation strategy.

        Returns:
            Dictionary with categorized skills
        """
        categories = {
            'context_files': [],  # Mark with skipSchemaValidation
            'executable_with_tools': [],  # Can infer schema from tools
            'executable_no_tools': [],  # Need AI generation
            'valid': []  # Already have schemas
        }

        for type_dir in ['executable', 'context']:
            type_path = self.skills_library_path / type_dir
            if not type_path.exists():
                continue

            is_context = (type_dir == 'context')

            for domain_dir in type_path.iterdir():
                if not domain_dir.is_dir():
                    continue

                for skill_dir in domain_dir.iterdir():
                    if not skill_dir.is_dir():
                        continue

                    skill_json_path = skill_dir / 'skill.json'
                    if not skill_json_path.exists():
                        continue

                    try:
                        with open(skill_json_path, 'r') as f:
                            skill = json.load(f)

                        self.stats['total'] += 1

                        skill_id = skill.get('id', 'unknown')
                        domain = skill.get('domain', 'unknown')
                        input_schema = skill.get('inputSchema', {})
                        output_schema = skill.get('outputSchema', {})
                        tools = skill.get('tools', [])

                        has_empty_schemas = (not input_schema or input_schema == {}) and \
                                          (not output_schema or output_schema == {})

                        skill_info = {
                            'id': skill_id,
                            'domain': domain,
                            'path': skill_json_path,
                            'has_tools': len(tools) > 0,
                            'num_tools': len(tools),
                            'empty_schemas': has_empty_schemas
                        }

                        if is_context:
                            self.stats['context_files'] += 1
                            categories['context_files'].append(skill_info)
                        elif has_empty_schemas:
                            self.stats['empty_schemas'] += 1
                            if tools:
                                self.stats['has_tools_but_empty_schemas'] += 1
                                categories['executable_with_tools'].append(skill_info)
                            else:
                                categories['executable_no_tools'].append(skill_info)
                        else:
                            self.stats['executable_skills'] += 1
                            categories['valid'].append(skill_info)

                    except Exception as e:
                        self.stats['errors'].append(f"Error reading {skill_json_path}: {e}")

        return categories

    def mark_context_files(self, dry_run: bool = False) -> int:
        """
        Mark context files with skipSchemaValidation flag.

        Args:
            dry_run: If True, don't actually modify files

        Returns:
            Number of files modified
        """
        modified = 0
        context_path = self.skills_library_path / 'context'

        if not context_path.exists():
            return 0

        for domain_dir in context_path.iterdir():
            if not domain_dir.is_dir():
                continue

            for skill_dir in domain_dir.iterdir():
                if not skill_dir.is_dir():
                    continue

                skill_json_path = skill_dir / 'skill.json'
                if not skill_json_path.exists():
                    continue

                try:
                    with open(skill_json_path, 'r') as f:
                        skill = json.load(f)

                    # Check if already marked
                    if skill.get('skipSchemaValidation') == True:
                        continue

                    # Add flag
                    skill['skipSchemaValidation'] = True

                    if not dry_run:
                        with open(skill_json_path, 'w') as f:
                            json.dump(skill, f, indent=2)
                            f.write('\n')  # Add trailing newline

                    modified += 1

                except Exception as e:
                    self.stats['errors'].append(f"Error marking {skill_json_path}: {e}")

        return modified

    def normalize_empty_schemas(self, dry_run: bool = False) -> int:
        """
        Normalize empty schema formats to consistent placeholder.

        Args:
            dry_run: If True, don't actually modify files

        Returns:
            Number of files modified
        """
        modified = 0
        executable_path = self.skills_library_path / 'executable'

        if not executable_path.exists():
            return 0

        for domain_dir in executable_path.iterdir():
            if not domain_dir.is_dir():
                continue

            for skill_dir in domain_dir.iterdir():
                if not skill_dir.is_dir():
                    continue

                skill_json_path = skill_dir / 'skill.json'
                if not skill_json_path.exists():
                    continue

                try:
                    with open(skill_json_path, 'r') as f:
                        skill = json.load(f)

                    changed = False

                    # Normalize input schema
                    input_schema = skill.get('inputSchema')
                    if input_schema is None or input_schema == {}:
                        skill['inputSchema'] = {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                        changed = True

                    # Normalize output schema
                    output_schema = skill.get('outputSchema')
                    if output_schema is None or output_schema == {}:
                        skill['outputSchema'] = {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                        changed = True

                    if changed:
                        if not dry_run:
                            with open(skill_json_path, 'w') as f:
                                json.dump(skill, f, indent=2)
                                f.write('\n')

                        modified += 1

                except Exception as e:
                    self.stats['errors'].append(f"Error normalizing {skill_json_path}: {e}")

        return modified

    def print_report(self, categories: Dict[str, List[Dict]]):
        """Print analysis report."""
        print("\n" + "=" * 70)
        print("SCHEMA NORMALIZATION ANALYSIS")
        print("=" * 70)
        print(f"\nTotal skills: {self.stats['total']}")
        print(f"Context files: {self.stats['context_files']}")
        print(f"Executable skills: {self.stats['executable_skills']}")
        print(f"Empty schemas: {self.stats['empty_schemas']}")
        print(f"Has tools but empty schemas: {self.stats['has_tools_but_empty_schemas']}")

        print("\n" + "=" * 70)
        print("REMEDIATION STRATEGY")
        print("=" * 70)

        print(f"\n1. Mark as context (skipSchemaValidation): {len(categories['context_files'])}")
        print("   → cursor_rules, scientific, security, etc.")

        print(f"\n2. Can infer from tools: {len(categories['executable_with_tools'])}")
        print("   → Skills with tools but empty schemas")
        if categories['executable_with_tools'][:5]:
            print("   Examples:")
            for skill in categories['executable_with_tools'][:5]:
                print(f"     - {skill['id']} ({skill['num_tools']} tools)")

        print(f"\n3. Need AI generation: {len(categories['executable_no_tools'])}")
        print("   → Skills without tools and empty schemas")
        if categories['executable_no_tools'][:5]:
            print("   Examples:")
            for skill in categories['executable_no_tools'][:5]:
                print(f"     - {skill['id']}")

        print(f"\n4. Already valid: {len(categories['valid'])}")

        if self.stats['errors']:
            print(f"\n⚠ Errors encountered: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:
                print(f"  - {error}")


def main():
    parser = argparse.ArgumentParser(description='Normalize and remediate skill schemas')
    parser.add_argument('--analyze', action='store_true', help='Analyze schema quality')
    parser.add_argument('--fix-context', action='store_true', help='Mark context files')
    parser.add_argument('--fix-empty', action='store_true', help='Normalize empty schemas')
    parser.add_argument('--fix-all', action='store_true', help='Apply all fixes')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without applying')
    parser.add_argument('--skills-library', type=str, default='skills-library',
                       help='Path to skills library')

    args = parser.parse_args()

    # Default to analyze if no action specified
    if not (args.analyze or args.fix_context or args.fix_empty or args.fix_all):
        args.analyze = True

    normalizer = SchemaNormalizer(Path(args.skills_library))

    # Always analyze first
    categories = normalizer.analyze()

    if args.analyze:
        normalizer.print_report(categories)

    if args.fix_context or args.fix_all:
        print("\n" + "=" * 70)
        print("MARKING CONTEXT FILES")
        print("=" * 70)
        modified = normalizer.mark_context_files(dry_run=args.dry_run)
        if args.dry_run:
            print(f"Would mark {modified} context files with skipSchemaValidation")
        else:
            print(f"✓ Marked {modified} context files with skipSchemaValidation")

    if args.fix_empty or args.fix_all:
        print("\n" + "=" * 70)
        print("NORMALIZING EMPTY SCHEMAS")
        print("=" * 70)
        modified = normalizer.normalize_empty_schemas(dry_run=args.dry_run)
        if args.dry_run:
            print(f"Would normalize {modified} empty schemas")
        else:
            print(f"✓ Normalized {modified} empty schemas")

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("\n1. Review changes: git diff skills-library/")
    print("2. Generate missing schemas: python scripts/generate_missing_schemas.py")
    print("3. Re-run evaluation: python scripts/batch_eval_skills.py --domains all")


if __name__ == '__main__':
    main()
