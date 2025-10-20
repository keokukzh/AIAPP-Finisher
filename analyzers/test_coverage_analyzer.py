"""
Test Coverage Analyzer - Analyzes test coverage
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class TestCoverageAnalyzer:
    """Analyzes test coverage and test frameworks"""

    async def analyze_test_coverage(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analysiert Test-Coverage"""
        test_coverage = {
            "coverage_percentage": 0,
            "test_files": [],
            "test_frameworks": [],
            "missing_tests": [],
        }

        try:
            # Finde Test-Dateien
            test_patterns = ["test_", "_test", ".test.", ".spec."]
            test_files = []

            for file_info in file_structure.get("all_files", []):
                file_name = Path(file_info["path"]).name.lower()
                if any(pattern in file_name for pattern in test_patterns):
                    test_files.append(file_info["path"])

            test_coverage["test_files"] = test_files

            # Erkenne Test-Frameworks
            test_frameworks = set()
            for file_info in file_structure.get("all_files", []):
                if file_info["extension"].lower() == ".py":
                    file_path = Path(project_path) / file_info["path"]
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            if "import pytest" in content or "from pytest" in content:
                                test_frameworks.add("pytest")
                            if "import unittest" in content or "from unittest" in content:
                                test_frameworks.add("unittest")
                    except Exception:
                        continue

            test_coverage["test_frameworks"] = list(test_frameworks)

            # Simuliere Coverage-Prozentsatz
            total_code_files = len(
                [
                    f
                    for f in file_structure.get("all_files", [])
                    if f["extension"].lower() in {".py", ".js", ".ts"}
                ]
            )
            test_coverage["coverage_percentage"] = min(
                100, (len(test_files) / max(1, total_code_files)) * 100
            )

        except Exception as e:
            logger.error(f"Fehler bei der Test-Coverage-Analyse: {e}")

        return test_coverage
