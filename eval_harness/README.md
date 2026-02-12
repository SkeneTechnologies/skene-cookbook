# Evaluation Harness for skene-cookbook

Production-ready evaluation infrastructure for AI skills with runtime validation, distributed tracing, metrics collection, and intelligent decision-making.

## Features

### 🔍 Runtime Validation
- **Input/Output Schema Validation**: Validates runtime data against JSON Schema contracts
- **Chain Compatibility**: Validates that skills can be chained together
- **Detailed Error Messages**: JSONPath-based error reporting

### 📊 Distributed Tracing
- **OpenTelemetry Integration**: Industry-standard distributed tracing
- **Hierarchical Spans**: Workflow → Steps → Skills
- **Console & OTLP Export**: Dev-friendly console output, production OTLP export

### 📈 Metrics Collection
- **Success Rate**: % executions without errors
- **Latency**: avg, p50, p95, p99, max, min
- **Validation Pass Rate**: % passing I/O schema checks
- **Auto-Act Rate**: % that auto-executed vs flagged
- **Error Distribution**: Track error types

### 🎯 Decision Engine
- **Auto-Act**: Execute automatically (high confidence, acceptable risk)
- **Flag for Review**: Execute but notify human (medium confidence)
- **Require Approval**: Block until human approves (low confidence or high risk)
- **Block**: Reject execution (validation failed)

### 📝 Reporting
- **Markdown Reports**: Human-readable evaluation reports
- **JSON Exports**: Machine-readable for programmatic analysis
- **HTML Dashboards**: Interactive visualizations (coming soon)

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements-test.txt
```

### Basic Usage

```python
from eval_harness.instrumented_executor import InstrumentedSkillExecutor

# Initialize executor
executor = InstrumentedSkillExecutor()

# Execute skill with full instrumentation
result = executor.execute_skill(
    skill_id='elg_mdf_tracker',
    skill_version='1.0.0',
    inputs={'partnerId': 'test-123', 'action': 'check_budget'},
    skill_logic=my_skill_function
)

# Check results
print(f"Success: {result.success}")
print(f"Decision: {result.decision.type.value}")
print(f"Duration: {result.duration_ms:.2f}ms")
```

### CLI Usage

```bash
# Evaluate single skill
python scripts/run_eval_harness.py eval-skill --skill-id elg_mdf_tracker

# Generate reports
python scripts/run_eval_harness.py eval-skill --skill-id elg_mdf_tracker \\
  --report-dir reports/evals/

# Evaluate workflow (coming soon)
python scripts/run_eval_harness.py eval-workflow --workflow-id test_workflow

# Generate dashboard (coming soon)
python scripts/run_eval_harness.py dashboard --session-dir reports/evals/sessions/

# A/B test (coming soon)
python scripts/run_eval_harness.py ab-test --skill-id elg_mdf_tracker \\
  --version-a 1.0.0 --version-b 1.1.0
```

## Architecture

### Core Components

```
eval_harness/
├── core/
│   ├── validator.py           # Runtime JSON Schema validation
│   ├── tracer.py              # OpenTelemetry tracing
│   ├── metrics_collector.py  # Metrics aggregation
│   └── eval_session.py        # Session management
├── decision/
│   ├── decision_engine.py     # Auto-act vs flag logic
│   ├── confidence_scorer.py   # Confidence calculation
│   └── risk_evaluator.py      # Risk assessment
├── reporters/
│   ├── markdown_reporter.py   # Markdown reports
│   └── json_reporter.py       # JSON exports
└── instrumented_executor.py   # Main executor
```

### Decision Flow

```
1. Validate Inputs
   ↓
2. Get Risk Level (from metadata.yaml)
   ↓
3. Calculate Confidence (input quality + history + context)
   ↓
4. Make Decision (auto-act vs flag vs block)
   ↓
5. Execute with Tracing (if not blocked)
   ↓
6. Validate Outputs
   ↓
7. Record Metrics
```

### Decision Rules

| Condition | Decision | Reasoning |
|-----------|----------|-----------|
| Validation failed | **BLOCK** | Cannot execute with invalid data |
| Critical risk | **REQUIRE_APPROVAL** | Always needs human oversight |
| Confidence < 0.30 | **BLOCK** | Too risky to execute |
| High risk + confidence < 0.75 | **FLAG_FOR_REVIEW** | Needs monitoring |
| Confidence ≥ 0.85 | **AUTO_ACT** | High confidence, safe to auto-execute |
| Confidence ≥ 0.50 | **FLAG_FOR_REVIEW** | Medium confidence, execute but notify |
| Confidence < 0.50 | **REQUIRE_APPROVAL** | Low confidence, needs approval |

## Examples

### Example 1: Basic Validation

```python
from eval_harness.core import SkillValidator

validator = SkillValidator()

# Validate input
result = validator.validate_input('elg_mdf_tracker', {
    'partnerId': 'test-123',
    'action': 'check_budget'
})

print(result.valid)  # True
print(result.errors)  # []
```

### Example 2: Chain Compatibility

```python
# Check if two skills can be chained
result = validator.validate_chain_compatibility(
    producer_skill_id='elg_partner_tier_manager',
    consumer_skill_id='elg_partner_influenced_revenue',
    field_mappings={
        'output.partnerId': 'input.partnerId'
    }
)

print(result.valid)
print(result.warnings)
```

### Example 3: Full Instrumentation

```python
from eval_harness.instrumented_executor import InstrumentedSkillExecutor

executor = InstrumentedSkillExecutor()

# Define skill logic
def mdf_tracker_logic(inputs):
    # Actual skill implementation
    return {
        'available_budget': 10000.0,
        'allocated': 5000.0,
        'spent': 2000.0
    }

# Execute with instrumentation
result = executor.execute_skill(
    skill_id='elg_mdf_tracker',
    skill_version='1.0.0',
    inputs={'partnerId': 'test-123', 'action': 'check_budget'},
    skill_logic=mdf_tracker_logic,
    context={'user_id': 'user-456'},
    runtime_risk_factors={'financial_operation': True}
)

# Access results
print(f"Success: {result.success}")
print(f"Decision: {result.decision.type.value}")
print(f"Confidence: {result.decision.confidence:.2f}")
print(f"Risk Level: {result.decision.risk_level}")
print(f"Duration: {result.duration_ms:.2f}ms")
print(f"Trace ID: {result.trace_id}")

# Check validation
print(f"Input Valid: {result.input_validation.valid}")
print(f"Output Valid: {result.output_validation.valid}")
```

### Example 4: Session-Based Evaluation

```python
from eval_harness.core import EvalSession
from eval_harness.core.eval_session import EvalConfig
from pathlib import Path

# Create config
config = EvalConfig(
    session_id='eval_20260211',
    session_name='MDF Tracker Evaluation',
    skills_to_eval=['elg_mdf_tracker'],
    test_data_paths={},
    output_dir=Path('reports/evals/sessions')
)

# Create session
session = EvalSession(config)
session.start()

# Run evaluations
for test_case in test_cases:
    result = executor.execute_skill(...)
    session.validate_and_record(
        skill_id='elg_mdf_tracker',
        input_data=test_case,
        output_data=result.outputs
    )

# End session and save results
session_result = session.end()
session.save_results()
```

## Integration with Existing Infrastructure

### Using Existing Schemas

The eval harness automatically loads schemas from:
- `skills-library/[domain]/[skill]/skill.json` (inputSchema, outputSchema)
- `skills-library/[domain]/[skill]/metadata.yaml` (security.risk_level)

No changes needed to existing skill definitions!

### Using with Pytest

```python
# tests/test_my_skill_eval.py
import pytest
from eval_harness.instrumented_executor import InstrumentedSkillExecutor

@pytest.fixture
def executor():
    return InstrumentedSkillExecutor()

def test_mdf_tracker_eval(executor):
    result = executor.execute_skill(
        skill_id='elg_mdf_tracker',
        skill_version='1.0.0',
        inputs={'partnerId': 'test-123', 'action': 'check_budget'},
        skill_logic=mdf_tracker_logic
    )

    assert result.success is True
    assert result.decision.type.value == 'auto_act'
    assert result.duration_ms < 500
```

## Reports

### Markdown Report Example

```markdown
# Evaluation Report: elg_mdf_tracker

**Session**: eval_20260211_153022
**Success Rate**: 96.0% (48/50)
**Avg Latency**: 234ms (p95: 450ms)
**Validation Pass**: 100%
**Auto-Act Rate**: 82%

## Decision Breakdown
| Decision Type | Count | % |
|---------------|-------|---|
| Auto-Act | 41 | 82% |
| Flag for Review | 7 | 14% |
| Blocked | 2 | 4% |

## Recommendations
✅ Excellent performance - skill is production-ready
```

### JSON Report Example

```json
{
  "skill_id": "elg_mdf_tracker",
  "summary": {
    "success_rate": 0.96,
    "avg_duration_ms": 234.5,
    "validation_pass_rate": 1.0,
    "auto_act_rate": 0.82
  },
  "decisions": {
    "auto_act": 41,
    "flag_for_review": 7,
    "blocked": 2
  }
}
```

## Testing

```bash
# Run eval harness tests
pytest tests/test_eval_harness_*.py -v

# Run with coverage
pytest tests/test_eval_harness_*.py --cov=eval_harness --cov-report=html
```

## Roadmap

### Phase 1: Core Infrastructure ✅ (Complete)
- [x] Runtime I/O validation
- [x] Distributed tracing
- [x] Metrics collection
- [x] Eval session management

### Phase 2: Decision Engine ✅ (Complete)
- [x] Auto-act vs flag logic
- [x] Confidence scoring
- [x] Risk evaluation
- [x] Execution history tracking

### Phase 3: Instrumentation ✅ (Complete)
- [x] Instrumented executor
- [x] Workflow executor
- [x] Chain validation

### Phase 4: Reporting ✅ (Complete)
- [x] Markdown reports
- [x] JSON exports
- [ ] HTML dashboards (TODO)

### Phase 5: CLI & Documentation ✅ (Complete)
- [x] CLI entry point
- [x] Documentation
- [ ] Integration tests (TODO)

### Phase 6: A/B Testing (TODO)
- [ ] A/B test session management
- [ ] Statistical significance testing
- [ ] A/B test reports

### Phase 7: Production Rollout (TODO)
- [ ] Deploy to staging
- [ ] Run evals on 50+ skills
- [ ] Production dashboards

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

See [LICENSE](../LICENSE) for details.
