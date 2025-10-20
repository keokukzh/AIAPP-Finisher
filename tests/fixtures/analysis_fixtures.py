"""Pytest fixtures for analysis testing.

Provides reusable fixtures for testing analysis, agents, and generation operations.
"""

import json
from pathlib import Path
from typing import Any, Dict

import pytest


@pytest.fixture
def sample_project_path(tmp_path: Path) -> Path:
    """Create a temporary sample project structure.

    Args:
        tmp_path: pytest's temporary path fixture.

    Returns:
        Path to the created sample project.
    """
    project = tmp_path / "sample_project"
    project.mkdir()

    # Create sample Python files
    (project / "main.py").write_text(
        '''
"""Main application module."""

def hello(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"

def main():
    """Application entry point."""
    print(hello("World"))

if __name__ == "__main__":
    main()
'''
    )

    (project / "utils.py").write_text(
        '''
"""Utility functions."""

def calculate_sum(a: int, b: int) -> int:
    """Calculate sum of two numbers."""
    return a + b
'''
    )

    # Create requirements.txt
    (project / "requirements.txt").write_text(
        """
fastapi==0.104.1
streamlit==1.29.0
pytest==7.4.3
"""
    )

    # Create package.json
    (project / "package.json").write_text(
        json.dumps(
            {
                "name": "sample-project",
                "version": "1.0.0",
                "dependencies": {"react": "^18.0.0", "axios": "^1.6.0"},
            },
            indent=2,
        )
    )

    # Create README
    (project / "README.md").write_text(
        """
# Sample Project

This is a test project for analysis.
"""
    )

    return project


@pytest.fixture
def mock_analysis_results() -> Dict[str, Any]:
    """Provide mock analysis results for testing.

    Returns:
        Dictionary containing complete mock analysis results.
    """
    return {
        "project_path": "/test/project",
        "project_name": "test-project",
        "analysis_timestamp": "2025-10-20T12:00:00",
        "file_count": 25,
        "total_files": 25,
        "lines_of_code": 1500,
        "languages": [
            {"name": "Python", "percentage": 70.0, "lines": 1050, "files": 15},
            {"name": "JavaScript", "percentage": 30.0, "lines": 450, "files": 10},
        ],
        "frameworks": [
            {"name": "FastAPI", "type": "Backend", "version": "0.104.1", "confidence": 0.95},
            {"name": "React", "type": "Frontend", "version": "18.0.0", "confidence": 0.90},
        ],
        "dependencies": {
            "python": [
                {"name": "fastapi", "version": "0.104.1", "type": "direct", "ecosystem": "pip"},
                {"name": "streamlit", "version": "1.29.0", "type": "direct", "ecosystem": "pip"},
            ],
            "javascript": [
                {"name": "react", "version": "18.0.0", "type": "direct", "ecosystem": "npm"},
                {"name": "axios", "version": "1.6.0", "type": "direct", "ecosystem": "npm"},
            ],
        },
        "dependency_count": 4,
        "api_endpoints": [
            {
                "path": "/api/users",
                "method": "GET",
                "handler": "get_users",
                "file_path": "app/routes.py",
                "line_number": 10,
                "parameters": ["limit", "offset"],
                "authenticated": True,
            }
        ],
        "api_count": 1,
        "database_schema": {
            "database_type": "PostgreSQL",
            "tables": [{"name": "users", "columns": 5}, {"name": "posts", "columns": 8}],
            "models": [{"name": "User", "fields": 5}, {"name": "Post", "fields": 8}],
            "migrations_count": 12,
        },
        "metrics": {
            "complexity": 5.2,
            "cyclomatic_complexity": 8.5,
            "maintainability_index": 85.0,
            "code_quality_score": 88.5,
            "technical_debt": 2.5,
            "lines_of_code": 1500,
            "comment_ratio": 0.15,
        },
        "security_analysis": {
            "security_score": 85.0,
            "vulnerabilities": [
                {
                    "severity": "medium",
                    "title": "Insecure dependency version",
                    "description": "Using outdated library version",
                    "file_path": "requirements.txt",
                    "line_number": 5,
                    "cve_id": "CVE-2024-1234",
                    "recommendation": "Update to latest version",
                }
            ],
            "total_issues": 1,
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 1,
            "low_count": 0,
        },
        "test_coverage": {
            "coverage_percentage": 75.5,
            "lines_covered": 1132,
            "lines_total": 1500,
            "test_files_count": 8,
            "test_frameworks": ["pytest"],
        },
        "analysis_duration": 45.3,
        "analysis_phases": [
            "initialization",
            "file_scanning",
            "language_detection",
            "framework_detection",
            "dependency_analysis",
            "api_analysis",
            "database_analysis",
            "security_scan",
            "metrics_calculation",
            "report_generation",
            "completed",
        ],
    }


@pytest.fixture
def mock_security_results() -> Dict[str, Any]:
    """Provide mock security analysis results.

    Returns:
        Dictionary containing security scan results.
    """
    return {
        "security_score": 75.0,
        "vulnerabilities": [
            {
                "severity": "critical",
                "title": "SQL Injection vulnerability",
                "description": "Unsanitized user input in SQL query",
                "file_path": "app/database.py",
                "line_number": 42,
                "cve_id": None,
                "recommendation": "Use parameterized queries",
            },
            {
                "severity": "high",
                "title": "Hardcoded secret",
                "description": "API key found in source code",
                "file_path": "config.py",
                "line_number": 15,
                "cve_id": None,
                "recommendation": "Move to environment variables",
            },
        ],
        "total_issues": 2,
        "critical_count": 1,
        "high_count": 1,
        "medium_count": 0,
        "low_count": 0,
    }


@pytest.fixture
def mock_metrics() -> Dict[str, Any]:
    """Provide mock code quality metrics.

    Returns:
        Dictionary containing code quality metrics.
    """
    return {
        "complexity": 12.5,
        "cyclomatic_complexity": 15.3,
        "maintainability_index": 72.0,
        "code_quality_score": 78.5,
        "technical_debt": 8.2,
        "lines_of_code": 5000,
        "comment_ratio": 0.12,
    }


@pytest.fixture
async def project_analyzer():
    """Provide a configured ProjectAnalyzer instance.

    Yields:
        ProjectAnalyzer instance ready for testing.
    """
    from analyzers.project_analyzer import ProjectAnalyzer

    analyzer = ProjectAnalyzer()
    yield analyzer
    # Cleanup if needed
    analyzer.analysis_results = {}


@pytest.fixture
def mock_llm_response() -> Dict[str, Any]:
    """Provide mock LLM response.

    Returns:
        Dictionary containing mock LLM response data.
    """
    return {
        "model": "gpt-4",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "This is a mock LLM response for testing.",
                }
            }
        ],
        "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
    }
