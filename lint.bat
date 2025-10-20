@echo off
REM Lint code with flake8

echo Linting with flake8...
flake8 . --max-line-length=100 --ignore=E203,W503,E501 --exclude=Lib,Scripts,build,dist,.venv,venv

if %errorlevel% equ 0 (
    echo.
    echo Linting passed!
) else (
    echo.
    echo Linting failed - please fix the issues above
)

