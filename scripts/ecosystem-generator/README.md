# Skene Ecosystem Generator

Automatically generates tailored ecosystem recommendations based on the host repository's tech stack.

## Overview

When users install `@skene/skills-directory` in their projects, they receive personalized promotional content about other SkeneTechnologies repositories that complement their specific stack.

## Features

- **Automatic detection** of repo type (Next.js, React, Node.js, Python, docs, generic)
- **Live GitHub data** fetching from SkeneTechnologies org
- **Benefit-focused copy** extracted from README first paragraphs
- **Relevance-based ordering** tailored to detected repo type
- **Smart caching** with 1-hour TTL to minimize API calls
- **Role-based customization** (frontend, backend, etc.)

## Architecture

```
scripts/ecosystem-generator/
├── cli.ts                    # Main entry point & orchestration
├── github-client.ts          # GitHub API wrapper (fetch repos + READMEs)
├── cache-manager.ts          # File-based caching with TTL
├── repo-detector.ts          # Detect host repo type
├── relevance-mapper.ts       # RELEVANCE_CONFIG & ordering logic
├── markdown-generator.ts     # Format final output
├── types.ts                  # TypeScript interfaces
└── config.ts                 # Constants (org name, TTL, etc.)
```

## Usage

### Manual CLI

```bash
# Print to stdout (default)
npx skills-directory ecosystem

# Save to file
npx skills-directory ecosystem --output ECOSYSTEM.md

# Force refresh cache
npx skills-directory ecosystem --no-cache

# Role-based ordering
npx skills-directory ecosystem --role frontend

# Different repo
npx skills-directory ecosystem --repo-root /path/to/project
```

### Automatic (Postinstall)

When users install `@skene/skills-directory`, the postinstall script automatically:
1. Installs skills to Claude/Cursor
2. Generates `ECOSYSTEM.md` in their project root
3. Tailors content based on detected repo type

### Environment Variables

- `GITHUB_TOKEN` - GitHub personal access token (optional, increases rate limits)
- `SKENE_ECOSYSTEM_ROLE` - Default role for relevance ordering

## Detection Logic

The repo detector follows this priority order:

1. **Next.js** - `package.json` contains `next` dependency
2. **React** - `package.json` contains `react` dependency
3. **Node.js** - `package.json` exists
4. **Python** - `pyproject.toml`, `requirements.txt`, `setup.py`, or `Pipfile` exists
5. **Docs** - Doc-heavy structure (many `.md` files, `docs/` directory)
6. **Generic** - Default fallback

## Relevance Configuration

Repos are ordered by relevance to the detected type:

- **Next.js**: skene-dashboard → skene-flow → skene-cookbook → skene-growth
- **React**: skene-dashboard → skene-cookbook → skene-flow
- **Node.js**: skene-flow → skene-cookbook → skene-dashboard
- **Python**: skene-cookbook → skene-flow → skene-strategy
- **Docs**: skene-cookbook → skene-dashboard → skene-flow
- **Generic**: skene-cookbook → skene-flow → skene-dashboard → skene-growth

Role overrides (e.g., `--role frontend`) further customize ordering.

## Caching

- **Cache location**: `.skene/cache/` in repo root (fallback to `/tmp/`)
- **TTL**: 1 hour (3600000ms)
- **Cache keys**:
  - `org-repos-SkeneTechnologies` - List of all repos
  - `readme-{repoName}` - Individual README benefit lines

Caching significantly reduces GitHub API calls and improves performance.

## Output Format

```markdown
## Skene Ecosystem

{Tailored intro based on repo type}

### [repo-name](https://github.com/SkeneTechnologies/repo-name)
{Benefit-oriented line extracted from README}

**[Secondary link text](url)** (for specific repos)

---

**Explore all Skene repositories:** https://github.com/SkeneTechnologies
```

## Error Handling

The generator gracefully degrades on errors:

- **GitHub 403 (rate limit)**: Log warning, use cache or fallback
- **GitHub 404**: Skip repo/README, continue with others
- **Network timeout**: Retry once (1s delay), then skip
- **README parse failure**: Use repo description
- **No benefit line**: Fallback to "Explore {repo}"
- **Cache write failure**: Continue without cache

The generator always produces output, even if it's a generic fallback message.

## Integration Points

1. **Postinstall** - Automatically generates `ECOSYSTEM.md` when users install the package
2. **Manual CLI** - Users can run `npx skills-directory ecosystem` anytime
3. **Context Sync** - Could be called by context synchronization checkers to refresh stale content

## Dependencies

- **Zero external dependencies** - Uses built-in Node.js `fetch` and `fs/promises`
- Requires Node.js 18+ (for native `fetch` support)

## Future Enhancements

- [ ] Support for more repo types (Go, Rust, Java, etc.)
- [ ] GitHub GraphQL API for better rate limits
- [ ] Integration with Claude Code context sync
- [ ] Multi-language README support
- [ ] Analytics on which repos users engage with
- [ ] A/B testing of intro copy
