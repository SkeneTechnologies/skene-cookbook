# SKILL-LOOM CLI Guide

## Overview

The SKILL-LOOM CLI is an interactive ASCII terminal interface for browsing and managing the Skills Directory. Built with Python and Rich, it provides a beautiful command-line experience for exploring 808+ AI skills.

## Installation

### Prerequisites

```bash
# Python 3.8+ required
python3 --version

# Install dependencies
pip3 install rich pyfiglet
```

### Quick Start

```bash
# Launch the CLI
python3 skill-loom-cli.py

# Or make it globally accessible
chmod +x skill-loom-cli.py
./skill-loom-cli.py
```

## Features

### 1. Browse by Job Function

Navigate through 13 job functions to find skills relevant to your role:

- **Engineering** (271 skills)
- **Data** (129 skills)
- **Marketing** (84 skills)
- **Design** (77 skills)
- **Customer Success** (69 skills)
- And 8 more...

Each function displays:
- Total skill count
- Risk level distribution
- Top risk classification

### 2. Search Skills

Fuzzy search across all 808 skills:

```
Enter search term: partner
Found 45 results for 'partner'
```

Search looks for matches in:
- Skill IDs
- Job descriptions (JTBD)
- Tags and metadata

### 3. Security Audit View

Color-coded security dashboard:

```
┌──────────┬───────┬──────────┬────────────┐
│ Level    │ Count │ Percent  │ Visual     │
├──────────┼───────┼──────────┼────────────┤
│ Critical │   0   │   0.0%   │            │
│ High     │ 227   │  28.1%   │ ████████   │
│ Medium   │ 330   │  40.8%   │ ████████████│
│ Low      │ 251   │  31.1%   │ ██████████  │
└──────────┴───────┴──────────┴────────────┘
```

Features:
- Overall security posture
- Risk breakdown by job function
- Color-coded visualization (Red/Yellow/Cyan/Green)

### 4. Workflow Chains

View and explore workflow blueprints:

- Visual ASCII representation of skill chains
- Step-by-step execution flow
- Conditional logic and error handling
- Security context and approval requirements

### 5. Statistics Dashboard

Comprehensive metrics:
- Total skills and job functions
- Top 5 job functions by skill count
- Remediation impact statistics
- Estimated cost savings

### 6. Skill Details

Detailed view for each skill:
- Job to be Done (JTBD) description
- Required tools and dependencies
- Security controls applied
- Domain and tags
- Risk level and requirements

## CLI Navigation

### Menu Options

```
┌──────────┬────────────────────────────┐
│ 1        │ 📋 Browse by Job Function  │
│ 2        │ 🔍 Search Skills           │
│ 3        │ 🔒 Security Audit View     │
│ 4        │ 🔗 View Workflow Chains    │
│ 5        │ 📊 Statistics Dashboard    │
│ 6        │ ℹ️  About Skills Directory │
│ 0        │ 🚪 Exit                    │
└──────────┴────────────────────────────┘
```

### Keyboard Shortcuts

- **Number keys** - Select menu options
- **Enter** - Confirm selection or continue
- **0** - Return to previous menu or exit
- **Ctrl+C** - Exit immediately

## Examples

### Example 1: Find Engineering Skills

```bash
python3 skill-loom-cli.py
# Select: 1 (Browse by Job Function)
# Select: 1 (Engineering)
# Browse through 271 engineering skills
```

### Example 2: Search for Payment Skills

```bash
python3 skill-loom-cli.py
# Select: 2 (Search Skills)
# Enter: payment
# View all payment-related skills
```

### Example 3: Check Security Status

```bash
python3 skill-loom-cli.py
# Select: 3 (Security Audit View)
# View color-coded risk distribution
# Check security posture
```

## Advanced Usage

### Batch Operations

While the CLI is interactive, you can script basic navigation:

```bash
# Example: Navigate to statistics view
echo -e "5\n0" | python3 skill-loom-cli.py
```

### Integration with Other Tools

```bash
# Export skill list
python3 -c "
import json
with open('registry/job_functions/index.json', 'r') as f:
    data = json.load(f)
    for func, skills in data.items():
        print(f'{func}: {len(skills)} skills')
"
```

### Custom Queries

Use the Python API directly:

```python
import json

# Load registry
with open('registry/job_functions/index.json', 'r') as f:
    job_functions = json.load(f)

# Find high-risk marketing skills
marketing_skills = job_functions['marketing']
high_risk = [s for s in marketing_skills if s['risk_level'] in ['High', 'Critical']]

print(f"Found {len(high_risk)} high-risk marketing skills")
for skill in high_risk:
    print(f"  - {skill['skill_id']}: {skill['risk_level']}")
```

## Color Scheme

The CLI uses semantic coloring:

- **Cyan** - Headers, prompts, navigation
- **Green** - Success, low risk, confirmations
- **Yellow** - Warnings, high risk, attention needed
- **Red** - Critical risk, errors, dangerous operations
- **White/Dim** - Regular text, secondary information

## Troubleshooting

### Import Error: rich module not found

```bash
pip3 install rich pyfiglet
```

### Import Error: registry not found

Make sure you're running from the project root:

```bash
cd /path/to/skene-skills-directory
python3 skill-loom-cli.py
```

### Display Issues

If text appears garbled:

```bash
# Check terminal encoding
echo $LANG

# Should be UTF-8
export LANG=en_US.UTF-8
```

### Performance

The CLI is optimized for fast loading:
- Registry loaded once at startup
- Paginated views (max 30 items)
- Efficient search algorithms

## Tips & Tricks

1. **Use numbers for quick navigation** - Type `1` to browse, `2` to search, etc.

2. **Search is your friend** - With 808 skills, searching is faster than browsing

3. **Check security first** - Use option 3 to understand the security landscape

4. **Export data** - The registry JSON can be imported into other tools

5. **Bookmark favorites** - Note skill IDs for quick reference

## Future Enhancements

Planned features:
- Skill comparison view
- Export to CSV/JSON
- Custom filters and saved searches
- Workflow execution simulation
- Integration with CI/CD pipelines

## Support

- **Documentation:** [docs/](../docs/)
- **Issues:** Open a GitHub issue
- **CLI Source:** [`skill-loom-cli.py`](../skill-loom-cli.py)

---

**Built with ❤️ using Python, Rich, and ASCII Art**
