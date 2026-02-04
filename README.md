# Skills Directory

**800+ AI skills for Claude and Cursor** — PLG, marketing, security, DevEx, and more.

One command to install. No API keys. No setup.

## Install

```bash
npm install @skene/skills-directory
```

## Activate Skills

```bash
# Install to Cursor and Claude
npx skills-directory install --target all

# Cursor only
npx skills-directory install --target cursor

# Claude only
npx skills-directory install --target claude
```

## What's Included

| Category       | Skills | Description                          |
| -------------- | ------ | ------------------------------------ |
| Cursor Rules   | 241    | React, Next.js, Python, etc.        |
| Scientific     | 141    | Research, data science               |
| Marketing      | 73     | Content, SEO, campaigns              |
| PLG Frameworks | 43     | Product-led growth playbooks         |
| Customer Success | 28   | Health scoring, churn prevention     |
| RevOps         | 25     | Pipeline, forecasting                |
| ... and 19 more domains | | **Total: 800+ skills**          |

## How It Works

Skills are installed to:

- **Cursor:** `~/.cursor/skills/`
- **Claude:** `~/.claude/skills/`

Cursor and Claude automatically pick the right skill based on your prompt. No configuration needed.

## Commands

| Command                              | Description                |
| ------------------------------------ | -------------------------- |
| `npx skills-directory install`       | Install to Cursor + Claude |
| `npx skills-directory stats`         | Show library statistics   |
| `npx skills-directory list --domain plg` | List skills by domain |
| `npx skills-directory uninstall`     | Remove installed skills    |

## Skill Sources

- Anthropic Official, Trail of Bits, obra/superpowers, K-Dense-AI, awesome-cursor-rules, Skene PLG

## License

MIT
