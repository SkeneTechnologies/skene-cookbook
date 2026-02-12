# SPDX-License-Identifier: MIT
# Copyright (c) 2024-2026 Skene Technologies

"""
LLM-based schema generator for skills.

Uses Claude API to generate JSON schemas from skill descriptions and instructions.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import anthropic


class SchemaGenerator:
    """
    Generates JSON schemas from skill descriptions using Claude API.

    Analyzes skill objectives, tools, and instructions to create appropriate
    inputSchema and outputSchema definitions.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-5-20250929"):
        """
        Initialize schema generator.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Claude model to use
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model

    def generate_schema(
        self,
        skill_id: str,
        description: str,
        tools: list,
        instructions: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any], float]:
        """
        Generate input and output schemas for a skill.

        Args:
            skill_id: Skill identifier
            description: Skill description/objective
            tools: List of tools the skill uses
            instructions: Optional detailed instructions
            domain: Optional domain (e.g., 'finops', 'marketing')

        Returns:
            Tuple of (inputSchema, outputSchema, confidence_score)
        """
        prompt = self._build_prompt(skill_id, description, tools, instructions, domain)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8192,  # Increased for complex schemas
                messages=[{"role": "user", "content": prompt}],
            )

            # Parse response
            content = response.content[0].text
            result = self._parse_response(content)

            return result["inputSchema"], result["outputSchema"], result["confidence"]

        except Exception as e:
            raise RuntimeError(f"Schema generation failed for {skill_id}: {e}")

    def _build_prompt(
        self,
        skill_id: str,
        description: str,
        tools: list,
        instructions: Optional[str],
        domain: Optional[str],
    ) -> str:
        """Build prompt for schema generation."""
        tools_desc = (
            "\n".join([f"- {tool.get('name', tool)}" for tool in tools]) if tools else "None"
        )

        prompt = f"""You are a JSON Schema expert. Generate input and output schemas for a skill.

**Skill ID:** {skill_id}
**Domain:** {domain or 'unknown'}
**Description:** {description}

**Tools Used:**
{tools_desc}

**Instructions:**
{instructions or 'Not provided'}

Generate two JSON schemas:
1. **inputSchema**: What data this skill needs as input
2. **outputSchema**: What data this skill produces as output

**Guidelines:**
- Use JSON Schema Draft 2020-12 format
- Include type, properties, required fields, descriptions
- Infer field names from the skill description and tools
- Be specific with types (string, number, integer, boolean, array, object)
- Add format hints where appropriate (email, uri, date-time, etc.)
- For finops skills: Include numeric fields for calculations
- For marketing skills: Include string fields for content/campaigns
- For RevOps skills: Include CRM/deal-related fields
- Keep schemas practical and aligned with tool requirements

**Output format (JSON only, no markdown):**
{{
  "inputSchema": {{
    "type": "object",
    "properties": {{ ... }},
    "required": [ ... ],
    "additionalProperties": false
  }},
  "outputSchema": {{
    "type": "object",
    "properties": {{ ... }},
    "required": [ ... ]
  }},
  "confidence": 0.85,
  "reasoning": "Brief explanation of schema design choices"
}}

Generate the schemas now:"""

        return prompt

    def _parse_response(self, content: str) -> Dict[str, Any]:
        """
        Parse LLM response into schemas.

        Args:
            content: Raw LLM response

        Returns:
            Dictionary with inputSchema, outputSchema, confidence, reasoning
        """
        # Try to extract JSON from response (handle markdown code blocks)
        content = content.strip()

        if "```json" in content:
            # Extract from markdown code block
            start = content.find("```json") + 7
            end = content.find("```", start)
            content = content[start:end].strip()
        elif "```" in content:
            # Generic code block
            start = content.find("```") + 3
            end = content.find("```", start)
            content = content[start:end].strip()

        try:
            result = json.loads(content)

            # Validate structure
            if "inputSchema" not in result or "outputSchema" not in result:
                raise ValueError("Missing inputSchema or outputSchema in response")

            # Add default confidence if missing
            if "confidence" not in result:
                result["confidence"] = 0.7

            return result

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}\nContent: {content[:200]}")

    def validate_generated_schema(self, schema: Dict[str, Any]) -> bool:
        """
        Validate that generated schema is well-formed.

        Args:
            schema: JSON Schema to validate

        Returns:
            True if valid, False otherwise
        """
        if not isinstance(schema, dict):
            return False

        # Check required fields
        if "type" not in schema:
            return False

        if schema["type"] == "object":
            if "properties" not in schema:
                return False

            # Validate properties
            properties = schema.get("properties", {})
            if not isinstance(properties, dict):
                return False

        return True


def generate_for_skill_file(
    skill_json_path: Path, generator: SchemaGenerator, dry_run: bool = False
) -> Dict[str, Any]:
    """
    Generate schemas for a skill.json file.

    Args:
        skill_json_path: Path to skill.json
        generator: SchemaGenerator instance
        dry_run: If True, don't modify the file

    Returns:
        Dictionary with result details
    """
    with open(skill_json_path, "r") as f:
        skill = json.load(f)

    skill_id = skill.get("id", "unknown")
    description = skill.get("description", "")
    tools = skill.get("tools", [])
    domain = skill.get("domain", "")

    # Check if instructions file exists
    instructions = None
    instructions_path = skill_json_path.parent / "instructions.md"
    if instructions_path.exists():
        with open(instructions_path, "r") as f:
            instructions = f.read()

    # Generate schemas
    try:
        input_schema, output_schema, confidence = generator.generate_schema(
            skill_id=skill_id,
            description=description,
            tools=tools,
            instructions=instructions,
            domain=domain,
        )

        # Validate
        if not generator.validate_generated_schema(input_schema):
            return {
                "success": False,
                "skill_id": skill_id,
                "error": "Generated inputSchema is invalid",
            }

        if not generator.validate_generated_schema(output_schema):
            return {
                "success": False,
                "skill_id": skill_id,
                "error": "Generated outputSchema is invalid",
            }

        # Update skill.json
        if not dry_run:
            skill["inputSchema"] = input_schema
            skill["outputSchema"] = output_schema

            # Add metadata about generation
            if "metadata" not in skill:
                skill["metadata"] = {}
            skill["metadata"]["schemaGenerated"] = True
            skill["metadata"]["schemaConfidence"] = confidence

            with open(skill_json_path, "w") as f:
                json.dump(skill, f, indent=2)
                f.write("\n")

        return {
            "success": True,
            "skill_id": skill_id,
            "confidence": confidence,
            "input_fields": len(input_schema.get("properties", {})),
            "output_fields": len(output_schema.get("properties", {})),
        }

    except Exception as e:
        return {"success": False, "skill_id": skill_id, "error": str(e)}
