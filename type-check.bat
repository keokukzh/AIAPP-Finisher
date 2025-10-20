@echo off
REM Type check with mypy

echo Type checking with mypy...
mypy analyzers agents generators llm orchestrator routes services --config-file=mypy.ini

if %errorlevel% equ 0 (
    echo.
    echo Type checking passed!
) else (
    echo.
    echo Type checking failed - please fix the issues above
)

