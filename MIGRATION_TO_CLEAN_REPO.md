# Migration to Clean Repository - Security Remediation

## 🚨 Issue
GitHub access token found in git history. Even though removed in later commits, it remains accessible in git history.

## ✅ Solution: Fresh Repository Migration

### Step 1: Revoke Compromised Token (URGENT)

1. **Go to GitHub Settings**:
   - https://github.com/settings/tokens
   - Find the exposed token
   - Click "Delete" to revoke immediately

2. **Generate new token** (if needed):
   - Settings → Developer settings → Personal access tokens
   - Generate new token with minimum required scopes
   - Store securely (password manager, not in code)

### Step 2: Prepare Clean Export

```bash
# Create clean export directory
mkdir -p ~/skills-directory-clean
cd ~/skills-directory-clean

# Copy only the files (not .git directory)
rsync -av --exclude='.git' \
          --exclude='.pytest_cache' \
          --exclude='__pycache__' \
          --exclude='*.pyc' \
          --exclude='htmlcov' \
          --exclude='.coverage' \
          /Users/teemukinos/skene-skills-directory/ .

# Verify no .git directory
ls -la | grep .git
# (should show nothing)
```

### Step 3: Initialize Fresh Git Repository

```bash
cd ~/skills-directory-clean

# Initialize new git repo (clean history)
git init

# Add .gitignore first (critical!)
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Secrets (CRITICAL)
.env
.env.local
.env.*.local
*.pem
*.key
secrets.json
credentials.json
config.local.json

# OS
.DS_Store
Thumbs.db

# Reports (generated)
reports/*.json
reports/*.md
!reports/.gitkeep

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
EOF

# Create initial commit with clean history
git add .gitignore
git commit -m "Initial commit: Add .gitignore"

# Add all project files
git add .
git commit -m "Initial commit: Skills Directory with 808+ AI skills

- Complete skills library (808+ skills)
- Semantic deduplication engine
- Security risk analysis
- Workflow blueprint generation
- Interactive CLI tools
- Comprehensive testing (135 tests, 80%+ coverage)
- CI/CD pipeline
- E2E testing framework
- Documentation

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

### Step 4: Create New GitHub Repository

```bash
# On GitHub.com:
# 1. Go to https://github.com/new
# 2. Repository name: skills-directory
# 3. Description: "800+ AI Skills for Claude and Cursor - Production Ready"
# 4. Public/Private: Choose Public (after verification)
# 5. DO NOT initialize with README (we have one)
# 6. Click "Create repository"

# Link local repo to new GitHub repo
git remote add origin https://github.com/YOUR_USERNAME/skills-directory.git

# Push to new clean repository
git push -u origin main
```

### Step 5: Verify Clean History

```bash
# Check git history (should only show clean commits)
git log --oneline

# Verify no secrets in history
trufflehog filesystem . --only-verified

# Expected: No findings

# Check current files
rg -i "github|token|ghp_" --type py --type json --type yaml
# Should not find any tokens
```

### Step 6: Archive Old Repository

```bash
# Go to old repository settings on GitHub
# Settings → Danger Zone → Archive this repository
# Add note: "Archived due to security - migrated to [new repo]"

# Or delete entirely (after backup)
# Settings → Danger Zone → Delete this repository
```

### Step 7: Update All References

**Update documentation:**
- [ ] README.md - Update GitHub URLs
- [ ] CONTRIBUTING.md - Update repository URL
- [ ] Documentation links
- [ ] CI/CD workflows (if they reference repo)
- [ ] Package metadata

**Update workflows:**
```yaml
# .github/workflows/lint-and-build.yml
# Verify all repository references are correct
```

## 🔒 Security Best Practices Going Forward

### 1. Never Commit Secrets
```bash
# Add to .gitignore BEFORE any commits
.env
.env.*
*.pem
*.key
secrets.*
credentials.*
config.local.*
```

### 2. Use Environment Variables
```bash
# Instead of hardcoding:
# token = "ghp_xxxxx"  ❌

# Use environment variables:
# token = os.getenv("GITHUB_TOKEN")  ✅

# Or use .env with python-dotenv
pip install python-dotenv

# In code:
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("GITHUB_TOKEN")
```

### 3. Use Pre-Commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
      - id: check-yaml
      - id: check-json
      - id: detect-private-key

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
EOF

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

### 4. Use GitHub Secrets for CI/CD
```yaml
# In GitHub Actions workflows, use secrets:
- name: Run tests
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: pytest
```

### 5. Regular Security Audits
```bash
# Add to pre-release checklist
trufflehog filesystem . --only-verified
pip-audit
bandit -r scripts/ -ll
```

## 📋 Pre-Release Security Checklist

Before making repository public:

### Critical (Blocking)
- [ ] Token from old repo has been revoked
- [ ] New repository has clean git history
- [ ] `git log --all` shows no token commits
- [ ] `trufflehog` scan shows no secrets
- [ ] `.gitignore` includes all secret patterns
- [ ] No .env files in repository
- [ ] No credentials in code

### Important (Recommended)
- [ ] Pre-commit hooks installed
- [ ] Documentation updated with new URLs
- [ ] Old repository archived/deleted
- [ ] CI/CD uses GitHub secrets
- [ ] Security policy documented
- [ ] SECURITY.md file created

### Optional (Best Practice)
- [ ] Branch protection rules enabled
- [ ] Required reviews for PRs
- [ ] Status checks required
- [ ] Signed commits enabled
- [ ] Dependabot enabled

## 🚀 Migration Timeline

**Day 1 (Today)**:
- [x] ✅ Revoke exposed token (IMMEDIATE)
- [ ] Create clean export
- [ ] Initialize fresh repository
- [ ] Verify no secrets

**Day 2**:
- [ ] Create new GitHub repo
- [ ] Push clean code
- [ ] Setup pre-commit hooks
- [ ] Update documentation

**Day 3**:
- [ ] Run security scans
- [ ] Update all references
- [ ] Archive old repository
- [ ] Verify everything works

**Day 4**:
- [ ] Final security review
- [ ] Make repository public
- [ ] Announce release

## 📚 Additional Resources

### Tools
- **trufflehog**: https://github.com/trufflesecurity/trufflehog
- **git-secrets**: https://github.com/awslabs/git-secrets
- **detect-secrets**: https://github.com/Yelp/detect-secrets
- **BFG Repo Cleaner**: https://rtyley.github.io/bfg-repo-cleaner/

### Guides
- GitHub: Removing sensitive data
  https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

- OWASP: Secrets Management
  https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

## ⚠️ If Token Was Already Exposed

If the token was already exposed and repository was public:

1. **Assume compromise** - Token may have been scraped
2. **Revoke immediately** - Don't wait
3. **Check GitHub audit logs** - Look for suspicious activity
4. **Rotate all secrets** - Not just the exposed token
5. **Review repository access** - Check who accessed the repo
6. **Monitor for abuse** - Watch for API usage spikes

## ✅ Verification Commands

```bash
# After migration, verify:

# 1. No secrets in history
trufflehog filesystem . --only-verified
echo "Expected: No findings"

# 2. No old commits
git log --all --oneline | wc -l
echo "Expected: 1-2 commits only"

# 3. No .git from old repo
du -sh .git
echo "Expected: Small size (< 10MB)"

# 4. All tests pass
pytest tests/ -v
echo "Expected: All pass"

# 5. E2E validation
./scripts/run_e2e_tests.sh
echo "Expected: READY FOR RELEASE"
```

## 🎯 Success Criteria

Migration is complete when:
- ✅ Old token revoked
- ✅ New repo has clean history
- ✅ No secrets in git history
- ✅ All tests pass
- ✅ Documentation updated
- ✅ Old repo archived
- ✅ Security scans clean

---

**Status**: Migration plan ready
**Priority**: URGENT - Do this before public release
**Time Required**: 2-3 hours
