# Skills Directory Testing Suite

Comprehensive pytest-based testing framework providing 80%+ code coverage across 2,622 lines of critical Python code.

## Quick Start

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest

# Run specific test suite
pytest tests/unit/test_dedupe_skills.py -v

# Run with coverage
pytest --cov=scripts --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Test Structure

```
tests/
├── conftest.py                  # Shared fixtures & mocks
├── fixtures/                    # Mock data
│   ├── mock_skills.json        # 10 sample skills
│   └── mock_registry.json      # Sample registry
├── unit/                        # Unit tests
│   ├── test_dedupe_skills.py   # Deduplication tests
│   ├── test_analyze_skills.py  # Security analysis tests
│   ├── test_generate_blueprints.py  # Blueprint generation tests
│   ├── test_skill_loom_cli.py  # Interactive CLI tests
│   └── test_loom_cli.py        # Enhanced CLI tests
├── integration/                 # Integration tests
│   ├── test_full_pipeline.py   # End-to-end workflow tests
│   └── test_cli_workflows.py   # CLI command integration
└── performance/                 # Performance tests
    └── test_large_scale.py     # Large-scale operation tests
```

## Test Categories

### Unit Tests (`tests/unit/`)
- **test_dedupe_skills.py**: Semantic deduplication engine
  - Sentence transformer mocking
  - Embedding generation
  - Duplicate detection
  - Completeness validation

- **test_analyze_skills.py**: Security risk analysis
  - Risk level calculation
  - Job function categorization
  - JTBD extraction
  - Security requirements

- **test_generate_blueprints.py**: Workflow chaining
  - I/O type extraction
  - Chainability analysis
  - Blueprint generation
  - Missing link detection

- **test_skill_loom_cli.py**: Interactive terminal interface
  - Job function browsing
  - Security audit views
  - Skill search functionality

- **test_loom_cli.py**: Enhanced CLI
  - Deduplication commands
  - Health metrics
  - Chain suggestions

### Integration Tests (`tests/integration/`)
- **test_full_pipeline.py**: Complete workflow testing
  - Analyze → Dedupe → Blueprints pipeline
  - Cross-component integration
  - Data consistency validation

- **test_cli_workflows.py**: CLI command execution
  - End-to-end command testing
  - Output validation
  - Error handling

### Performance Tests (`tests/performance/`)
- **test_large_scale.py**: Large-scale operations
  - 808 skills deduplication (< 60s embedding, < 30s dedupe)
  - Security analysis performance (< 120s)
  - Blueprint generation (< 10s)
  - Memory usage validation (< 2GB)

## Running Tests

### By Category
```bash
# Unit tests only
pytest tests/unit -v

# Integration tests
pytest tests/integration -v

# Performance tests (slow)
pytest tests/performance -v
```

### By Markers
```bash
# Fast tests only (exclude slow tests)
pytest -m "not slow"

# CLI tests only
pytest -m cli

# Integration tests
pytest -m integration

# Performance tests
pytest -m performance
```

### With Coverage
```bash
# Generate coverage report
pytest --cov=scripts --cov=. --cov-report=html --cov-report=term-missing

# Fail if coverage below 80%
pytest --cov=scripts --cov-fail-under=80
```

### Parallel Execution
```bash
# Run tests in parallel (faster)
pytest -n auto
```

## Key Features

### Automatic Mocking
All heavy dependencies are mocked automatically:
- **Sentence Transformers**: Prevents 500MB+ model loading
- **Rich Console**: Captures output without rendering
- **Pyfiglet**: Mocks ASCII art generation

### Fixtures
- `mock_skills_data`: 10 representative test skills
- `temp_skills_directory`: Temporary file structure
- `temp_output_directory`: Temporary output location
- `mock_console`: Captured console output
- `sample_skill_complete`: Complete skill with all fields
- `sample_skill_high_risk`: High-risk skill for security testing

### Test Data
- **mock_skills.json**: 10 skills covering:
  - Different job functions (engineering, marketing, finops)
  - Various risk levels (Critical, High, Medium, Low)
  - Complete and incomplete schemas
  - Chainable and standalone skills

## CI/CD Integration

Tests run automatically on:
- Every push to `main` or `develop`
- Every pull request to `main`

### GitHub Actions Workflow
```yaml
- Run unit tests with coverage
- Run integration tests
- Upload coverage to Codecov
- Fail if coverage < 80%
- Upload test results as artifacts
```

## Coverage Goals

| Component | Target | Status |
|-----------|--------|--------|
| dedupe_skills.py | 90%+ | ✅ |
| analyze_skills.py | 85%+ | ✅ |
| generate_blueprints.py | 80%+ | ✅ |
| skill-loom-cli.py | 70%+ | ✅ |
| loom | 75%+ | ✅ |
| **Overall** | **80%+** | **✅** |

## Writing New Tests

### Example Unit Test
```python
@pytest.mark.unit
def test_my_function(temp_skills_directory):
    """Test my function does X."""
    result = my_function(temp_skills_directory)
    assert result == expected_value
```

### Example Integration Test
```python
@pytest.mark.integration
@pytest.mark.slow
def test_my_workflow(temp_skills_directory):
    """Test complete workflow."""
    # Setup
    analyzer = SkillAnalyzer(...)

    # Execute
    analyzer.analyze_all_skills()

    # Verify
    assert len(analyzer.analyzed_skills) > 0
```

## Troubleshooting

### Import Errors
```bash
# Ensure scripts are in path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/scripts"
```

### Slow Tests
```bash
# Skip slow tests during development
pytest -m "not slow"
```

### Coverage Issues
```bash
# Check what's not covered
pytest --cov=scripts --cov-report=term-missing
```

### Failed Tests
```bash
# Run with verbose output
pytest -vv --tb=long
```

## Best Practices

1. **Mock heavy dependencies**: Always mock ML models, external APIs
2. **Use fixtures**: Leverage shared fixtures from conftest.py
3. **Isolate tests**: Each test should be independent
4. **Clean up**: Use temporary directories that auto-cleanup
5. **Mark appropriately**: Use @pytest.mark.unit, @pytest.mark.slow, etc.
6. **Test edge cases**: Empty inputs, invalid data, errors
7. **Verify outputs**: Check both success and failure paths

## Performance Benchmarks

With test data (10 skills):
- **Unit tests**: < 5 seconds
- **Integration tests**: < 30 seconds
- **Full suite**: < 60 seconds

With full dataset (808 skills):
- **Deduplication**: < 90 seconds
- **Security analysis**: < 120 seconds
- **Blueprint generation**: < 10 seconds

## Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Ensure tests pass: `pytest`
3. Check coverage: `pytest --cov`
4. Run in CI: Push to branch

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
