# Troubleshooting Guide

Common issues and solutions for Skene Skills Directory

---

## Table of Contents

- [Installation Issues](#installation-issues)
- [Skills Not Activating](#skills-not-activating)
- [Composition Errors](#composition-errors)
- [Performance Issues](#performance-issues)
- [Security & Permissions](#security--permissions)
- [Getting Help](#getting-help)

---

## Installation Issues

### Issue: Post-install script doesn't run

**Symptoms:**
- Skills not installed automatically after `npm install`
- No "What can you build today?" message
- Directories `~/.claude/skills/` or `~/.cursor/skills/` are empty

**Causes:**
- CI/CD environment detected
- `--ignore-scripts` flag used
- `SKIP_SKILLS_INSTALL=true` environment variable set

**Solution:**
```bash
# Manual installation
npx skills-directory install --target all

# Verify installation
npx skills-directory status
```

**Prevention:**
- Avoid using `--ignore-scripts` in local development
- Check for `SKIP_SKILLS_INSTALL` in your shell profile

---

### Issue: Permission denied errors during install

**Symptoms:**
```
Error: EACCES: permission denied, mkdir '/Users/username/.claude/skills'
```

**Causes:**
- Insufficient permissions to create directories in home folder
- Parent directories have restrictive permissions

**Solution:**
```bash
# Check current permissions
ls -la ~/.claude
ls -la ~/.cursor

# Create directories with correct permissions
mkdir -p ~/.claude/skills
mkdir -p ~/.cursor/skills
chmod 755 ~/.claude/skills
chmod 755 ~/.cursor/skills

# Re-run installation
npx skills-directory install --target all
```

**Prevention:**
- Ensure your home directory is writable
- Don't run npm install with sudo (creates permission issues)

---

### Issue: Peer dependency warnings

**Symptoms:**
```
npm WARN peer dependencies: @skene/skills-directory requires zod@3.x but found 4.x
```

**Causes:**
- Other packages in your project have different version requirements
- Common with AI SDK packages

**Solution:**
These warnings are **safe to ignore** - Skills Directory has no direct zod or react dependencies.

If you want to resolve them:
```bash
# Check which packages have conflicts
npm ls zod
npm ls react

# Install with legacy peer deps flag
npm install --legacy-peer-deps
```

**Prevention:**
- Use `--legacy-peer-deps` flag when installing in complex projects

---

### Issue: Installation in Docker containers

**Symptoms:**
- Auto-installation skips in Docker
- Skills not available in containerized environments

**Causes:**
- Postinstall detects Docker environment and skips auto-installation

**Solution:**
```dockerfile
# In your Dockerfile, add manual installation step
RUN npx skills-directory install --target all

# Or set environment variable to force installation
ENV FORCE_SKILLS_INSTALL=true
RUN npm install @skene/skills-directory
```

**Prevention:**
- Always manually install skills in Docker images
- Document in your Docker setup instructions

---

## Skills Not Activating

### Issue: Claude/Cursor doesn't recognize skills

**Symptoms:**
- Prompts like "use lead_qualification skill" don't work
- Claude/Cursor says "I don't have that skill"
- Skills directory seems installed but not activated

**Causes:**
- Skills not installed to correct location
- Manifest file missing or corrupted
- IDE/CLI not reading from skills directory

**Solution:**
```bash
# 1. Verify installation status
npx skills-directory status

# 2. Check if files exist
ls -la ~/.claude/skills/
ls -la ~/.cursor/skills/

# 3. Check manifest files
cat ~/.claude/skills/skene-skills.json
cat ~/.cursor/skills/skene-skills.json

# 4. Reinstall if needed
npx skills-directory uninstall
npx skills-directory install --target all

# 5. Restart Claude/Cursor
# Skills are loaded at startup
```

**Prevention:**
- Run `npx skills-directory status` after installation
- Restart IDE/CLI after installing skills

---

### Issue: Some skills missing or incomplete

**Symptoms:**
- Status shows fewer skills than expected (should be 764+)
- Some skill files are missing

**Causes:**
- Partial installation failure
- Disk space issues during installation
- File system corruption

**Solution:**
```bash
# 1. Check installation integrity
npx skills-directory status
# Look for "Files intact: X/Y" where X < Y

# 2. Uninstall and reinstall
npx skills-directory uninstall
npx skills-directory install --target all

# 3. Verify all files present
npx skills-directory status
```

**Prevention:**
- Ensure sufficient disk space (need ~50MB for all skills)
- Run status check after installation

---

### Issue: Skills work in Claude but not Cursor (or vice versa)

**Symptoms:**
- Skills recognized in one IDE but not the other
- Status shows one installed, one not

**Causes:**
- Selective installation using `--target` flag
- One IDE reinstalled, cleared skills directory

**Solution:**
```bash
# Install to both
npx skills-directory install --target all

# Or install selectively
npx skills-directory install --target claude
npx skills-directory install --target cursor

# Verify both
npx skills-directory status
```

**Prevention:**
- Use `--target all` to install to both by default

---

## Composition Errors

### Issue: Exit state mismatch when chaining skills

**Symptoms:**
- Error: "Previous skill exited with 'qualified' but next skill expects 'approved'"
- Skill chain breaks mid-execution
- Data not passing between skills

**Causes:**
- Exit state from previous skill doesn't match input expectations of next skill
- Incorrect routing configuration

**Solution:**
```json
// Check exit states in skill definitions
// Example: lead_qualification has exit states: qualified, nurture, disqualified

{
  "skill": "lead_qualification",
  "exit_routing": {
    "qualified": "opportunity_scoring",  // ✅ Correct routing
    "nurture": "nurture_campaign",
    "disqualified": "archive_lead"
  }
}

// Make sure next skill accepts the exit state
{
  "skill": "opportunity_scoring",
  "input": {
    "leadData": "{{previous.output}}"  // ✅ Correct data passing
  }
}
```

**Prevention:**
- Review exit states in [SKILL_CHAINS.md](SKILL_CHAINS.md)
- Use recommended skill chain recipes
- Test chains with sample data before production

---

### Issue: Data format incompatibility between skills

**Symptoms:**
- Skills execute but data isn't passed correctly
- Next skill receives undefined or null values
- Type errors in skill execution

**Causes:**
- Output format of skill A doesn't match input format of skill B
- Missing data transformation

**Solution:**
```json
// Add data transformation in routing
{
  "skill": "lead_qualification",
  "exit_routing": {
    "qualified": {
      "next_skill": "opportunity_scoring",
      "transform": {
        "opportunityId": "{{output.leadId}}",
        "qualificationData": "{{output}}"
      }
    }
  }
}
```

**Prevention:**
- Check skill schemas in directory.md
- Use transformation layers when needed
- Test data flow with sample inputs

---

## Performance Issues

### Issue: Skill execution is slow

**Symptoms:**
- Skills take longer than expected to execute
- Timeouts when running skill chains
- High memory usage

**Causes:**
- Too many skills loaded in memory
- Large data sets being processed
- Network latency to external APIs

**Solution:**
```bash
# 1. Install only needed skill domains
npx skills-directory uninstall
npx skills-directory install --target all

# For future: domain-specific installation (Phase 2)
# npx skills-directory install --domain sales,revops

# 2. Optimize data processing
# - Limit result sets
# - Use pagination
# - Cache frequently accessed data

# 3. Check API rate limits
# - Some skills hit external APIs
# - Implement rate limiting
```

**Prevention:**
- Only install skills you actively use
- Monitor execution times
- Implement caching for repeated queries

---

### Issue: High memory usage

**Symptoms:**
- System running slow when using skills
- Out of memory errors
- Performance degradation over time

**Causes:**
- All 764 skills loaded in memory
- Memory leaks in skill execution
- Large data structures retained

**Solution:**
```bash
# 1. Restart IDE/CLI to clear memory
# 2. Check memory usage
top  # or htop on Linux
Activity Monitor  # on macOS

# 3. Reduce skill set (future feature)
# Install only domains you need

# 4. Update to latest version
npm update @skene/skills-directory
```

**Prevention:**
- Restart IDE periodically
- Monitor system resources
- Use domain-specific installations when available

---

## Security & Permissions

### Issue: Skill wants to access sensitive data

**Symptoms:**
- Skill requests access to files, APIs, or credentials
- Approval prompt shown
- Unsure if access should be granted

**Solution:**
1. **Review the skill's risk level** in directory.md:
   - Low risk: Safe to approve (read-only operations)
   - Medium risk: Review carefully (write operations)
   - High risk: Requires approval (destructive operations)

2. **Check what the skill needs**:
   ```bash
   # View skill details
   npx skills-directory list --skill <skill-name>
   ```

3. **Approve selectively**:
   - One-time approval: Grant for current execution only
   - Persistent approval: Add to approved list (use cautiously)

**Prevention:**
- Read skill descriptions before use
- Start with low-risk skills
- Use sandbox environments for testing

---

### Issue: Skill requires API keys or credentials

**Symptoms:**
- Error: "Missing API key for [service]"
- Authentication failures
- Skill can't access external services

**Causes:**
- Skills integrating with external services need credentials
- Environment variables not set

**Solution:**
```bash
# 1. Check which credentials are needed
# See skill description in directory.md

# 2. Set environment variables
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export SALESFORCE_API_KEY="your-key"

# Or use .env file
echo "OPENAI_API_KEY=your-key" >> .env

# 3. Verify credentials loaded
echo $OPENAI_API_KEY
```

**Prevention:**
- Document required API keys
- Use secure credential management (1Password, env files)
- Never commit API keys to git

---

### Issue: Audit trail not capturing all actions

**Symptoms:**
- Missing audit logs
- Can't trace skill execution
- Compliance concerns

**Causes:**
- Audit logging not enabled
- Log files not writable
- Incorrect log configuration

**Solution:**
```bash
# 1. Enable audit logging
# Add to your config or environment

# 2. Check log files
ls -la ~/.claude/logs/
ls -la ~/.cursor/logs/

# 3. Set proper permissions
chmod 644 ~/.claude/logs/audit.log

# 4. Review audit policy
# See SECURITY_POLICY.md for configuration
```

**Prevention:**
- Enable audit logging from day one
- Regular log reviews
- Set up log rotation

---

## Getting Help

### Before Asking for Help

1. **Check this troubleshooting guide** — Most common issues covered
2. **Run diagnostics**:
   ```bash
   npx skills-directory status
   npx skills-directory validate  # (Phase 2 feature)
   ```
3. **Check existing issues**: [GitHub Issues](https://github.com/SkeneTechnologies/skene-cookbook/issues)

### How to Report an Issue

Include these details:

```
**Environment:**
- OS: [macOS 14.1, Ubuntu 22.04, Windows 11]
- Node version: [18.x, 20.x]
- Package version: [@skene/skills-directory@0.1.0]
- IDE: [Claude Code, Cursor]

**Issue:**
[Clear description of the problem]

**Steps to Reproduce:**
1. [First step]
2. [Second step]
3. [What happened]

**Expected Behavior:**
[What should have happened]

**Actual Behavior:**
[What actually happened]

**Logs/Screenshots:**
[Paste relevant logs or attach screenshots]

**Installation Status:**
[Output of `npx skills-directory status`]
```

### Where to Get Help

- **GitHub Issues**: [Report bugs](https://github.com/SkeneTechnologies/skene-cookbook/issues/new)
- **GitHub Discussions**: [Ask questions](https://github.com/SkeneTechnologies/skene-cookbook/discussions)
- **Documentation**: [Browse docs](../README.md)

---

## Quick Reference

### Diagnostic Commands

```bash
# Check installation status
npx skills-directory status

# Reinstall skills
npx skills-directory uninstall
npx skills-directory install --target all

# List available skills
npx skills-directory list

# Get help
npx skills-directory --help
```

### Common File Locations

```
~/.claude/skills/          # Claude skills directory
~/.cursor/skills/          # Cursor skills directory
~/.claude/skills/skene-skills.json    # Claude manifest
~/.cursor/skills/skene-skills.json    # Cursor manifest
```

### Log Files (if enabled)

```
~/.claude/logs/audit.log   # Audit trail
~/.cursor/logs/audit.log   # Audit trail
```

---

**Still stuck?** [Open an issue](https://github.com/SkeneTechnologies/skene-cookbook/issues/new) and we'll help!
