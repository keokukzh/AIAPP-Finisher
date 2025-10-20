@echo off
REM Run pre-commit hooks manually

echo Running pre-commit hooks on all files...
pre-commit run --all-files

if %errorlevel% equ 0 (
    echo.
    echo All pre-commit hooks passed!
) else (
    echo.
    echo Some pre-commit hooks failed - please fix the issues above
)

