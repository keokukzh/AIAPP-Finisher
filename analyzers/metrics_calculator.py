"""Metrics calculation module for code quality analysis.

This module provides the MetricsCalculator class which calculates comprehensive
code quality metrics using external tools (radon, lizard) and internal analysis.
Metrics include cyclomatic complexity, maintainability index, technical debt,
and overall quality scores.

Typical usage example:
    calculator = MetricsCalculator()
    metrics = await calculator.calculate_metrics(
        project_path="/path/to/project",
        file_structure=file_data,
        analysis_results=results
    )
    print(f"Quality Score: {metrics['code_quality_score']}")

Classes:
    MetricsCalculator: Main class for calculating code quality metrics.
"""

import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from exceptions import AnalysisError

logger = logging.getLogger(__name__)


class MetricsCalculator:
    """Calculates comprehensive code quality metrics.

    Uses multiple analysis tools (radon for Python, lizard for multi-language)
    to calculate code metrics including complexity, maintainability, and
    technical debt. Aggregates results into an overall quality score.
    """

    async def calculate_metrics(
        self, project_path: str, file_structure: Dict[str, Any], analysis_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate comprehensive code quality metrics.

        Analyzes project code using multiple tools and techniques to generate
        a complete metrics report including lines of code, complexity scores,
        maintainability index, technical debt, and an overall quality score.

        Args:
            project_path: Absolute path to the project root directory.
            file_structure: Dictionary containing project file structure with
                keys 'all_files', 'directories', and 'file_types'.
            analysis_results: Dictionary containing existing analysis results
                for context and optimization.

        Returns:
            Dictionary containing comprehensive metrics with keys:
                - lines_of_code: Total lines of code
                - complexity_score: Overall complexity score
                - file_count: Number of analyzed files
                - directory_count: Number of directories
                - largest_files: List of largest files by line count
                - cyclomatic_complexity: Complexity analysis data
                - maintainability_index: Maintainability scores
                - technical_debt: Technical debt indicators
                - code_quality_score: Overall quality score (0-100)

        Raises:
            AnalysisError: If metrics calculation fails critically.

        Example:
            >>> calculator = MetricsCalculator()
            >>> metrics = await calculator.calculate_metrics(
            ...     "/path/to/project",
            ...     file_structure,
            ...     analysis_results
            ... )
            >>> print(f"Quality: {metrics['code_quality_score']}")
            Quality: 85.3
        """
        metrics = {
            "lines_of_code": 0,
            "complexity_score": 0,
            "file_count": len(file_structure.get("all_files", [])),
            "directory_count": len(file_structure.get("directories", [])),
            "largest_files": [],
            "most_common_extensions": [],
            "cyclomatic_complexity": {},
            "maintainability_index": {},
            "technical_debt": {},
            "code_quality_score": 0,
        }

        try:
            # 1. Basis-Metriken
            await self._calculate_basic_metrics(project_path, file_structure, metrics)

            # 2. Echte Komplexitäts-Analyse mit radon (Python)
            await self._calculate_radon_metrics(project_path, metrics, analysis_results)

            # 3. Echte Komplexitäts-Analyse mit lizard (Multi-Language)
            await self._calculate_lizard_metrics(project_path, metrics)

            # 4. Berechne Gesamt-Quality-Score
            metrics["code_quality_score"] = self._calculate_quality_score(metrics)

        except Exception as e:
            logger.error(f"Fehler bei der Metriken-Berechnung: {e}")

        return metrics

    async def _calculate_basic_metrics(
        self, project_path: str, file_structure: Dict[str, Any], metrics: Dict[str, Any]
    ):
        """Berechnet Basis-Metriken"""
        code_extensions = {
            ".py",
            ".js",
            ".ts",
            ".jsx",
            ".tsx",
            ".java",
            ".cpp",
            ".c",
            ".h",
            ".cs",
            ".php",
            ".rb",
            ".go",
            ".rs",
        }

        for file_info in file_structure.get("all_files", []):
            if file_info["extension"].lower() in code_extensions:
                file_path = Path(project_path) / file_info["path"]
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = len(f.readlines())
                        metrics["lines_of_code"] += lines

                        # Tracke größte Dateien
                        metrics["largest_files"].append(
                            {"path": file_info["path"], "lines": lines, "size": file_info["size"]}
                        )
                except Exception:
                    continue

        # Sortiere größte Dateien
        metrics["largest_files"].sort(key=lambda x: x["lines"], reverse=True)
        metrics["largest_files"] = metrics["largest_files"][:10]

        # Sortiere häufigste Extensions
        file_types = file_structure.get("file_types", {})
        metrics["most_common_extensions"] = sorted(
            file_types.items(), key=lambda x: x[1], reverse=True
        )[:10]

    async def _calculate_radon_metrics(
        self, project_path: str, metrics: Dict[str, Any], analysis_results: Dict[str, Any]
    ):
        """Berechnet echte Komplexitäts-Metriken mit radon"""
        try:
            # Finde Python-Dateien
            python_files = []
            for file_info in analysis_results.get("file_structure", {}).get("all_files", []):
                if file_info["extension"].lower() == ".py":
                    python_files.append(str(Path(project_path) / file_info["path"]))

            if not python_files:
                return

            # Radon Cyclomatic Complexity
            try:
                result = subprocess.run(
                    ["radon", "cc", "--json", "--min", "A", "--show-complexity"] + python_files,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode == 0:
                    radon_data = json.loads(result.stdout)
                    metrics["cyclomatic_complexity"] = radon_data

                    # Berechne durchschnittliche Komplexität
                    total_complexity = 0
                    function_count = 0
                    for file_data in radon_data.values():
                        if isinstance(file_data, list):
                            for func_data in file_data:
                                total_complexity += func_data.get("complexity", 0)
                                function_count += 1

                    if function_count > 0:
                        metrics["avg_cyclomatic_complexity"] = total_complexity / function_count

            except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
                logger.warning("Radon CC-Scan fehlgeschlagen")

            # Radon Maintainability Index
            try:
                result = subprocess.run(
                    ["radon", "mi", "--json", "--min", "A"] + python_files,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode == 0:
                    mi_data = json.loads(result.stdout)
                    metrics["maintainability_index"] = mi_data

                    # Berechne durchschnittlichen MI
                    total_mi = 0
                    file_count = 0
                    for file_path, file_mi in mi_data.items():
                        if isinstance(file_mi, (int, float)):
                            total_mi += file_mi
                            file_count += 1

                    if file_count > 0:
                        metrics["avg_maintainability_index"] = total_mi / file_count

            except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
                logger.warning("Radon MI-Scan fehlgeschlagen")

        except Exception as e:
            logger.error(f"Fehler bei Radon-Metriken: {e}")

    async def _calculate_lizard_metrics(self, project_path: str, metrics: Dict[str, Any]):
        """Berechnet echte Komplexitäts-Metriken mit lizard"""
        try:
            # Lizard-Scan für alle unterstützten Sprachen
            result = subprocess.run(
                ["lizard", "-l", "python,javascript,java,cpp,c", str(project_path)],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                output_lines = result.stdout.split("\n")
                metrics["lizard_analysis"] = {
                    "raw_output": result.stdout,
                    "parsed_metrics": self._parse_lizard_output(output_lines),
                }

                # Extrahiere wichtige Metriken
                parsed_metrics = metrics["lizard_analysis"]["parsed_metrics"]
                metrics["total_functions"] = parsed_metrics.get("total_functions", 0)
                metrics["avg_cyclomatic_complexity"] = parsed_metrics.get("avg_complexity", 0)
                metrics["avg_lines_per_function"] = parsed_metrics.get("avg_lines", 0)

                # Berechne Technical Debt
                metrics["technical_debt"] = {
                    "high_complexity_functions": parsed_metrics.get("high_complexity", 0),
                    "long_functions": parsed_metrics.get("long_functions", 0),
                    "total_debt_score": parsed_metrics.get("total_debt", 0),
                }

                # Detaillierte Funktionen-Analyse
                complex_functions = parsed_metrics.get("complex_functions", [])
                metrics["complex_functions"] = complex_functions[:10]

            else:
                logger.warning(f"Lizard-Scan fehlgeschlagen: {result.stderr}")

        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Lizard-Scan fehlgeschlagen: {e}")
        except Exception as e:
            logger.error(f"Fehler bei Lizard-Metriken: {e}")

    def _parse_lizard_output(self, output_lines: List[str]) -> Dict[str, Any]:
        """Parst Lizard Text-Output für Metriken"""
        metrics = {
            "total_functions": 0,
            "avg_complexity": 0,
            "avg_lines": 0,
            "high_complexity": 0,
            "long_functions": 0,
            "total_debt": 0,
            "complex_functions": [],
        }

        try:
            import re

            # Suche nach Summary-Zeilen
            for line in output_lines:
                if "Total nloc" in line:
                    numbers = re.findall(r"\d+", line)
                    if numbers:
                        metrics["total_functions"] = int(numbers[0])
                elif "Average CCN" in line:
                    numbers = re.findall(r"\d+\.?\d*", line)
                    if numbers:
                        metrics["avg_complexity"] = float(numbers[0])
                elif "Average nloc" in line:
                    numbers = re.findall(r"\d+\.?\d*", line)
                    if numbers:
                        metrics["avg_lines"] = float(numbers[0])
                elif "High CCN" in line:
                    numbers = re.findall(r"\d+", line)
                    if numbers:
                        metrics["high_complexity"] = int(numbers[0])
                elif "Long functions" in line:
                    numbers = re.findall(r"\d+", line)
                    if numbers:
                        metrics["long_functions"] = int(numbers[0])

            # Berechne Total Debt
            metrics["total_debt"] = metrics["high_complexity"] + metrics["long_functions"]

        except Exception as e:
            logger.debug(f"Fehler beim Parsen von Lizard-Output: {e}")

        return metrics

    def _calculate_quality_score(self, metrics: Dict[str, Any]) -> float:
        """Berechnet einen Gesamt-Quality-Score (0-100)"""
        try:
            score = 100.0

            # Abzug für hohe Komplexität
            avg_complexity = metrics.get("avg_cyclomatic_complexity", 0)
            if avg_complexity > 10:
                score -= min(30, (avg_complexity - 10) * 2)
            elif avg_complexity > 5:
                score -= min(20, (avg_complexity - 5) * 2)

            # Abzug für niedrigen Maintainability Index
            avg_mi = metrics.get("avg_maintainability_index", 100)
            if avg_mi < 20:
                score -= 25
            elif avg_mi < 50:
                score -= 15
            elif avg_mi < 80:
                score -= 5

            # Abzug für Technical Debt
            debt_score = metrics.get("technical_debt", {}).get("total_debt_score", 0)
            if debt_score > 20:
                score -= min(25, debt_score)
            elif debt_score > 10:
                score -= min(15, debt_score)
            elif debt_score > 5:
                score -= min(10, debt_score)

            # Bonus für gute Struktur
            if metrics.get("file_count", 0) > 0:
                avg_file_size = metrics.get("lines_of_code", 0) / metrics["file_count"]
                if avg_file_size < 200:
                    score += 5
                elif avg_file_size > 1000:
                    score -= 10

            return max(0, min(100, score))

        except Exception as e:
            logger.error(f"Fehler bei Quality-Score-Berechnung: {e}")
            return 50.0

    def calculate_ast_complexity_summary(
        self, analyzed_files: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Berechnet Komplexitäts-Summary aus AST-Analyse"""
        summary = {
            "total_files": len(analyzed_files),
            "avg_functions_per_file": 0,
            "avg_classes_per_file": 0,
            "avg_complexity_per_file": 0,
            "most_complex_files": [],
            "language_distribution": {},
        }

        if not analyzed_files:
            return summary

        total_functions = 0
        total_classes = 0
        total_complexity = 0
        language_counts = {}

        for file_analysis in analyzed_files:
            functions = file_analysis.get("functions", [])
            classes = file_analysis.get("classes", [])
            complexity_metrics = file_analysis.get("complexity_metrics", {})
            language = file_analysis.get("language", "unknown")

            total_functions += len(functions)
            total_classes += len(classes)
            total_complexity += complexity_metrics.get("cyclomatic_complexity", 0)

            language_counts[language] = language_counts.get(language, 0) + 1

            # Tracke komplexeste Dateien
            if complexity_metrics.get("cyclomatic_complexity", 0) > 0:
                summary["most_complex_files"].append(
                    {
                        "file": file_analysis.get("file_path", ""),
                        "complexity": complexity_metrics.get("cyclomatic_complexity", 0),
                        "functions": len(functions),
                        "classes": len(classes),
                    }
                )

        # Berechne Durchschnittswerte
        summary["avg_functions_per_file"] = total_functions / len(analyzed_files)
        summary["avg_classes_per_file"] = total_classes / len(analyzed_files)
        summary["avg_complexity_per_file"] = total_complexity / len(analyzed_files)
        summary["language_distribution"] = language_counts

        # Sortiere komplexeste Dateien
        summary["most_complex_files"].sort(key=lambda x: x["complexity"], reverse=True)
        summary["most_complex_files"] = summary["most_complex_files"][:10]

        return summary
