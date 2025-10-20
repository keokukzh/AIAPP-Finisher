# Quick Start: Python Pro Standards

## 🚀 Immediate Usage Guide

> **Windows Users:** See [WINDOWS_QUICK_START.md](WINDOWS_QUICK_START.md) for `.bat` file alternatives!

### Run All Quality Checks (One Command)

**Linux/Mac:**
```bash
make quality
```

**Windows:**
```powershell
.\quality.bat
```

This runs:
1. ✅ black (format code)
2. ✅ isort (sort imports)
3. ✅ flake8 (lint code)
4. ✅ mypy (type check)
5. ✅ pytest (test with 70% coverage)

---

## 🔧 Individual Commands

```bash
# Format code
make format

# Lint code
make lint

# Type check
make type-check

# Test with coverage
make test-with-coverage

# Install pre-commit hooks (one-time)
make pre-commit-install

# Run pre-commit manually
make pre-commit-run
```

---

## 📝 Using New Features

### 1. Import Custom Exceptions

```python
from exceptions import AnalysisError, LLMError

try:
    result = analyze_project(path)
except FileNotFoundError as e:
    raise AnalysisError(
        "Project not found",
        project_path=path,
        cause=e
    ) from e
```

### 2. Import Type Definitions

```python
from types import AnalysisResults, Priority, Severity

def process(results: AnalysisResults) -> None:
    score: float = results['metrics']['code_quality_score']
    print(f"Quality: {score}")
```

### 3. Use Context Managers

```python
from utils import analysis_context

with analysis_context("/path/to/project", "parsing"):
    data = parse_files()
```

### 4. Use Test Fixtures

```python
from tests.fixtures import mock_analysis_results, sample_project_path

def test_something(mock_analysis_results):
    result = process_results(mock_analysis_results)
    assert result['status'] == 'success'
```

---

## 📂 New Files Reference

```
exceptions.py                      # Custom exception classes
mypy.ini                           # Type checking config
.coveragerc                        # Coverage config
.pre-commit-config.yaml            # Pre-commit hooks

types/
├── __init__.py                    # Type exports
└── analysis_types.py              # TypedDict definitions

utils/
├── __init__.py                    # Utility exports
└── context_managers.py            # Context managers

tests/fixtures/
├── __init__.py                    # Fixture exports
└── analysis_fixtures.py           # Test fixtures
```

---

## ✅ Pre-Commit Hooks

Auto-run on every commit after installation:

```bash
make pre-commit-install
```

Now every `git commit` automatically:
- Removes trailing whitespace
- Fixes end-of-file issues
- Validates YAML/JSON/TOML
- Formats code with black
- Sorts imports with isort
- Lints with flake8
- Type checks with mypy

**Skip hooks (not recommended):**
```bash
git commit --no-verify
```

---

## 📊 Check Coverage

```bash
make test-with-coverage
```

View HTML report:
```bash
open htmlcov/index.html  # Mac/Linux
start htmlcov/index.html  # Windows
```

---

## 🎯 Next Steps

1. **Phase 2:** Add type hints to all modules
2. **Phase 3:** Convert docstrings to Google style
3. **Phase 4:** Apply error handling patterns
4. **Phase 5:** Boost test coverage to 80%

See `PYTHON_PRO_IMPLEMENTATION_PHASE1.md` for full plan.

---

**All tools are ready to use!** 🎉

