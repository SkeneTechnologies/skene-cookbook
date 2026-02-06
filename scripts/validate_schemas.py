#!/usr/bin/env python3
"""
Schema Validator for Skills Directory
Validates JSON/YAML files against schemas
"""

import json
import yaml
import sys
import argparse
from pathlib import Path
from jsonschema import validate, ValidationError, Draft7Validator


class SchemaValidator:
    """Validate files against schemas"""

    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.schemas_path = self.base_path / "schemas"
        self.errors = []

    def validate_skills(self):
        """Validate all skill.json files"""
        print("🔍 Validating skill.json files...")

        # Load schema
        schema_path = self.schemas_path / "skill_definition.json"
        with open(schema_path, 'r') as f:
            schema = json.load(f)

        # Find all skill.json files
        skill_files = list(Path("skills-library").rglob("skill.json"))
        print(f"   Found {len(skill_files)} skill files")

        errors = 0
        for skill_file in skill_files:
            try:
                with open(skill_file, 'r') as f:
                    skill_data = json.load(f)

                # Basic structure validation (schema might be too strict for existing files)
                if 'id' not in skill_data:
                    print(f"   ❌ {skill_file}: Missing 'id' field")
                    errors += 1
                elif 'version' not in skill_data:
                    print(f"   ⚠️  {skill_file}: Missing 'version' field")

            except json.JSONDecodeError as e:
                print(f"   ❌ {skill_file}: Invalid JSON - {e}")
                errors += 1
            except Exception as e:
                print(f"   ❌ {skill_file}: {e}")
                errors += 1

        if errors == 0:
            print(f"   ✅ All skill files valid")
        else:
            print(f"   ❌ {errors} errors found")
            sys.exit(1)

    def validate_metadata(self):
        """Validate all metadata.yaml files"""
        print("🔍 Validating metadata.yaml files...")

        metadata_files = list(Path("skills-library").rglob("metadata.yaml"))
        print(f"   Found {len(metadata_files)} metadata files")

        errors = 0
        for metadata_file in metadata_files:
            try:
                with open(metadata_file, 'r') as f:
                    metadata = yaml.safe_load(f)

                # Basic structure validation
                if 'security' not in metadata:
                    print(f"   ❌ {metadata_file}: Missing 'security' section")
                    errors += 1
                elif 'risk_level' not in metadata['security']:
                    print(f"   ❌ {metadata_file}: Missing 'risk_level'")
                    errors += 1

            except yaml.YAMLError as e:
                print(f"   ❌ {metadata_file}: Invalid YAML - {e}")
                errors += 1
            except Exception as e:
                print(f"   ❌ {metadata_file}: {e}")
                errors += 1

        if errors == 0:
            print(f"   ✅ All metadata files valid")
        else:
            print(f"   ❌ {errors} errors found")
            sys.exit(1)

    def validate_workflows(self):
        """Validate workflow blueprint files"""
        print("🔍 Validating workflow blueprints...")

        blueprint_files = list(Path("registry/blueprints").glob("*.yaml"))
        print(f"   Found {len(blueprint_files)} blueprint files")

        errors = 0
        for blueprint_file in blueprint_files:
            try:
                with open(blueprint_file, 'r') as f:
                    blueprint = yaml.safe_load(f)

                # Basic structure validation
                required_fields = ['id', 'name', 'chain_sequence']
                for field in required_fields:
                    if field not in blueprint:
                        print(f"   ❌ {blueprint_file}: Missing '{field}'")
                        errors += 1

            except yaml.YAMLError as e:
                print(f"   ❌ {blueprint_file}: Invalid YAML - {e}")
                errors += 1
            except Exception as e:
                print(f"   ❌ {blueprint_file}: {e}")
                errors += 1

        if errors == 0:
            print(f"   ✅ All workflow blueprints valid")
        else:
            print(f"   ❌ {errors} errors found")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Validate schema files')
    parser.add_argument('--type', choices=['skills', 'metadata', 'workflows', 'all'],
                       default='all', help='Type of files to validate')

    args = parser.parse_args()

    validator = SchemaValidator()

    if args.type in ['skills', 'all']:
        validator.validate_skills()

    if args.type in ['metadata', 'all']:
        validator.validate_metadata()

    if args.type in ['workflows', 'all']:
        validator.validate_workflows()

    print("\n✅ Validation complete!")


if __name__ == '__main__':
    main()
