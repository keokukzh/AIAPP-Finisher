"""
AST Analyzer - Analyzes source code using Abstract Syntax Trees
Refactored to use specialized language parsers
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

from .ast_parsers import JavaScriptParser, PythonParser

logger = logging.getLogger(__name__)


class ASTAnalyzer:
    """Koordiniert AST-basierte Code-Analyse"""

    def __init__(self):
        self.python_parser = PythonParser()
        self.javascript_parser = JavaScriptParser()

        self.language_extensions = {
            "python": {".py"},
            "javascript": {".js", ".jsx", ".ts", ".tsx", ".mjs"},
        }

    async def analyze_file(self, file_path: str, language: str = None) -> Dict[str, Any]:
        """Analysiert eine einzelne Datei"""
        try:
            path = Path(file_path)

            # Auto-detect language if not provided
            if not language:
                language = self._detect_language(path)

            # Route to appropriate parser
            if language == "python":
                return await self.python_parser.parse_file(path)
            elif language == "javascript":
                return await self.javascript_parser.parse_file(path)
            else:
                logger.debug(f"Unsupported language for AST analysis: {language}")
                return {}

        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return {}

    async def analyze_project(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analysiert alle relevanten Dateien im Projekt"""
        analysis_results = {
            "files_analyzed": 0,
            "total_classes": 0,
            "total_functions": 0,
            "total_imports": 0,
            "average_complexity": 0,
            "by_language": {
                "python": {"files": 0, "classes": 0, "functions": 0},
                "javascript": {"files": 0, "classes": 0, "functions": 0},
            },
        }

        try:
            all_files = file_structure.get("all_files", [])
            total_complexity = 0

            for file_info in all_files:
                ext = file_info["extension"].lower()
                language = self._detect_language_by_extension(ext)

                if language:
                    file_path = Path(project_path) / file_info["path"]
                    result = await self.analyze_file(str(file_path), language)

                    if result:
                        analysis_results["files_analyzed"] += 1
                        analysis_results["total_classes"] += len(result.get("classes", []))
                        analysis_results["total_functions"] += len(result.get("functions", []))
                        analysis_results["total_imports"] += len(result.get("imports", []))
                        total_complexity += result.get("complexity", 0)

                        # Update by-language stats
                        lang_stats = analysis_results["by_language"].get(language, {})
                        lang_stats["files"] = lang_stats.get("files", 0) + 1
                        lang_stats["classes"] = lang_stats.get("classes", 0) + len(
                            result.get("classes", [])
                        )
                        lang_stats["functions"] = lang_stats.get("functions", 0) + len(
                            result.get("functions", [])
                        )
                        analysis_results["by_language"][language] = lang_stats

            # Calculate average complexity
            if analysis_results["files_analyzed"] > 0:
                analysis_results["average_complexity"] = (
                    total_complexity / analysis_results["files_analyzed"]
                )

            logger.info(
                f"AST analysis completed: {analysis_results['files_analyzed']} files analyzed"
            )

        except Exception as e:
            logger.error(f"Error during project AST analysis: {e}")

        return analysis_results

    def _detect_language(self, file_path: Path) -> str:
        """Detects language from file extension"""
        ext = file_path.suffix.lower()
        return self._detect_language_by_extension(ext)

    def _detect_language_by_extension(self, extension: str) -> str:
        """Detects language from extension string"""
        for language, extensions in self.language_extensions.items():
            if extension in extensions:
                return language
        return None
