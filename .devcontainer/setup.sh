#!/bin/bash
set -e

echo "🚀 Setting up skene-cookbook development environment..."

# Install Node.js dependencies
echo "📦 Installing npm dependencies..."
npm ci

# Create Python virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
fi

# Install development dependencies
pip install pytest pytest-cov pytest-mock pytest-xdist faker black flake8 isort

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
  pre-commit install
else
  pip install pre-commit
  pre-commit install
fi

# Install security scanning tools (optional, best effort)
echo "🔒 Installing security tools..."
pip install detect-secrets 2>/dev/null || echo "⚠️  detect-secrets installation failed (optional)"

# Verify installation
echo "✅ Verifying installation..."
npm --version
node --version
python --version
pytest --version

# Run metrics verification
echo "📊 Verifying metrics consistency..."
npm run verify:metrics || echo "⚠️  Metrics verification skipped"

# Run a quick test
echo "🧪 Running quick smoke test..."
pytest tests/unit -v -m "not slow" --co -q || echo "⚠️  Test collection check skipped"

echo ""
echo "✅ Development environment ready!"
echo ""
echo "📚 Quick Start:"
echo "  • Run tests:         pytest tests/ -v"
echo "  • Fast tests only:   pytest tests/unit -v -m 'not slow'"
echo "  • Lint JavaScript:   npm run lint"
echo "  • Format code:       npm run format"
echo "  • Verify metrics:    npm run verify:metrics"
echo "  • Pre-release check: bash scripts/pre_release_check.sh"
echo ""
echo "📖 Documentation:"
echo "  • AGENTS.md          - AI agent instructions"
echo "  • CONTRIBUTING.md    - Contribution guidelines"
echo "  • docs/SKILL_CHAINS.md - 36 ready-to-use recipes"
echo ""
