# Windows Quick Start: Python Pro Standards

## 🚀 For Windows Users

Since `make` is not available on Windows by default, use these `.bat` files instead:

---

## ✅ Run All Quality Checks (One Command)

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

```powershell
# Format code
.\format.bat

# Lint code
.\lint.bat

# Type check
.\type-check.bat

# Test with coverage
.\test-with-coverage.bat

# Install pre-commit hooks (one-time)
.\pre-commit-install.bat

# Run pre-commit manually
.\pre-commit-run.bat
```

---

## 📦 First-Time Setup

**1. Install dependencies:**
```powershell
pip install -r requirements.txt
```

**2. Install pre-commit (if not included):**
```powershell
pip install pre-commit
```

**3. Install pre-commit hooks:**
```powershell
.\pre-commit-install.bat
```

Now hooks run automatically on every `git commit`!

---

## 🎯 Typical Workflow

**Before starting work:**
```powershell
git checkout -b feature/my-feature
```

**While working:**
```powershell
# After making changes, format your code
.\format.bat

# Check for issues
.\lint.bat
.\type-check.bat
```

**Before committing:**
```powershell
# Run all checks
.\quality.bat

# If all pass, commit
git add .
git commit -m "Add feature"  # Pre-commit runs automatically
```

---

## 📊 View Coverage Report

After running `.\test-with-coverage.bat`:

```powershell
# Open HTML coverage report
start htmlcov\index.html
```

---

## 🔍 Troubleshooting

### "command not found" errors

If you get errors about missing commands:

```powershell
# Verify Python packages are installed
pip list | findstr "mypy black isort flake8 pytest"

# If missing, install them
pip install -r requirements.txt
```

### Pre-commit issues

```powershell
# Reinstall pre-commit
pip install --upgrade pre-commit

# Reinstall hooks
.\pre-commit-install.bat

# Clear pre-commit cache
pre-commit clean
```

### Virtual Environment

If you're using a virtual environment:

```powershell
# Activate it first
.\.venv\Scripts\Activate.ps1

# Then run commands
.\quality.bat
```

---

## 💡 Windows-Specific Tips

### PowerShell Execution Policy

If you can't run .bat files in PowerShell:

```powershell
# Check current policy
Get-ExecutionPolicy

# If needed, allow scripts (run as Administrator)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Path Issues

If commands fail with "not found":

```powershell
# Check if Python Scripts folder is in PATH
$env:PATH -split ';' | Select-String "Scripts"

# Add it temporarily if needed
$env:PATH += ";$env:USERPROFILE\AppData\Local\Programs\Python\Python39\Scripts"
```

---

## 🎨 Alternative: Using Python Directly

If .bat files don't work, run commands directly:

```powershell
# Format
python -m black . --line-length=100 --exclude="/(Lib|Scripts|build|dist|\.venv|venv)/"
python -m isort . --profile=black --line-length=100

# Lint
python -m flake8 . --max-line-length=100 --ignore=E203,W503,E501 --exclude=Lib,Scripts,build,dist,.venv,venv

# Type check
python -m mypy analyzers agents generators llm orchestrator routes services --config-file=mypy.ini

# Test
python -m pytest --cov=. --cov-report=html --cov-report=term-missing --cov-fail-under=70
```

---

## 📋 Available Batch Files

| File | Description |
|------|-------------|
| `quality.bat` | Run all quality checks |
| `format.bat` | Format code with black and isort |
| `lint.bat` | Lint with flake8 |
| `type-check.bat` | Type check with mypy |
| `test-with-coverage.bat` | Run tests with coverage |
| `pre-commit-install.bat` | Install pre-commit hooks |
| `pre-commit-run.bat` | Run pre-commit manually |

---

## 🚀 Quick Commands Reference

```powershell
# One command to rule them all
.\quality.bat

# Or step by step
.\format.bat         # Fix formatting
.\lint.bat           # Check for issues
.\type-check.bat     # Verify types
.\test-with-coverage.bat  # Run tests
```

---

**All tools are ready to use on Windows!** 🎉

