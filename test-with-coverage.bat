@echo off
REM Run tests with coverage

echo Running tests with coverage...
pytest --cov=. --cov-report=html --cov-report=term-missing --cov-fail-under=70

if %errorlevel% equ 0 (
    echo.
    echo Tests passed with sufficient coverage!
    echo HTML coverage report generated in htmlcov/index.html
) else (
    echo.
    echo Tests failed or coverage below 70%%
)

