# Security Policy

## Overview

The Skills Directory takes security seriously. Every skill is analyzed for potential risks, and high-risk skills require additional safeguards. This document explains our security framework and policies.

## Security Risk Levels

### Low Risk
**Definition**: Read-only operations, public data access, no external API calls

**Examples**:
- List available skills
- Format/transform data
- Calculate metrics
- Display information

**Requirements**:
- No special requirements
- Standard execution allowed
- Audit logging optional

### Medium Risk
**Definition**: Write operations, internal data access, external API calls without sensitive data

**Examples**:
- Send notifications
- Update non-critical records
- Query analytics
- Create tickets

**Requirements**:
- ✅ Audit logging enabled
- Standard execution allowed
- No sandboxing required

### High Risk
**Definition**: Modify/delete operations, PII access, sensitive data handling, risky external calls

**Examples**:
- Update customer records
- Access PII data
- Modify financial data
- Delete resources
- Execute external webhooks

**Requirements**:
- ✅ Sandboxing required
- ✅ Audit logging enabled
- ⚠️ Human-in-loop recommended
- Access controls enforced

### Critical Risk
**Definition**: Financial operations, credential handling, destructive actions, regulatory data

**Examples**:
- Process payments
- Access credentials/secrets
- Delete production data
- Modify financial records
- Execute system commands

**Requirements**:
- ✅ Sandboxing required
- ✅ Human-in-loop required
- ✅ Audit logging enabled
- ✅ Multi-party approval
- Access restricted to authorized personnel

## Security Requirements

### Sandboxing
Isolates skill execution to prevent:
- Unauthorized system access
- Data leakage
- Privilege escalation
- Resource exhaustion

**Implementation**: Skills run in isolated containers with limited permissions.

### Human-in-Loop (HITL)
Requires explicit human approval before execution.

**When Required**:
- Critical risk level skills
- Financial transactions
- Destructive operations
- Regulatory compliance needs

**Process**:
1. Skill execution initiated
2. Request sent to authorized approvers
3. Approver reviews context and impact
4. Approval or rejection
5. Execution proceeds or aborts

### Audit Logging
All executions are logged with:
- Skill ID and version
- Execution timestamp
- Input parameters (sanitized)
- Output results (sanitized)
- User/system that invoked
- Security context
- Success/failure status

**Retention**: Logs retained per compliance requirements (typically 90-365 days)

**Access**: Restricted to security team and authorized auditors

## Data Access Scope

Skills must declare what types of data they access:

| Scope | Description | Examples |
|-------|-------------|----------|
| `public` | Publicly available data | Documentation, public APIs |
| `internal` | Company-internal data | Internal analytics, metrics |
| `confidential` | Sensitive business data | Strategy, financials, deals |
| `pii` | Personally Identifiable Information | Names, emails, addresses |
| `financial` | Financial/payment data | Revenue, transactions, invoices |
| `health` | Health/medical data | PHI, medical records |

**Access Control**: Skills can only access scopes they declare, enforced at runtime.

## Security Analysis Process

### Automated Analysis

The `analyze_skills.py` script performs:

1. **Keyword Detection**
   - Scans skill.json and instructions.md
   - Identifies risk keywords (delete, financial, credential, etc.)
   - Weights keywords by severity

2. **Tool Risk Assessment**
   - Analyzes required tools
   - Identifies risky operations
   - Checks for external API calls

3. **Risk Level Assignment**
   - Aggregates risk factors
   - Assigns risk level (Low/Medium/High/Critical)
   - Generates risk factor list

4. **Security Requirements**
   - Determines sandboxing needs
   - Sets HITL requirements
   - Configures audit logging
   - Defines data access scope

5. **Metadata Generation**
   - Creates metadata.yaml with analysis results
   - Updates security indices
   - Generates reports

### Manual Review

All skills undergo manual security review before production:

1. **Automated Analysis**: Initial scan by analyzer
2. **Peer Review**: Code review by contributor
3. **Security Review**: Review by security team for High/Critical skills
4. **Approval**: Sign-off by maintainers

## Workflow Security

### Workflow Risk Level

A workflow's risk level is the **highest risk level** of any skill in the chain.

**Example**:
```
Skill A (Low) → Skill B (Medium) → Skill C (High)
= Workflow Risk Level: High
```

### Security Context

Workflows define security context:

```yaml
security_context:
  max_risk_level: "Medium"          # Maximum allowed skill risk
  requires_approval: true            # Entire workflow needs approval
  approval_at_steps:                # Individual step approvals
    - "step_3_delete_data"
```

### Approval Gates

Workflows can require approval at specific steps:
- Before execution (entire workflow)
- At individual steps (step-level gates)
- After failures (recovery actions)

## Malicious Skill Detection

### Prohibited Actions

Skills MAY NOT:
- Execute arbitrary code
- Access filesystem outside sandbox
- Make network requests to undeclared endpoints
- Extract or exfiltrate data
- Perform cryptomining or resource abuse
- Attempt privilege escalation
- Bypass security controls

### Detection Mechanisms

- Static analysis for malicious patterns
- Runtime sandboxing
- Network egress filtering
- Resource usage monitoring
- Behavioral analysis

### Reporting

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email: security@skene.ai
3. Include:
   - Skill ID and version
   - Vulnerability description
   - Reproduction steps
   - Potential impact
4. We will respond within 48 hours

### Rewards

We offer recognition (and potentially rewards) for:
- Critical vulnerability discoveries
- Security enhancement proposals
- Malicious skill detection

## Supply Chain Security

### Skill Provenance

All skills include:
- Author identification
- Source attribution
- License information
- Version history

### Dependency Management

Skills declare dependencies:
- Other skills required
- External tools/APIs
- Minimum versions

Dependencies are:
- Validated at registration
- Checked for vulnerabilities
- Pinned to specific versions

### Code Signing (Future)

Future releases will support:
- Cryptographic signing of skills
- Verification at execution time
- Trusted skill registries

## Compliance

### Regulatory Frameworks

Skills handling regulated data must comply with:
- **GDPR**: Personal data of EU residents
- **HIPAA**: Health information (US)
- **SOC 2**: Security controls
- **PCI DSS**: Payment card data

### Data Residency

Skills declare data residency requirements:
```yaml
compliance:
  regulations:
    - "GDPR"
    - "HIPAA"
  data_residency:
    - "EU"
    - "US"
```

Execution restricted to compliant regions.

## Security Updates

### Versioning

Security-related changes increment version:
- **Patch** (1.0.x): Security fix, no breaking changes
- **Minor** (1.x.0): New security requirements
- **Major** (x.0.0): Breaking security changes

### Deprecation

Skills with unresolvable security issues:
1. Marked as deprecated
2. Removed from recommendations
3. Execution disabled (with grace period)
4. Deleted after 90 days

### Security Advisories

Critical issues are disclosed via:
- GitHub Security Advisories
- Email to skill authors
- Community notifications
- CVE assignment (if applicable)

## Best Practices

### For Skill Authors

✅ **Do:**
- Declare all data access explicitly
- Follow principle of least privilege
- Validate all inputs
- Sanitize all outputs
- Handle errors gracefully
- Document security considerations

❌ **Don't:**
- Store credentials in skill code
- Access undeclared data
- Execute arbitrary user input
- Make assumptions about security context

### For Skill Users

✅ **Do:**
- Review security metadata before execution
- Approve HITL requests promptly
- Monitor execution logs
- Report suspicious behavior

❌ **Don't:**
- Override security controls
- Share approval credentials
- Execute untrusted skills
- Ignore security warnings

## Questions?

For security questions:
- 📧 Email: security@skene.ai
- 📖 Read: [CONTRIBUTING.md](CONTRIBUTING.md)
- 💬 Discuss: GitHub Discussions (non-sensitive only)

**Remember**: When in doubt, err on the side of caution. It's better to over-classify a skill's risk than under-classify it.
