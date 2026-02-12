# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
Test data generator for evaluation harness.

Automatically generates valid and edge-case test data from JSON Schema definitions.
Supports both single skill test generation and batch generation for multiple skills.

Usage:
    generator = TestDataGenerator()

    # Generate from skill definition
    test_cases = generator.generate_from_skill('elg_mdf_tracker')

    # Generate from schema directly
    test_cases = generator.generate_from_schema(input_schema, num_cases=5)

    # Generate edge cases
    edge_cases = generator.generate_edge_cases(input_schema)
"""

import json
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class TestDataGenerator:
    """
    Generates synthetic test data from JSON Schema definitions.

    Supports:
    - Valid test cases following schema constraints
    - Edge cases (missing fields, invalid types, boundary values)
    - Bulk generation for batch evaluation
    """

    def __init__(self, skills_library_path: Optional[Path] = None):
        """
        Initialize test data generator.

        Args:
            skills_library_path: Path to skills library (default: auto-detect)
        """
        if skills_library_path is None:
            # Auto-detect from common locations
            project_root = Path(__file__).parent.parent
            skills_library_path = project_root / "skills-library"

        self.skills_library_path = Path(skills_library_path)

        # Support new directory structure (context/ and executable/ subdirs)
        self.search_paths = []
        if (self.skills_library_path / "executable").exists():
            self.search_paths.append(self.skills_library_path / "executable")
        if (self.skills_library_path / "context").exists():
            self.search_paths.append(self.skills_library_path / "context")
        if not self.search_paths:
            # Fallback to root if new structure doesn't exist
            self.search_paths = [self.skills_library_path]

        # Default value generators by type
        self.type_generators = {
            "string": self._generate_string,
            "number": self._generate_number,
            "integer": self._generate_integer,
            "boolean": self._generate_boolean,
            "array": self._generate_array,
            "object": self._generate_object,
        }

    def generate_from_skill(
        self, skill_id: str, num_valid_cases: int = 3, include_edge_cases: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Generate test data for a specific skill.

        Args:
            skill_id: Skill identifier (e.g., 'elg_mdf_tracker')
            num_valid_cases: Number of valid test cases to generate
            include_edge_cases: Whether to include edge cases

        Returns:
            List of test case dictionaries with 'inputs', 'label', 'expected_valid' fields
        """
        # Load skill definition
        skill_path = self._find_skill_path(skill_id)
        if not skill_path:
            raise FileNotFoundError(f"Skill not found: {skill_id}")

        with open(skill_path / "skill.json", "r") as f:
            skill_def = json.load(f)

        input_schema = skill_def.get("inputSchema", {})

        # Generate valid test cases
        test_cases = []
        for i in range(num_valid_cases):
            inputs = self.generate_from_schema(input_schema)
            test_cases.append(
                {"inputs": inputs, "label": f"valid_case_{i+1}", "expected_valid": True}
            )

        # Generate edge cases
        if include_edge_cases:
            edge_cases = self.generate_edge_cases(input_schema)
            test_cases.extend(edge_cases)

        return test_cases

    def generate_from_schema(
        self, schema: Dict[str, Any], depth: int = 0, max_depth: int = 5
    ) -> Any:
        """
        Generate a single valid value from JSON Schema.

        Args:
            schema: JSON Schema definition
            depth: Current recursion depth
            max_depth: Maximum recursion depth

        Returns:
            Generated value matching schema
        """
        if depth > max_depth:
            return None

        schema_type = schema.get("type", "object")

        # Handle enum
        if "enum" in schema:
            return random.choice(schema["enum"])

        # Handle const
        if "const" in schema:
            return schema["const"]

        # Generate by type
        generator = self.type_generators.get(schema_type, self._generate_string)
        return generator(schema, depth)

    def generate_edge_cases(self, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate edge cases for schema validation testing.

        Edge cases include:
        - Missing required fields
        - Invalid types
        - Boundary values
        - Empty arrays/objects

        Args:
            schema: JSON Schema definition

        Returns:
            List of test case dictionaries with edge cases
        """
        edge_cases = []

        if schema.get("type") != "object":
            return edge_cases

        required = schema.get("required", [])
        properties = schema.get("properties", {})

        # Edge case 1: Missing required field
        if required:
            for field in required:
                incomplete_data = self.generate_from_schema(schema)
                if field in incomplete_data:
                    del incomplete_data[field]
                edge_cases.append(
                    {
                        "inputs": incomplete_data,
                        "label": f"missing_{field}",
                        "expected_valid": False,
                    }
                )

        # Edge case 2: Wrong type for field
        for field, prop_schema in properties.items():
            invalid_data = self.generate_from_schema(schema)
            field_type = prop_schema.get("type", "string")

            # Generate wrong type
            if field_type == "string":
                invalid_data[field] = 12345  # number instead of string
            elif field_type in ["number", "integer"]:
                invalid_data[field] = "not_a_number"  # string instead of number
            elif field_type == "boolean":
                invalid_data[field] = "yes"  # string instead of boolean
            elif field_type == "array":
                invalid_data[field] = "not_an_array"
            elif field_type == "object":
                invalid_data[field] = "not_an_object"

            edge_cases.append(
                {"inputs": invalid_data, "label": f"invalid_type_{field}", "expected_valid": False}
            )

        # Edge case 3: Empty values
        edge_cases.append(
            {"inputs": {}, "label": "empty_object", "expected_valid": len(required) == 0}
        )

        return edge_cases

    def generate_batch(
        self, skill_ids: List[str], cases_per_skill: int = 3, output_dir: Optional[Path] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate test data for multiple skills at once.

        Args:
            skill_ids: List of skill IDs to generate for
            cases_per_skill: Number of test cases per skill
            output_dir: Optional directory to save test files

        Returns:
            Dictionary mapping skill_id to list of test cases
        """
        batch_data = {}

        for skill_id in skill_ids:
            try:
                test_cases = self.generate_from_skill(skill_id, num_valid_cases=cases_per_skill)
                batch_data[skill_id] = test_cases

                # Save to file if output dir specified
                if output_dir:
                    output_path = Path(output_dir) / f"{skill_id}_test_data.json"
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "w") as f:
                        json.dump(test_cases, f, indent=2)

            except Exception as e:
                print(f"Warning: Failed to generate test data for {skill_id}: {e}")
                batch_data[skill_id] = []

        return batch_data

    def save_test_cases(self, skill_id: str, test_cases: List[Dict[str, Any]], output_path: Path):
        """
        Save test cases to JSON file.

        Args:
            skill_id: Skill identifier
            test_cases: List of test cases
            output_path: Path to save JSON file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "skill_id": skill_id,
            "generated_at": datetime.now().isoformat(),
            "num_cases": len(test_cases),
            "test_cases": test_cases,
        }

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

    # Type-specific generators

    def _generate_string(self, schema: Dict[str, Any], depth: int = 0) -> str:
        """Generate string value."""
        # Check for pattern or format
        format_type = schema.get("format")

        if format_type == "email":
            return f"user_{self._random_string(5)}@example.com"
        elif format_type == "uri":
            return f"https://example.com/{self._random_string(8)}"
        elif format_type == "date-time":
            return datetime.now().isoformat()
        elif format_type == "date":
            return datetime.now().date().isoformat()

        # Check for min/max length
        min_length = schema.get("minLength", 1)
        max_length = schema.get("maxLength", 20)
        length = random.randint(min_length, min(max_length, 20))

        # Use description as hint for generating meaningful values
        description = schema.get("description", "").lower()

        if "id" in description or "identifier" in description:
            return f"test_{self._random_string(8)}"
        elif "name" in description:
            return f"Test Name {self._random_string(4)}"
        elif "email" in description:
            return f"user_{self._random_string(5)}@example.com"
        elif "url" in description or "uri" in description:
            return f"https://example.com/{self._random_string(8)}"

        return self._random_string(length)

    def _generate_number(self, schema: Dict[str, Any], depth: int = 0) -> float:
        """Generate number value."""
        minimum = schema.get("minimum", 0)
        maximum = schema.get("maximum", 10000)

        # Check for exclusive bounds
        if schema.get("exclusiveMinimum"):
            minimum = schema["exclusiveMinimum"] + 0.01
        if schema.get("exclusiveMaximum"):
            maximum = schema["exclusiveMaximum"] - 0.01

        return round(random.uniform(minimum, maximum), 2)

    def _generate_integer(self, schema: Dict[str, Any], depth: int = 0) -> int:
        """Generate integer value."""
        minimum = schema.get("minimum", 0)
        maximum = schema.get("maximum", 1000)

        # Check for exclusive bounds
        if schema.get("exclusiveMinimum"):
            minimum = schema["exclusiveMinimum"] + 1
        if schema.get("exclusiveMaximum"):
            maximum = schema["exclusiveMaximum"] - 1

        return random.randint(minimum, maximum)

    def _generate_boolean(self, schema: Dict[str, Any], depth: int = 0) -> bool:
        """Generate boolean value."""
        return random.choice([True, False])

    def _generate_array(self, schema: Dict[str, Any], depth: int = 0) -> List[Any]:
        """Generate array value."""
        min_items = schema.get("minItems", 0)
        max_items = schema.get("maxItems", 3)
        num_items = random.randint(min_items, min(max_items, 3))

        items_schema = schema.get("items", {"type": "string"})

        return [self.generate_from_schema(items_schema, depth + 1) for _ in range(num_items)]

    def _generate_object(self, schema: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
        """Generate object value."""
        properties = schema.get("properties", {})
        required = schema.get("required", [])

        result = {}

        # Generate required properties
        for prop in required:
            if prop in properties:
                result[prop] = self.generate_from_schema(properties[prop], depth + 1)

        # Generate some optional properties (50% chance each)
        for prop, prop_schema in properties.items():
            if prop not in required and random.random() > 0.5:
                result[prop] = self.generate_from_schema(prop_schema, depth + 1)

        return result

    # Helper methods

    def _random_string(self, length: int = 10) -> str:
        """Generate random alphanumeric string."""
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def _find_skill_path(self, skill_id: str) -> Optional[Path]:
        """
        Find skill directory in skills library.

        Args:
            skill_id: Skill identifier (e.g., 'elg_mdf_tracker', 'cursor_rules/flask')

        Returns:
            Path to skill directory or None if not found
        """
        # Handle path-based IDs (e.g., 'cursor_rules/flask')
        if "/" in skill_id:
            # Direct path-based lookup
            skill_path = self.skills_library_path / skill_id
            if skill_path.exists() and (skill_path / "skill.json").exists():
                return skill_path
            # Also try without skill.json to handle directory directly
            if skill_path.exists():
                return skill_path
            return None

        # Common domain abbreviations
        domain_prefixes = {
            "customer_success": ["cs_", "customer_success_"],
            "ai_ops": ["ai_", "ai_ops_"],
            "product_ops": ["prodops_", "product_ops_"],
            "support_ops": ["support_", "support_ops_"],
            "ecosystem": ["elg_", "ecosystem_"],
            "marketing": ["mktg_", "marketing_"],
            "revops": ["revops_", "revenue_ops_"],
            "plg": ["plg_"],
            "monetization": ["monetization_", "mon_"],
            "finops": ["finops_", "finance_ops_"],
            "security": ["security_", "sec_"],
            "community": ["community_", "comm_"],
        }

        # Search all domain directories (in both executable and context paths)
        for search_path in self.search_paths:
            for domain_dir in search_path.iterdir():
                if not domain_dir.is_dir() or domain_dir.name.startswith("."):
                    continue

                domain_name = domain_dir.name

                # Get possible prefixes for this domain
                prefixes_to_try = domain_prefixes.get(domain_name, [f"{domain_name}_"])
                prefixes_to_try.append("")  # Also try no prefix

                # Try multiple naming patterns
                patterns = set()  # Use set to avoid duplicates

                for prefix in prefixes_to_try:
                    if skill_id.startswith(prefix):
                        # Remove the prefix
                        base_name = skill_id[len(prefix) :]
                        patterns.add(base_name)
                        patterns.add(base_name.replace("_", "-"))

                # Also try exact match and common variations
                patterns.add(skill_id)
                patterns.add(skill_id.replace("_", "-"))
                patterns.add(skill_id.replace("-", "_"))

                # Try direct match first (fast path for non-nested structures)
                for pattern in patterns:
                    skill_dir = domain_dir / pattern
                    if skill_dir.exists() and (skill_dir / "skill.json").exists():
                        return skill_dir

                # If not found, search recursively (for nested structures like marketing)
                for pattern in patterns:
                    # Use rglob to search recursively
                    for skill_json_path in domain_dir.rglob(f"{pattern}/skill.json"):
                        return skill_json_path.parent

        return None


# Convenience functions


def generate_test_data(skill_id: str, num_cases: int = 3) -> List[Dict[str, Any]]:
    """
    Convenience function to generate test data for a skill.

    Args:
        skill_id: Skill identifier
        num_cases: Number of test cases to generate

    Returns:
        List of test cases
    """
    generator = TestDataGenerator()
    return generator.generate_from_skill(skill_id, num_valid_cases=num_cases)


def generate_batch_test_data(
    skill_ids: List[str], output_dir: Union[str, Path], cases_per_skill: int = 3
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Convenience function to generate test data for multiple skills.

    Args:
        skill_ids: List of skill IDs
        output_dir: Directory to save test files
        cases_per_skill: Number of test cases per skill

    Returns:
        Dictionary mapping skill_id to test cases
    """
    generator = TestDataGenerator()
    return generator.generate_batch(skill_ids, cases_per_skill, Path(output_dir))
