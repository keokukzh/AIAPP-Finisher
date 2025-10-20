@echo off
REM Format code with black and isort

echo Formatting code with black...
black . --line-length=100 --exclude="/(Lib|Scripts|build|dist|\.venv|venv)/"

echo.
echo Sorting imports with isort...
isort . --profile=black --line-length=100 --skip-glob="Lib/*" --skip-glob="Scripts/*"

echo.
echo Done! Code formatted.

