---
name: Codebase Onboarding
description: Systematic approach to understanding a new codebase. Use when joining a project, exploring unfamiliar code, or helping someone understand a repo structure.
---

# Codebase Onboarding

A systematic approach to quickly understand and navigate unfamiliar codebases.

## Exploration Strategy

### Phase 1: High-Level Overview (5 min)

1. **Read README.md**
   - What does this project do?
   - What problem does it solve?
   - How do you run it?

2. **Check package.json / Cargo.toml / requirements.txt**
   - What's the tech stack?
   - What are the main dependencies?
   - What scripts are available?

3. **Scan Directory Structure**
   ```
   Look for:
   - src/ or lib/ — Main source code
   - tests/ — Test files (reveal intended behavior)
   - docs/ — Documentation
   - config/ — Configuration
   - scripts/ — Build/deploy scripts
   ```

### Phase 2: Entry Points (10 min)

Find where execution starts:

| Type | Common Entry Points |
|------|---------------------|
| **Web App** | `index.html`, `App.tsx`, `main.ts` |
| **API Server** | `server.ts`, `app.py`, `main.go` |
| **CLI** | `cli.ts`, `__main__.py`, `bin/` |
| **Library** | `index.ts`, `lib.rs`, `__init__.py` |

### Phase 3: Core Flow (15 min)

Trace ONE complete path through the code:

1. **Pick a simple feature**
   - User login
   - API endpoint
   - CLI command

2. **Follow the data**
   - Where does input enter?
   - What transformations happen?
   - Where does output go?

3. **Note key abstractions**
   - What patterns are used?
   - What are the main classes/modules?

### Phase 4: Testing & Docs (10 min)

1. **Read test files**
   - Tests reveal intended behavior
   - Test names describe features
   - Test data shows edge cases

2. **Check for architecture docs**
   - `ARCHITECTURE.md`
   - `docs/` folder
   - Code comments in key files

## Quick Assessment Checklist

```markdown
## Codebase Summary

**Project**: [Name]
**Purpose**: [One sentence description]
**Tech Stack**: [Languages, frameworks, databases]

### Architecture
- **Pattern**: [MVC, Clean Architecture, Microservices, etc.]
- **Entry Points**: [List main entry files]
- **Core Modules**: [List key directories/modules]

### Key Files to Read
1. [File] — [Why it's important]
2. [File] — [Why it's important]
3. [File] — [Why it's important]

### Data Flow
[Input] → [Processing] → [Output]

### Conventions
- **Naming**: [camelCase, snake_case, etc.]
- **File Structure**: [By feature, by type, etc.]
- **Testing**: [Jest, pytest, etc.]

### Questions to Investigate
- [ ] How does [X] work?
- [ ] Why is [Y] structured this way?
```

## Red Flags to Note

While exploring, note:
- Missing tests
- Outdated dependencies
- No documentation
- Inconsistent patterns
- Dead code
- `TODO` without tickets

## Tips for Speed

1. **Use search, not browse** — Search for keywords, not file-by-file
2. **Read tests first** — They're often clearer than implementation
3. **Follow imports** — They reveal dependencies
4. **Git blame key files** — See who knows what
5. **Run it locally** — Hands-on beats reading

## When You're Stuck

If a codebase is confusing:

1. Find the simplest working example (test or example file)
2. Add logging/breakpoints to trace execution
3. Read git history for context on decisions
4. Ask the team (if available)

Remember: You don't need to understand everything at once. Focus on the area you need to work in.
