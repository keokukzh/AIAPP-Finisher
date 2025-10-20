@echo off
REM Run all quality checks

echo ========================================
echo Running Quality Checks
echo ========================================

echo.
echo [1/5] Formatting code with black...
black . --line-length=100 --exclude="/(Lib|Scripts|build|dist|\.venv|venv)/"
if %errorlevel% neq 0 (
    echo ERROR: black formatting failed
    exit /b 1
)

echo.
echo [2/5] Sorting imports with isort...
isort . --profile=black --line-length=100 --skip-glob="Lib/*" --skip-glob="Scripts/*"
if %errorlevel% neq 0 (
    echo ERROR: isort failed
    exit /b 1
)

echo.
echo [3/5] Linting with flake8...
flake8 . --max-line-length=100 --ignore=E203,W503,E501 --exclude=Lib,Scripts,build,dist,.venv,venv
if %errorlevel% neq 0 (
    echo ERROR: flake8 linting failed
    exit /b 1
)

echo.
echo [4/5] Type checking with mypy...
mypy analyzers agents generators llm orchestrator routes services --config-file=mypy.ini
if %errorlevel% neq 0 (
    echo ERROR: mypy type checking failed
    exit /b 1
)

echo.
echo [5/5] Running tests with coverage...
pytest --cov=. --cov-report=html --cov-report=term-missing --cov-fail-under=70
if %errorlevel% neq 0 (
    echo ERROR: tests failed or coverage below 70%%
    exit /b 1
)

echo.
echo ========================================
echo All quality checks passed!
echo ========================================

