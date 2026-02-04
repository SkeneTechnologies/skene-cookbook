---
name: Prompt Engineering
description: Best practices for writing effective AI prompts. Use when crafting prompts for LLMs, creating system prompts, designing agent instructions, or optimizing AI outputs.
---

# Prompt Engineering

A systematic approach to writing effective prompts for AI systems.

## Core Principles

### 1. Be Specific, Not Vague

❌ **Bad**: "Write something about dogs"
✅ **Good**: "Write a 200-word blog post about the benefits of adopting senior dogs, targeting first-time dog owners"

### 2. Provide Context

❌ **Bad**: "Fix this code"
✅ **Good**: "Fix this TypeScript function that calculates user subscription costs. It should handle monthly and annual billing, with a 20% discount for annual plans. Current bug: returns NaN for annual subscriptions."

### 3. Specify Format

❌ **Bad**: "Give me a summary"
✅ **Good**: "Summarize this article in 3 bullet points, each under 20 words"

## Prompt Structure

### Basic Template

```
[ROLE/CONTEXT]
You are a [role] helping with [task].

[TASK]
Your task is to [specific action].

[INPUT]
Here is the [input type]:
{input}

[FORMAT]
Respond in the following format:
- [format specification]

[CONSTRAINTS]
Important rules:
- [constraint 1]
- [constraint 2]
```

### Example

```
You are a senior software engineer reviewing code for security vulnerabilities.

Your task is to identify potential security issues in the following code and suggest fixes.

Here is the code to review:
{code}

Respond in the following format:
1. **Issue**: [description]
   **Severity**: [Critical/High/Medium/Low]
   **Fix**: [suggested fix]

Important rules:
- Focus only on security issues, not style
- Prioritize by severity
- Include code examples for fixes
```

## Techniques

### Chain of Thought

For complex reasoning, ask for step-by-step thinking:

```
Solve this problem step by step:
1. First, identify what we know
2. Then, determine what we need to find
3. Apply the relevant formula/logic
4. Calculate the answer
5. Verify the result
```

### Few-Shot Examples

Provide examples of desired output:

```
Convert these sentences to formal business language.

Example 1:
Input: "Hey, can we chat about the project later?"
Output: "I would like to schedule a meeting to discuss the project at your earliest convenience."

Example 2:
Input: "This deadline is crazy tight!"
Output: "The timeline for this deliverable presents significant challenges."

Now convert:
Input: "{user_input}"
```

### Negative Examples

Show what NOT to do:

```
Write a professional email response.

DO NOT:
- Use casual language like "Hey" or "What's up"
- Include emojis
- Be overly wordy

DO:
- Use a formal greeting
- Be concise and clear
- Include a clear call to action
```

### Role Assignment

Assign a specific persona:

```
You are a Kubernetes expert with 10 years of experience in production deployments.
You explain concepts clearly to developers who are new to container orchestration.
You always provide practical examples alongside theory.
```

## Prompt Patterns

### Classification

```
Classify the following customer message into one of these categories:
- billing
- technical_support
- feature_request
- general_inquiry

Message: "{message}"

Respond with only the category name.
```

### Extraction

```
Extract the following information from this job posting:
- Job title
- Required years of experience
- Required skills (as a list)
- Salary range (if mentioned)

Job posting:
{posting}

Return as JSON.
```

### Generation with Constraints

```
Write a product description for {product}.

Constraints:
- Exactly 50-75 words
- Include 2 key benefits
- End with a call to action
- Use active voice
- Target audience: {audience}
```

### Analysis

```
Analyze this code for performance issues.

For each issue found:
1. Describe the problem
2. Explain the impact
3. Suggest an optimized solution
4. Estimate the improvement

Code:
{code}
```

## Testing Prompts

### Test Cases

Always test with:
1. **Happy path** — Normal, expected input
2. **Edge cases** — Empty, very long, special characters
3. **Adversarial** — Attempts to break or manipulate
4. **Domain-specific** — Industry/context-specific scenarios

### Iteration Loop

```
1. Write initial prompt
2. Test with 5+ varied inputs
3. Identify failure modes
4. Refine prompt
5. Repeat until consistent
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too vague | Add specific details and constraints |
| Too long | Remove unnecessary context, focus on essentials |
| No examples | Add 2-3 clear examples |
| Ambiguous output format | Specify exact format (JSON, bullets, etc.) |
| Missing edge cases | Add explicit handling for edge cases |
| Assuming knowledge | Provide necessary context |

## System Prompt Best Practices

For AI agents/assistants:

```
You are [role] for [company/product].

## Core Behavior
- [Key behavior 1]
- [Key behavior 2]

## Capabilities
You CAN:
- [Capability 1]
- [Capability 2]

You CANNOT:
- [Limitation 1]
- [Limitation 2]

## Response Style
- [Style guideline 1]
- [Style guideline 2]

## Important Rules
- [Critical rule 1]
- [Critical rule 2]
```

## Evaluation Criteria

Rate prompts on:
1. **Clarity** — Is the task unambiguous?
2. **Completeness** — Is all necessary context provided?
3. **Specificity** — Are output requirements clear?
4. **Robustness** — Does it handle edge cases?
5. **Efficiency** — Is it as concise as possible?
