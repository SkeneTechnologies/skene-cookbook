# Build Your First Skill

**A step-by-step guide to creating and contributing a new skill to the Skene Skills Directory**

This tutorial walks you through creating a simple skill from scratch. We'll build a `competitor_mention_tracker` skill that monitors mentions of competitors in customer conversations.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1: Plan Your Skill](#step-1-plan-your-skill)
- [Step 2: Set Up Your Environment](#step-2-set-up-your-environment)
- [Step 3: Create Skill Structure](#step-3-create-skill-structure)
- [Step 4: Write skill.json](#step-4-write-skilljson)
- [Step 5: Write instructions.md](#step-5-write-instructionsmd)
- [Step 6: Run Security Analysis](#step-6-run-security-analysis)
- [Step 7: Test Your Skill](#step-7-test-your-skill)
- [Step 8: Submit Your Skill](#step-8-submit-your-skill)
- [Best Practices](#best-practices)
- [Security Checklist](#security-checklist)

---

## Prerequisites

**Required:**

- Git installed
- Node.js 18+ installed
- Python 3.8+ installed (for security analysis)
- GitHub account

**Helpful:**

- Familiarity with JSON format
- Basic command line usage
- Understanding of the domain you're contributing to

---

## Step 1: Plan Your Skill

Before writing code, answer these questions:

### What does your skill do?

**Example:** Tracks competitor mentions in customer conversations and emails

### Which domain does it belong to?

**Example:** `sales` or `customer_success`

**Available domains:**

- `sales` - Pipeline, deals, CRM
- `marketing` - Campaigns, content, SEO
- `customer_success` - Health, churn, retention
- `finops` - Billing, revenue, financial
- `product_ops` - Roadmap, releases, features
- `security` - Security, compliance, auditing
- `devex` - Developer experience, tools
- `plg` - Product-led growth
- `scientific` - Research, data analysis
- ...and more

### What are the inputs?

**Example:**

- `conversation_id` - ID of conversation to analyze
- `competitors` - List of competitor names to track
- `time_range` - Time period to analyze

### What are the outputs?

**Example:**

- `mentions_found` - Number of competitor mentions
- `competitor_breakdown` - Mentions per competitor
- `context` - Surrounding text for each mention
- `sentiment` - Sentiment analysis (positive/negative/neutral)

### What tools does it need?

**Example:**

- `crm.conversations.read` - Read conversation data
- `ai.analyze_text` - Analyze text for mentions
- `ai.sentiment_analysis` - Sentiment scoring

---

## Step 2: Set Up Your Environment

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/skene-cookbook.git
cd skene-cookbook

# 2. Install dependencies
npm install
pip install pyyaml jsonschema

# 3. Create a new branch
git checkout -b add-skill-competitor-mention-tracker
```

---

## Step 3: Create Skill Structure

```bash
# Create skill directory
mkdir -p skills-library/sales/competitor_mention_tracker

# Navigate to it
cd skills-library/sales/competitor_mention_tracker

# Create required files
touch skill.json
touch instructions.md
```

Your structure should look like:

```
skills-library/sales/competitor_mention_tracker/
├── skill.json        # Skill definition and schema
└── instructions.md   # Execution instructions
```

---

## Step 4: Write skill.json

Create `skill.json` with this template:

```json
{
  "id": "sales_competitor_mention_tracker",
  "version": "1.0.0",
  "name": "Competitor Mention Tracker",
  "description": "Tracks and analyzes competitor mentions in customer conversations",
  "domain": "sales",

  "tools": [
    {
      "name": "crm.conversations.read",
      "required": true,
      "description": "Read conversation history from CRM"
    },
    {
      "name": "ai.analyze_text",
      "required": true,
      "description": "Analyze text for keyword mentions"
    },
    {
      "name": "ai.sentiment_analysis",
      "required": false,
      "description": "Analyze sentiment of mentions"
    }
  ],

  "inputSchema": {
    "type": "object",
    "required": ["conversation_id", "competitors"],
    "properties": {
      "conversation_id": {
        "type": "string",
        "description": "ID of the conversation to analyze"
      },
      "competitors": {
        "type": "array",
        "items": { "type": "string" },
        "description": "List of competitor names to track",
        "example": ["Competitor A", "Competitor B"]
      },
      "time_range": {
        "type": "string",
        "enum": ["7d", "30d", "90d", "all"],
        "default": "30d",
        "description": "Time range for analysis"
      },
      "include_sentiment": {
        "type": "boolean",
        "default": true,
        "description": "Whether to include sentiment analysis"
      }
    }
  },

  "outputSchema": {
    "type": "object",
    "properties": {
      "total_mentions": {
        "type": "integer",
        "description": "Total number of competitor mentions found"
      },
      "competitor_breakdown": {
        "type": "object",
        "description": "Mentions count per competitor",
        "additionalProperties": { "type": "integer" }
      },
      "mentions": {
        "type": "array",
        "description": "Detailed mention data",
        "items": {
          "type": "object",
          "properties": {
            "competitor": { "type": "string" },
            "context": { "type": "string" },
            "timestamp": { "type": "string", "format": "date-time" },
            "sentiment": {
              "type": "string",
              "enum": ["positive", "neutral", "negative"]
            }
          }
        }
      },
      "summary": {
        "type": "string",
        "description": "AI-generated summary of findings"
      }
    }
  },

  "exitStates": {
    "mentions_found": {
      "description": "Competitor mentions were found",
      "nextRecommendation": ["competitive_analysis", "competitive_battlecard"]
    },
    "no_mentions": {
      "description": "No competitor mentions found",
      "nextRecommendation": null
    },
    "error": {
      "description": "Error during analysis",
      "nextRecommendation": null
    }
  },

  "tags": ["sales", "competitive-intelligence", "conversation-analysis", "sentiment-analysis"],

  "jobFunctions": ["sales_ops", "competitive_intelligence", "product_marketing"],

  "platforms": {
    "claude": {
      "triggers": [
        "track competitor mentions",
        "analyze competitor mentions in conversation",
        "find competitor references"
      ]
    },
    "cursor": {
      "triggers": ["competitor_mention_tracker"]
    }
  }
}
```

### Key Fields Explained:

- **id**: Unique identifier in format `domain_skill_name`
- **tools**: External tools this skill needs (CRM, AI, etc.)
- **inputSchema**: What data the skill expects (with validation)
- **outputSchema**: What data the skill returns
- **exitStates**: Possible outcomes and recommended next skills
- **tags**: Searchable keywords
- **jobFunctions**: Who would use this skill
- **platforms**: How users invoke the skill in Claude/Cursor

---

## Step 5: Write instructions.md

Create `instructions.md` with clear execution steps:

```markdown
# Competitor Mention Tracker

## Purpose

Automatically tracks and analyzes competitor mentions in customer conversations, providing insights into competitive dynamics and customer sentiment.

## When to Use

- **Competitive intelligence**: Track how often competitors come up
- **Deal risk assessment**: Identify deals with competitive pressure
- **Product positioning**: Understand how customers compare products
- **Win/loss analysis**: Correlate competitor mentions with outcomes

## Prerequisites

### Required Tools

- `crm.conversations.read` - Access to conversation history
- `ai.analyze_text` - Text analysis capability

### Optional Tools

- `ai.sentiment_analysis` - For sentiment scoring

### Data Access

- Read access to CRM conversation data
- List of competitor names to track

## Execution Steps

### 1. Fetch Conversation Data

- Retrieve conversation history for given `conversation_id`
- Filter by `time_range` if specified
- Pull full conversation thread (not just summary)

### 2. Analyze for Competitor Mentions

For each competitor in `competitors` list:

- Search conversation text for mentions (case-insensitive)
- Include variations (e.g., "Acme", "Acme Corp", "Acme Software")
- Extract surrounding context (±50 words)
- Record timestamp of mention

### 3. Sentiment Analysis (if enabled)

For each mention found:

- Analyze sentiment of context (positive/neutral/negative)
- Score confidence (0-1)
- Flag highly positive or negative mentions

### 4. Generate Summary

- Count total mentions
- Break down by competitor
- Identify patterns or trends
- Generate actionable summary

### 5. Return Results

Exit with appropriate state:

- `mentions_found`: If 1+ mentions detected
- `no_mentions`: If 0 mentions found
- `error`: If analysis failed

## Example Usage

### Input

\`\`\`json
{
"conversation_id": "conv_12345",
"competitors": ["Competitor A", "Competitor B"],
"time_range": "30d",
"include_sentiment": true
}
\`\`\`

### Output

\`\`\`json
{
"total_mentions": 3,
"competitor_breakdown": {
"Competitor A": 2,
"Competitor B": 1
},
"mentions": [
{
"competitor": "Competitor A",
"context": "We looked at Competitor A but their pricing was too high...",
"timestamp": "2026-01-15T10:30:00Z",
"sentiment": "negative"
},
{
"competitor": "Competitor A",
"context": "Competitor A has a nice feature for reporting...",
"timestamp": "2026-01-20T14:15:00Z",
"sentiment": "positive"
},
{
"competitor": "Competitor B",
"context": "Currently using Competitor B but not satisfied...",
"timestamp": "2026-01-25T09:00:00Z",
"sentiment": "negative"
}
],
"summary": "3 competitor mentions found. Customer evaluated Competitor A (pricing concerns) and is currently using Competitor B with dissatisfaction. Opportunity to position on price/value and switching benefits."
}
\`\`\`

## Error Handling

### Common Errors

**Error: Conversation not found**

- Cause: Invalid `conversation_id`
- Solution: Verify conversation ID exists in CRM
- Exit state: `error`

**Error: Insufficient permissions**

- Cause: Missing read access to conversations
- Solution: Grant `crm.conversations.read` permission
- Exit state: `error`

**Error: Rate limit exceeded**

- Cause: Too many API calls to CRM
- Solution: Implement rate limiting, retry with backoff
- Exit state: `error`

## Security Considerations

### Data Access

- **Scope**: Read-only access to conversation data
- **Sensitivity**: May contain customer PII and confidential discussions
- **Retention**: Do not store conversation data beyond analysis

### Risk Level

**Medium** - Accesses customer conversation data

### Required Security Controls

- ✅ Audit logging enabled
- ✅ Read-only access (no modifications)
- ⚠️ Recommend human review for sensitive accounts

### Compliance Notes

- Ensure compliance with data retention policies
- Mask PII in exported reports if required
- Log all access for audit trails

## Recommended Next Skills

If `mentions_found`:

- `competitive_battlecard` - Generate battle card for mentioned competitor
- `competitive_analysis` - Deep dive into competitive positioning
- `win_loss_analyzer` - Correlate mentions with deal outcomes

## Performance Notes

- **Typical execution time**: 2-5 seconds per conversation
- **Rate limits**: Respects CRM API limits (typically 100 req/min)
- **Scalability**: Can batch process up to 100 conversations/run

## Version History

- **v1.0.0** (2026-02-06): Initial release
```

---

## Step 6: Run Security Analysis

Run the security analysis tool:

```bash
# From repository root
python scripts/analyze_skills.py --action metadata

# This generates metadata.yaml in your skill directory
```

Review the generated `metadata.yaml`:

```yaml
risk_level: 'Medium'
security_requirements:
  audit_logging: true
  read_only: true
  human_in_loop_recommended: true
  data_access_scope:
    - 'customer_conversations'
    - 'crm_data'

job_function: 'sales_ops'
jtbd: 'Track competitive mentions in customer conversations'
```

**Risk Levels:**

- **Low**: Read-only, public data, no credentials
- **Medium**: Read-only, internal data, some credentials
- **High**: Write operations, financial data, PII access
- **Critical**: Destructive operations, payment processing

---

## Step 7: Test Your Skill

### Manual Testing

1. **Validate JSON syntax**:

   ```bash
   cat skill.json | python -m json.tool
   ```

2. **Check schema compliance** (future feature):

   ```bash
   npm run validate:skill skills-library/sales/competitor_mention_tracker/skill.json
   ```

3. **Test with sample data**:
   - Create test input matching your inputSchema
   - Verify outputs match outputSchema
   - Test error cases

### Testing Checklist

- [ ] JSON is valid and well-formatted
- [ ] All required fields present
- [ ] inputSchema has examples
- [ ] outputSchema is complete
- [ ] instructions.md has clear steps
- [ ] Error handling documented
- [ ] Security considerations listed
- [ ] Exit states defined

---

## Step 8: Submit Your Skill

### 1. Commit Your Changes

```bash
# Add your skill files
git add skills-library/sales/competitor_mention_tracker/

# Commit with descriptive message
git commit -m "feat: add competitor_mention_tracker skill to sales domain

- Tracks competitor mentions in conversations
- Includes sentiment analysis
- Medium risk level (read-only access to CRM data)
- Tested with sample conversations"

# Push to your fork
git push origin add-skill-competitor-mention-tracker
```

### 2. Create Pull Request

Go to GitHub and create a PR with this template:

```markdown
## Skill Addition: Competitor Mention Tracker

**Domain:** sales
**Risk Level:** Medium
**Job Function:** sales_ops, competitive_intelligence

### Description

Tracks and analyzes competitor mentions in customer conversations with sentiment analysis. Helps sales teams understand competitive dynamics and position against alternatives.

### Key Features

- Searches conversation history for competitor names
- Extracts context around each mention
- Sentiment analysis (positive/neutral/negative)
- Actionable summary of findings
- Recommended next skills for follow-up

### Security Analysis

**Risk Level**: Medium

- Read-only access to customer conversation data
- No write operations
- Audit logging enabled
- PII considerations in conversation content

**Required Controls**:

- ✅ Audit logging
- ✅ Read-only access
- ⚠️ Human review recommended for sensitive accounts

### Testing

- [x] Tested standalone execution with sample data
- [x] Validated input/output schemas
- [x] Ran security analysis
- [x] Tested error handling (invalid IDs, rate limits)
- [x] Verified exit states work correctly

### Use Cases

1. **Deal Risk Assessment**: Identify deals with strong competitive pressure
2. **Win/Loss Analysis**: Correlate competitor mentions with outcomes
3. **Competitive Intelligence**: Track which competitors are most mentioned
4. **Product Positioning**: Understand how customers compare products

### Checklist

- [x] skill.json follows schema
- [x] instructions.md is complete and clear
- [x] metadata.yaml generated from security analysis
- [x] No security vulnerabilities
- [x] Examples provided
- [x] Exit states defined with recommendations
- [x] Tags and job functions assigned
```

### 3. Wait for Review

Maintainers will review your skill for:

- ✅ Schema compliance
- ✅ Security requirements
- ✅ Documentation quality
- ✅ Use case value

**Typical review time**: 3-5 business days

---

## Best Practices

### DO ✅

- **Be atomic**: One skill = one clear purpose
- **Be specific**: Clear inputs, outputs, and behavior
- **Document thoroughly**: Examples, errors, security
- **Think composable**: Define exit states and next skill recommendations
- **Test extensively**: Multiple scenarios, error cases
- **Consider security**: Always run security analysis

### DON'T ❌

- **Don't be vague**: Avoid unclear descriptions
- **Don't skip schemas**: Always define input/output schemas
- **Don't ignore security**: Always complete security analysis
- **Don't bypass reviews**: Security checks are mandatory
- **Don't copy proprietary code**: Respect IP and licenses

---

## Security Checklist

Before submitting, verify:

- [ ] Risk level assessed (Low/Medium/High/Critical)
- [ ] Data access scope documented
- [ ] Security requirements defined
- [ ] No hardcoded credentials or secrets
- [ ] Audit logging specified if needed
- [ ] Human-in-loop requirement noted if applicable
- [ ] PII handling documented
- [ ] Destructive operations flagged (if any)
- [ ] Rate limiting considered
- [ ] Error messages don't leak sensitive info

---

## Need Help?

- **Questions about skill structure**: See [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Security questions**: See [SECURITY_POLICY.md](../SECURITY_POLICY.md)
- **Technical issues**: [Open an issue](https://github.com/SkeneTechnologies/skene-cookbook/issues/new)
- **Discussions**: [GitHub Discussions](https://github.com/SkeneTechnologies/skene-cookbook/discussions)

---

## Next Steps

After your skill is merged:

1. **Test in production**: Install and use your skill
2. **Create skill chains**: Combine with other skills
3. **Share your workflow**: Add to [SHOWCASE.md](SHOWCASE.md)
4. **Iterate**: Improve based on usage feedback

**Thank you for contributing to Skene Skills Directory!** 🎉

Every skill you add makes AI agents more powerful for everyone.
