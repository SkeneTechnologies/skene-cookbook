# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Runtime JSON Schema validation for skill inputs, outputs, and chain compatibility.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any
import jsonschema
from jsonschema import Draft202012Validator, ValidationError
import yaml


@dataclass
class ValidationResult:
    """Result of schema validation."""

    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        status = "✓ VALID" if self.valid else "✗ INVALID"
        if self.errors:
            return f"{status}\nErrors:\n  " + "\n  ".join(self.errors)
        if self.warnings:
            return f"{status}\nWarnings:\n  " + "\n  ".join(self.warnings)
        return status


class SkillValidator:
    """
    Validates skill inputs/outputs against JSON Schema at runtime.

    Loads schemas from skills-library/[domain]/[skill]/skill.json files
    and validates runtime data against inputSchema and outputSchema.
    """

    def __init__(self, skills_library_path: Optional[Path] = None):
        """
        Initialize validator.

        Args:
            skills_library_path: Path to skills-library directory.
                                If None, auto-detects from current location.
        """
        if skills_library_path is None:
            # Auto-detect from current file location
            current_file = Path(__file__)
            repo_root = current_file.parent.parent.parent
            skills_library_path = repo_root / "skills-library"

        self.skills_library_path = Path(skills_library_path)
        self._schema_cache: Dict[str, Dict[str, Any]] = {}
        self._metadata_cache: Dict[str, Dict[str, Any]] = {}

        if not self.skills_library_path.exists():
            raise FileNotFoundError(
                f"Skills library not found at: {self.skills_library_path}"
            )

    def _load_skill_schema(self, skill_id: str) -> Dict[str, Any]:
        """Load skill.json for a given skill_id."""
        if skill_id in self._schema_cache:
            return self._schema_cache[skill_id]

        # Support new directory structure (executable/ and context/)
        search_paths = []
        if (self.skills_library_path / 'executable').exists():
            search_paths.append(self.skills_library_path / 'executable')
        if (self.skills_library_path / 'context').exists():
            search_paths.append(self.skills_library_path / 'context')
        if not search_paths:
            # Fallback to root if new structure doesn't exist
            search_paths = [self.skills_library_path]

        # Search for skill across all domains
        for search_path in search_paths:
            for domain_dir in search_path.iterdir():
                if not domain_dir.is_dir():
                    continue

                for skill_dir in domain_dir.iterdir():
                    if not skill_dir.is_dir():
                        continue

                    skill_json_path = skill_dir / "skill.json"
                    if skill_json_path.exists():
                        with open(skill_json_path, 'r') as f:
                            schema = json.load(f)

                        if schema.get('id') == skill_id:
                            self._schema_cache[skill_id] = schema
                            return schema

        raise FileNotFoundError(
            f"Skill '{skill_id}' not found in {self.skills_library_path}"
        )

    def _load_skill_metadata(self, skill_id: str) -> Dict[str, Any]:
        """Load metadata.yaml for a given skill_id."""
        if skill_id in self._metadata_cache:
            return self._metadata_cache[skill_id]

        # Support new directory structure (executable/ and context/)
        search_paths = []
        if (self.skills_library_path / 'executable').exists():
            search_paths.append(self.skills_library_path / 'executable')
        if (self.skills_library_path / 'context').exists():
            search_paths.append(self.skills_library_path / 'context')
        if not search_paths:
            # Fallback to root if new structure doesn't exist
            search_paths = [self.skills_library_path]

        # Search for metadata across all domains
        for search_path in search_paths:
            for domain_dir in search_path.iterdir():
                if not domain_dir.is_dir():
                    continue

                for skill_dir in domain_dir.iterdir():
                    if not skill_dir.is_dir():
                        continue

                    skill_json_path = skill_dir / "skill.json"
                    metadata_path = skill_dir / "metadata.yaml"

                    if skill_json_path.exists() and metadata_path.exists():
                        with open(skill_json_path, 'r') as f:
                            schema = json.load(f)

                        if schema.get('id') == skill_id:
                            with open(metadata_path, 'r') as f:
                                metadata = yaml.safe_load(f)
                            self._metadata_cache[skill_id] = metadata
                            return metadata

        return {}

    def validate_input(
        self,
        skill_id: str,
        input_data: Dict[str, Any]
    ) -> ValidationResult:
        """
        Validate input data against skill's inputSchema.

        Args:
            skill_id: Skill identifier (e.g., 'elg_mdf_tracker')
            input_data: Runtime input data to validate

        Returns:
            ValidationResult with validation status and errors
        """
        try:
            schema = self._load_skill_schema(skill_id)
            input_schema = schema.get('inputSchema')

            if not input_schema:
                return ValidationResult(
                    valid=False,
                    errors=[f"Skill '{skill_id}' has no inputSchema defined"]
                )

            # Validate against JSON Schema
            validator = Draft202012Validator(input_schema)
            errors = []

            for error in validator.iter_errors(input_data):
                # Format error with JSONPath reference
                path = ".".join(str(p) for p in error.absolute_path)
                error_msg = f"input.{path}: {error.message}" if path else f"input: {error.message}"
                errors.append(error_msg)

            return ValidationResult(
                valid=len(errors) == 0,
                errors=errors,
                details={'schema': input_schema, 'data': input_data}
            )

        except FileNotFoundError as e:
            return ValidationResult(valid=False, errors=[str(e)])
        except Exception as e:
            return ValidationResult(
                valid=False,
                errors=[f"Validation error: {str(e)}"]
            )

    def validate_output(
        self,
        skill_id: str,
        output_data: Dict[str, Any]
    ) -> ValidationResult:
        """
        Validate output data against skill's outputSchema.

        Args:
            skill_id: Skill identifier
            output_data: Runtime output data to validate

        Returns:
            ValidationResult with validation status and errors
        """
        try:
            schema = self._load_skill_schema(skill_id)
            output_schema = schema.get('outputSchema')

            if not output_schema:
                return ValidationResult(
                    valid=False,
                    errors=[f"Skill '{skill_id}' has no outputSchema defined"]
                )

            # Validate against JSON Schema
            validator = Draft202012Validator(output_schema)
            errors = []

            for error in validator.iter_errors(output_data):
                path = ".".join(str(p) for p in error.absolute_path)
                error_msg = f"output.{path}: {error.message}" if path else f"output: {error.message}"
                errors.append(error_msg)

            return ValidationResult(
                valid=len(errors) == 0,
                errors=errors,
                details={'schema': output_schema, 'data': output_data}
            )

        except FileNotFoundError as e:
            return ValidationResult(valid=False, errors=[str(e)])
        except Exception as e:
            return ValidationResult(
                valid=False,
                errors=[f"Validation error: {str(e)}"]
            )

    def validate_chain_compatibility(
        self,
        producer_skill_id: str,
        consumer_skill_id: str,
        field_mappings: Optional[Dict[str, str]] = None
    ) -> ValidationResult:
        """
        Validate that two skills can be chained together.

        Checks that producer's output fields can satisfy consumer's input requirements.

        Args:
            producer_skill_id: Skill that produces output
            consumer_skill_id: Skill that consumes the output
            field_mappings: Optional explicit field mappings
                          (e.g., {'output.partner_id': 'input.partnerId'})

        Returns:
            ValidationResult indicating compatibility
        """
        try:
            producer_schema = self._load_skill_schema(producer_skill_id)
            consumer_schema = self._load_skill_schema(consumer_skill_id)

            producer_output = producer_schema.get('outputSchema', {}).get('properties', {})
            consumer_input = consumer_schema.get('inputSchema', {})
            consumer_required = consumer_input.get('required', [])
            consumer_props = consumer_input.get('properties', {})

            errors = []
            warnings = []

            # Check if required fields can be satisfied
            for required_field in consumer_required:
                if field_mappings:
                    # Check explicit mappings
                    mapped = False
                    for output_field, input_field in field_mappings.items():
                        if input_field.endswith(required_field):
                            output_field_name = output_field.split('.')[-1]
                            if output_field_name not in producer_output:
                                errors.append(
                                    f"Required field '{required_field}' mapped to "
                                    f"'{output_field_name}' which doesn't exist in "
                                    f"producer output"
                                )
                            mapped = True
                            break

                    if not mapped:
                        errors.append(
                            f"Required field '{required_field}' has no mapping from producer"
                        )
                else:
                    # Auto-detect by field name matching
                    if required_field not in producer_output:
                        # Try case-insensitive and snake_case/camelCase variants
                        found = False
                        for output_field in producer_output.keys():
                            if output_field.lower() == required_field.lower():
                                warnings.append(
                                    f"Field '{required_field}' has case mismatch with "
                                    f"producer field '{output_field}'"
                                )
                                found = True
                                break

                        if not found:
                            errors.append(
                                f"Required field '{required_field}' not found in "
                                f"producer output"
                            )

            # Type compatibility check (basic)
            if field_mappings:
                for output_field, input_field in field_mappings.items():
                    output_field_name = output_field.split('.')[-1]
                    input_field_name = input_field.split('.')[-1]

                    if output_field_name in producer_output and \
                       input_field_name in consumer_props:
                        producer_type = producer_output[output_field_name].get('type')
                        consumer_type = consumer_props[input_field_name].get('type')

                        if producer_type and consumer_type and producer_type != consumer_type:
                            warnings.append(
                                f"Type mismatch: {output_field_name} ({producer_type}) -> "
                                f"{input_field_name} ({consumer_type})"
                            )

            return ValidationResult(
                valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                details={
                    'producer_output_fields': list(producer_output.keys()),
                    'consumer_required_fields': consumer_required,
                    'field_mappings': field_mappings
                }
            )

        except FileNotFoundError as e:
            return ValidationResult(valid=False, errors=[str(e)])
        except Exception as e:
            return ValidationResult(
                valid=False,
                errors=[f"Chain validation error: {str(e)}"]
            )

    def get_risk_level(self, skill_id: str) -> str:
        """
        Get security risk level from metadata.yaml.

        Args:
            skill_id: Skill identifier

        Returns:
            Risk level: 'Low', 'Medium', 'High', or 'Critical'
        """
        metadata = self._load_skill_metadata(skill_id)
        return metadata.get('security', {}).get('risk_level', 'Medium')
