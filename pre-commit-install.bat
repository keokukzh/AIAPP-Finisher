@echo off
REM Install pre-commit hooks

echo Installing pre-commit hooks...
pre-commit install

if %errorlevel% equ 0 (
    echo.
    echo Pre-commit hooks installed successfully!
    echo Hooks will now run automatically on git commit
) else (
    echo.
    echo Failed to install pre-commit hooks
    echo Make sure pre-commit is installed: pip install pre-commit
)

