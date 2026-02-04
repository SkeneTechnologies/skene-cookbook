# Push to New Repository

This folder is a standalone package ready for its own GitHub repository.

## Steps

1. **Create a new repo on GitHub** (e.g. `SkeneTechnologies/skills-directory`)

2. **Add remote and push:**
   ```bash
   cd /Users/teemukinos/skene-skills-directory
   git remote add origin https://github.com/SkeneTechnologies/skills-directory.git
   git branch -M main
   git commit -m "Initial commit: Skills Directory"
   git push -u origin main
   ```

3. **Publish to npm:**
   ```bash
   npm install
   npm publish
   ```

## Package

- **Name:** @skene/skills-directory
- **CLI:** `npx skills-directory install --target all`
