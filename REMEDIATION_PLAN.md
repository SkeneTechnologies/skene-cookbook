# Skills Security Remediation Plan

**Goal:** Reduce security risk across the skill library through systematic remediation
**Timeline:** Phased approach over 12 weeks
**Current State:** 521 skills (64.5%) require remediation (Critical: 470, High: 51)

## Executive Summary

### The Problem
- **470 Critical Risk Skills (58.2%)** - Currently require human approval for every execution
- **51 High Risk Skills (6.3%)** - Require sandboxing and audit logging
- **Impact:** Operational friction, delayed executions, compliance burden

### The Opportunity
By remediating these skills, we can:
- ✅ Reduce human-in-loop bottlenecks by 60-80%
- ✅ Lower operational risk exposure
- ✅ Improve skill execution speed
- ✅ Reduce compliance audit surface
- ✅ Enable more automation

### Success Metrics
- **Primary:** Reduce Critical skills from 470 to <150 (68% reduction)
- **Secondary:** Reduce High skills from 51 to <30 (41% reduction)
- **Tertiary:** Zero skills with unmitigated "payment", "credential", or "delete" operations

## Remediation Strategy

### What "Fixing" Means

Skills can be remediated through several approaches:

#### 1. **Risk Reduction** (Preferred)
Modify the skill to eliminate risky operations:
- Replace destructive operations with safer alternatives
- Remove credential handling, use delegated auth instead
- Scope down data access (read-only vs read-write)
- Add input validation and sanitization
- Implement principle of least privilege

#### 2. **Risk Mitigation** (When reduction isn't possible)
Add controls to manage risk:
- Implement granular approval workflows (per-action vs per-skill)
- Add transaction rollback capabilities
- Implement dry-run/preview modes
- Add detailed logging and monitoring
- Create safety guardrails (rate limits, quotas)

#### 3. **Risk Acceptance** (Last resort)
Document and accept remaining risk:
- Clear documentation of residual risk
- Defined approval process
- Monitoring and alerting
- Regular security reviews

#### 4. **Deprecation** (If unfixable)
Retire skills that can't be secured:
- Document replacement alternatives
- Migration path for existing users
- Sunset timeline

### Risk Reduction Matrix

| Current Risk | Target Risk | Primary Strategy | Examples |
|--------------|-------------|------------------|----------|
| Critical → Low | Remove risky operations | Replace `delete` with `archive`, Remove direct payment processing |
| Critical → Medium | Scope down permissions | Read-only data access, Preview-only mode |
| Critical → High | Add guardrails | Rate limits, Rollback capability, Dry-run mode |
| High → Medium | Improve validation | Input sanitization, Schema validation |
| High → Low | Remove external calls | Cache results, Use internal APIs only |

## Prioritization Framework

### Phase 1: Quick Wins (Weeks 1-2)
**Target:** 100 skills
**Criteria:** Skills with false positives or easy fixes

#### 1.1 False Positive Analysis (50 skills estimated)
Skills flagged as Critical due to keyword matches but actually low risk:

```bash
# Example: Skills with "system" keyword but no actual system access
# Action: Manual review + metadata correction
```

**Common False Positives:**
- "system" in documentation but not in actual operations
- "delete" in skill name but operates on cached data
- "payment" mentioned but read-only revenue reporting

**Action Items:**
- Manual review of risk factors
- Correct metadata.yaml
- Re-categorize to appropriate risk level
- Document rationale

#### 1.2 Easy Scoping Fixes (50 skills estimated)
Skills that can be made read-only or scoped down:

**Examples:**
- Analytics skills: Make read-only
- Reporting skills: Remove write access
- Dashboard skills: View-only mode

**Action Items:**
- Remove write permissions from tool definitions
- Update skill.json to reflect read-only nature
- Re-analyze security profile
- Test functionality

### Phase 2: Medium Effort (Weeks 3-6)
**Target:** 200 skills
**Criteria:** Skills needing architectural changes

#### 2.1 Credential Elimination (40 skills)
Skills handling credentials/secrets/API keys

**Strategy:**
- Replace with OAuth delegation
- Use managed identity providers
- Implement token exchange patterns
- Remove credential storage

**Example Remediation:**
```yaml
# Before: Direct API key handling
tools:
  - name: external_api.call
    config:
      api_key: "${USER_PROVIDED_KEY}"  # ❌ Critical risk

# After: Delegated authentication
tools:
  - name: external_api.call
    config:
      auth_method: "oauth"  # ✅ Medium risk
      scopes: ["read:data"]
```

#### 2.2 Payment Operation Hardening (30 skills)
Skills with payment/financial operations

**Strategy:**
- Implement two-phase commit (authorize then capture)
- Add preview/dry-run mode
- Require per-transaction approval (not per-skill)
- Add rollback capabilities
- Implement strict amount limits

**Example Remediation:**
```yaml
# Add safety controls
security_controls:
  preview_mode: true              # Show what will happen
  transaction_approval: true      # Approve each transaction
  amount_limit: 1000              # Max transaction size
  rollback_window: 3600           # 1 hour rollback period
```

#### 2.3 Data Access Scoping (130 skills)
Skills with broad data access

**Strategy:**
- Implement field-level access control
- Add data filtering (tenant isolation)
- Scope to specific data types
- Implement time-based access windows

**Example Remediation:**
```yaml
# Before: Broad access
data_access_scope: ["pii", "financial", "confidential"]  # ❌

# After: Scoped access
data_access_scope: ["pii"]  # ✅
data_filters:
  fields: ["email", "name"]  # Not SSN, credit cards
  tenant_isolated: true
  time_window: "90d"  # Only recent data
```

### Phase 3: Complex Remediation (Weeks 7-10)
**Target:** 150 skills
**Criteria:** Skills requiring significant rearchitecture

#### 3.1 Destructive Operations (50 skills)
Skills with delete/drop/truncate operations

**Strategy:**
- Replace with soft deletes (archive/mark inactive)
- Implement multi-party approval
- Add mandatory backup before delete
- Require explicit confirmation with context
- Implement undelete capability (time-limited)

**Example Remediation:**
```yaml
# Before: Direct delete
action: "delete_record"  # ❌ Critical risk

# After: Soft delete with safeguards
action: "archive_record"  # ✅ High risk
safeguards:
  soft_delete: true
  retention_period: "30d"
  undelete_capable: true
  backup_before_delete: true
  multi_party_approval: true
  explicit_confirmation:
    required: true
    show_impact: true  # Show what will be affected
```

#### 3.2 System Command Execution (30 skills)
Skills executing system commands or code

**Strategy:**
- Sandbox all executions (containers, VMs)
- Implement command whitelisting
- Add resource limits (CPU, memory, time)
- Disable network access unless required
- Run as non-privileged user

**Example Remediation:**
```yaml
execution_environment:
  type: "sandboxed_container"
  resource_limits:
    cpu: "1core"
    memory: "512MB"
    timeout: "30s"
  security:
    network_access: false
    filesystem: "read_only"
    user: "non_root"
    allowed_commands: ["npm", "node", "python3"]  # Whitelist
```

#### 3.3 External API Integration (70 skills)
Skills calling external/third-party APIs

**Strategy:**
- Implement API gateway pattern
- Add rate limiting and throttling
- Implement circuit breakers
- Add request/response validation
- Cache responses where possible

**Example Remediation:**
```yaml
external_api:
  gateway: "internal_proxy"  # Route through gateway
  rate_limit:
    requests_per_minute: 60
    burst: 10
  circuit_breaker:
    failure_threshold: 5
    timeout: 30
    retry_after: 60
  validation:
    request_schema: true
    response_schema: true
  caching:
    enabled: true
    ttl: 300  # 5 minutes
```

### Phase 4: Risk Acceptance (Weeks 11-12)
**Target:** 71 skills
**Criteria:** Skills that cannot be further reduced

#### 4.1 Document & Accept (50 skills)
Skills with inherent risk that serves business purpose

**Requirements:**
- Comprehensive risk documentation
- Defined approval workflow
- Monitoring and alerting
- Regular security reviews (quarterly)
- Incident response plan

**Documentation Template:**
```yaml
risk_acceptance:
  accepted_date: "2026-02-15"
  accepted_by: "CISO"
  review_frequency: "quarterly"

  residual_risks:
    - risk: "PII data access required for customer support"
      business_justification: "Core product feature"
      mitigations:
        - "Audit logging enabled"
        - "Access limited to CS team"
        - "Session recording"
        - "Regular access reviews"

  monitoring:
    alerts:
      - "Unusual access patterns"
      - "Bulk data exports"
      - "Access outside business hours"

  incident_response:
    contact: "security@company.com"
    playbook_url: "https://wiki/ir-pii-exposure"
```

#### 4.2 Deprecation Path (21 skills)
Skills that should be retired

**Criteria:**
- Unfixable security issues
- Duplicate functionality exists
- Low usage
- Architectural limitations

**Process:**
1. Mark as deprecated in metadata
2. Document replacement/alternative
3. Notify users (90-day notice)
4. Disable new usage
5. Monitor existing usage
6. Final sunset

## Implementation Tools

### 1. Remediation Tracker

Track progress on skill fixes with priority scoring.

### 2. Remediation Assistant

Automated suggestions for common fixes.

### 3. Security Diff Tool

Compare before/after security profiles.

### 4. Validation Suite

Test that remediation doesn't break functionality.

## Organizational Approach

### Team Structure

**Security Champions (1 per domain)**
- Review skills in their domain
- Propose remediations
- Implement fixes
- Test changes

**Security Architects (2-3)**
- Review complex remediations
- Approve risk acceptance
- Define patterns and standards
- Final approval

**Automation Engineer (1)**
- Build tooling
- Automate testing
- CI/CD integration

### Weekly Cadence

**Monday:** Planning & prioritization
**Tuesday-Thursday:** Implementation & testing
**Friday:** Review & approval

### Review Process

1. **Self-review:** Author reviews changes
2. **Peer review:** Domain champion reviews
3. **Security review:** Security architect approves (for High/Critical)
4. **Testing:** Validation suite passes
5. **Deployment:** Staged rollout

## Success Metrics & Reporting

### Weekly Dashboard

```
┌─────────────────────────────────────────────────┐
│  Skills Remediation Dashboard - Week X         │
├─────────────────────────────────────────────────┤
│  Critical Skills:  470 → 423 (↓47, -10%)      │
│  High Skills:       51 →  48 (↓3,  -6%)       │
│  Remediated:        50                          │
│  In Progress:       25                          │
│  Blocked:            5                          │
└─────────────────────────────────────────────────┘

Top Blockers:
1. Waiting on OAuth implementation (15 skills)
2. External API gateway not ready (8 skills)
3. Need business approval (2 skills)

This Week's Focus:
- Complete Phase 1 false positives (25 remaining)
- Start credential elimination (40 skills queued)
```

### Monthly Report

- Skills remediated by risk level
- Time to remediation by category
- Top blockers and resolutions
- Risk reduction percentage
- Cost savings (reduced manual approvals)

## Budget & Resources

### Estimated Effort

| Phase | Skills | Avg Hours/Skill | Total Hours | FTE @ 40h/wk |
|-------|--------|-----------------|-------------|--------------|
| Phase 1 | 100 | 2h | 200h | 1.25 FTE for 2 weeks |
| Phase 2 | 200 | 4h | 800h | 5 FTE for 4 weeks |
| Phase 3 | 150 | 8h | 1,200h | 7.5 FTE for 4 weeks |
| Phase 4 | 71 | 3h | 213h | 1.3 FTE for 2 weeks |
| **Total** | **521** | **4.6h avg** | **2,413h** | **15 FTE-weeks** |

### Team Composition

- 3 Senior Engineers (leads for 3 domains)
- 4 Engineers (implementation)
- 1 Security Engineer (review & guidance)
- 1 QA Engineer (testing & validation)

**Total:** ~9 people for 12 weeks (but not all full-time)

## Risk Management

### Risks to Remediation Plan

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking changes to skills | High | Comprehensive test suite, staged rollout |
| Scope creep | Medium | Strict prioritization, phase gates |
| Resource constraints | High | External contractors, phase extensions |
| Dependency blockers | Medium | Early identification, parallel work streams |
| Business pushback on changes | Medium | Clear communication, ROI metrics |

## Communication Plan

### Stakeholders

**Engineering Teams:** Monthly updates, skill change notifications
**Security Team:** Weekly sync, escalation path
**Compliance:** Phase completion reports
**Executive:** Monthly dashboard, milestone reports

### Templates

- Skill Change Notification (for users)
- Deprecation Notice (90-day warning)
- Risk Acceptance Form
- Remediation Completion Certificate

## Appendix: Quick Reference

### Remediation Decision Tree

```
Is the risky operation necessary?
├─ NO → Remove it (↓↓ Risk)
└─ YES
   ├─ Can we make it read-only?
   │  ├─ YES → Remove write access (↓ Risk)
   │  └─ NO → Continue
   ├─ Can we scope down permissions?
   │  ├─ YES → Apply least privilege (↓ Risk)
   │  └─ NO → Continue
   ├─ Can we add safeguards?
   │  ├─ YES → Add controls (↓ Risk)
   │  └─ NO → Continue
   └─ Must accept risk
      ├─ Business critical? → Document & accept
      └─ Not critical? → Deprecate
```

### Common Patterns

**Pattern 1: OAuth Migration**
Before: Direct API key → After: OAuth delegation
Risk: Critical → Medium

**Pattern 2: Soft Delete**
Before: Hard delete → After: Archive with undelete
Risk: Critical → High

**Pattern 3: Read-Only Projection**
Before: Full data access → After: Filtered view
Risk: High → Medium

**Pattern 4: Preview Mode**
Before: Direct execution → After: Preview + approve
Risk: Critical → High

---

**Next Steps:**
1. Review and approve this plan
2. Run `python3 scripts/generate_remediation_tracker.py` to create task list
3. Assign domain champions
4. Begin Phase 1 next Monday
