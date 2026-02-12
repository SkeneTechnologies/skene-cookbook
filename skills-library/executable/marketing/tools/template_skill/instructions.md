---
name: Marketing Tools Template
description: Template for creating new marketing automation skills. Use as a starting point when building custom marketing tools.
---

# Marketing Tools Template

This is a template for creating new marketing automation skills.

## How to Use This Template

1. Copy this directory to create a new marketing skill
2. Update `skill.json` with your skill's metadata
3. Replace this content with your skill's instructions

## Template Structure

```
your-skill/
├── skill.json       # Skill manifest
└── instructions.md  # AI instructions
```

## Required Fields in skill.json

- `id`: Unique identifier (domain/name format)
- `name`: Human-readable name
- `description`: What the skill does and when to use it
- `domain`: Should be "marketing"
- `tags`: Relevant tags for discovery

## Writing Good Instructions

1. Start with an overview of what the skill does
2. List specific use cases
3. Provide step-by-step guidance
4. Include examples where helpful
5. Define success criteria and exit conditions