# Pull Request

## Description

<!-- Provide a clear and concise description of your changes -->

## Type of Change

<!-- Check all that apply -->

- [ ] 🎯 New skill
- [ ] ✨ Feature enhancement
- [ ] 🐛 Bug fix
- [ ] 📚 Documentation update
- [ ] 🔧 Build/tooling improvement
- [ ] ♻️ Refactoring (no functional changes)
- [ ] 🧪 Test addition/improvement
- [ ] 🔒 Security fix

## Related Issues

<!-- Link related issues using #issue-number -->

Closes #
Related to #

## Changes Made

<!-- Describe the specific changes in bullet points -->

-
-
-

## Testing

### Test Coverage

<!-- Check all that apply -->

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed
- [ ] Test coverage ≥60% for new code
- [ ] All existing tests pass

### Test Plan

<!-- Describe how you tested your changes -->

```bash
# Commands used for testing
pytest tests/unit/test_my_feature.py
pytest tests/integration/
```

**Test Results:**
<!-- Paste relevant test output -->

```
```

## Security Review

<!-- Required for new skills or security-sensitive changes -->

### Risk Assessment

- [ ] **Low Risk** - Read-only operations, no sensitive data
- [ ] **Medium Risk** - Data modifications, moderate impact
- [ ] **High Risk** - System changes, significant impact
- [ ] **Critical Risk** - High-privilege operations, security implications

### Security Checklist

<!-- Check all that apply -->

- [ ] Input validation implemented
- [ ] No hardcoded credentials or secrets
- [ ] Proper error handling (no information leakage)
- [ ] Rate limiting considered (if applicable)
- [ ] Authentication/authorization reviewed
- [ ] Dependencies scanned for vulnerabilities
- [ ] Reviewed against [SECURITY_POLICY.md](../SECURITY_POLICY.md)

### Security Considerations

<!-- Describe any security implications -->

-

## Skill-Specific Information

<!-- Only required for new skills or skill modifications -->

### Skill Details

- **Skill Name:** `skill-name`
- **Domain:** `domain-name`
- **Risk Level:** Low/Medium/High/Critical

### Skill Schema

<!-- Verify schema compliance -->

- [ ] Schema follows standard format
- [ ] All parameters documented
- [ ] Examples provided
- [ ] Validation rules defined

### Eval Harness Results

<!-- Paste eval harness test results -->

```bash
# Command used
python scripts/batch_eval_skills.py --skill-name skill-name

# Results
```

```
```

## Breaking Changes

<!-- List any breaking changes and migration steps -->

- [ ] No breaking changes
- [ ] Breaking changes (describe below)

**Breaking Changes:**
-

**Migration Guide:**
-

## Code Quality

<!-- Verify code quality standards -->

- [ ] Code follows project style guidelines
- [ ] Linting passes (`black`, `flake8`, `eslint`)
- [ ] Pre-commit hooks pass
- [ ] No new warnings introduced
- [ ] Documentation updated (if needed)

## Performance Impact

<!-- Describe any performance implications -->

- [ ] No significant performance impact
- [ ] Performance improvement (describe below)
- [ ] Performance degradation (describe below, provide justification)

**Performance Notes:**
-

## Documentation

<!-- Check all that apply -->

- [ ] README.md updated (if needed)
- [ ] CHANGELOG.md updated
- [ ] Inline code comments added
- [ ] API documentation updated
- [ ] Examples/tutorials updated

## Checklist

<!-- Final verification before submission -->

- [ ] I have read [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] My code follows the project's code style
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Additional Context

<!-- Any other information reviewers should know -->

## Screenshots/Recordings

<!-- If applicable, add screenshots or recordings to demonstrate changes -->

---

**By submitting this pull request, I confirm that my contribution is made under the terms of the MIT License.**
