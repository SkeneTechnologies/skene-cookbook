---
name: Code Review Checklist
description: Systematic code review checklist covering correctness, security, performance, maintainability, and style. Use when reviewing PRs, doing code audits, or before merging changes.
---

# Code Review Checklist

A systematic approach to reviewing code changes for quality, security, and maintainability.

## Review Process

### 1. Understand Context First

Before reviewing code:
- Read the PR description/ticket
- Understand the problem being solved
- Check if the approach makes sense for the problem

### 2. Correctness Check

| Check | Questions |
|-------|-----------|
| **Logic** | Does the code do what it claims? Are edge cases handled? |
| **Requirements** | Does it meet the spec/ticket requirements? |
| **Tests** | Are there tests? Do they cover the key paths? |
| **Errors** | Are errors handled gracefully? No silent failures? |

### 3. Security Check

| Check | Questions |
|-------|-----------|
| **Input Validation** | Is user input validated and sanitized? |
| **Authentication** | Are auth checks in place where needed? |
| **Authorization** | Are permission checks correct? |
| **Data Exposure** | Is sensitive data properly protected? |
| **Injection** | SQL, XSS, command injection risks? |
| **Secrets** | No hardcoded credentials or API keys? |

### 4. Performance Check

| Check | Questions |
|-------|-----------|
| **Complexity** | O(n²) loops? Unnecessary iterations? |
| **Database** | N+1 queries? Missing indexes? |
| **Memory** | Large objects held unnecessarily? Memory leaks? |
| **Caching** | Should this be cached? Cache invalidation correct? |
| **Async** | Should this be async? Blocking the main thread? |

### 5. Maintainability Check

| Check | Questions |
|-------|-----------|
| **Naming** | Are names clear and descriptive? |
| **Functions** | Single responsibility? Not too long? |
| **Comments** | Complex logic explained? No obvious comments? |
| **Duplication** | DRY principle followed? |
| **Dependencies** | New deps necessary? Are they maintained? |

### 6. Style Check

| Check | Questions |
|-------|-----------|
| **Consistency** | Follows project conventions? |
| **Formatting** | Properly formatted? Linter passing? |
| **Types** | TypeScript types correct and useful? |

## Response Format

After review, provide:

```markdown
## Review Summary

**Verdict**: [Approved / Changes Requested / Needs Discussion]

### Issues (must fix)
- [ ] Issue 1: Description and location
- [ ] Issue 2: Description and location

### Suggestions (optional improvements)
- Suggestion 1: Description
- Suggestion 2: Description

### Questions
- Question about design decision?

### Positive Notes
- Good: Something done well
```

## Review Etiquette

1. **Be constructive** — Suggest solutions, not just problems
2. **Be specific** — Point to exact lines/code
3. **Explain why** — Help the author learn
4. **Prioritize** — Distinguish critical issues from nits
5. **Be timely** — Don't block PRs unnecessarily

## Common Patterns to Flag

### Red Flags
- `TODO` without ticket
- `console.log` in production code
- Commented-out code
- Magic numbers without constants
- `any` type in TypeScript
- Missing error boundaries
- Hardcoded URLs/IPs

### Yellow Flags
- Long functions (>50 lines)
- Deep nesting (>3 levels)
- Multiple responsibilities
- Missing null checks
- Inconsistent naming
