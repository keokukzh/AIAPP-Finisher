"""
Project Analyzer - Orchestrates project analysis
Refactored to delegate to specialized analyzers
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .api_analyzer import APIAnalyzer
from .ast_analyzer import ASTAnalyzer
from .database_analyzer import DatabaseAnalyzer
from .dependency_analyzer import DependencyAnalyzer
from .framework_detector import FrameworkDetector
from .language_detector import LanguageDetector
from .metrics_calculator import MetricsCalculator
from .report_generator_helper import ReportGeneratorHelper
from .security_scanner import SecurityScanner
from .test_coverage_analyzer import TestCoverageAnalyzer

logger = logging.getLogger(__name__)


class ProjectAnalyzer:
    """Orchestrates project analysis using specialized analyzers"""

    def __init__(self):
        # Initialize all specialized analyzers
        self.language_detector = LanguageDetector()
        self.framework_detector = FrameworkDetector()
        self.dependency_analyzer = DependencyAnalyzer()
        self.database_analyzer = DatabaseAnalyzer()
        self.api_analyzer = APIAnalyzer()
        self.ast_analyzer = ASTAnalyzer()
        self.metrics_calculator = MetricsCalculator()
        self.security_scanner = SecurityScanner()
        self.test_coverage_analyzer = TestCoverageAnalyzer()
        self.report_generator = ReportGeneratorHelper()

        self.analysis_results = {}
        self.progress_callback = None

    async def analyze_project(self, project_path: str, progress_callback=None) -> Dict[str, Any]:
        """Orchestrates complete project analysis"""
        self.progress_callback = progress_callback
        self.analysis_results = {
            "project_name": Path(project_path).name,
            "project_path": project_path,
            "analysis_date": datetime.now().isoformat(),
            "analysis_status": "running",
        }

        try:
            # Phase 1: Dateien scannen
            await self._update_progress("📁 Scanne Dateien...", 10)
            file_structure = await self._scan_files(project_path)
            self.analysis_results["file_structure"] = file_structure
            self.analysis_results["file_count"] = len(file_structure.get("all_files", []))

            # Phase 2: Sprachen erkennen
            await self._update_progress("🔍 Erkenne Sprachen...", 20)
            languages = await self.language_detector.detect_languages(project_path, file_structure)
            self.analysis_results["languages"] = languages

            # Phase 3: Frameworks identifizieren
            await self._update_progress("🛠️ Identifiziere Frameworks...", 30)
            frameworks = await self.framework_detector.detect_frameworks(
                project_path, file_structure
            )
            self.analysis_results["frameworks"] = frameworks

            # Phase 4: Dependencies analysieren
            await self._update_progress("📦 Analysiere Dependencies...", 40)
            dependencies = await self.dependency_analyzer.analyze_dependencies(
                project_path, file_structure
            )
            self.analysis_results["dependencies"] = dependencies
            self.analysis_results["dependency_count"] = len(dependencies.get("packages", []))

            # Phase 5: API-Endpoints extrahieren
            await self._update_progress("🗄️ Extrahiere API-Endpoints...", 50)
            api_endpoints = await self.api_analyzer.extract_endpoints(project_path, file_structure)
            self.analysis_results["api_endpoints"] = api_endpoints

            # Phase 6: Datenbank-Schema extrahieren
            await self._update_progress("🗃️ Extrahiere Datenbank-Schema...", 60)
            database_schema = await self.database_analyzer.extract_schema(
                project_path, file_structure
            )
            self.analysis_results["database_schema"] = database_schema

            # Phase 7: AST-Analyse durchführen
            await self._update_progress("🌳 Führe AST-Analyse durch...", 70)
            ast_analysis = await self._perform_ast_analysis(project_path, file_structure)
            self.analysis_results["ast_analysis"] = ast_analysis

            # Phase 8: Code-Metriken berechnen
            await self._update_progress("📊 Berechne Metriken...", 80)
            metrics = await self.metrics_calculator.calculate_metrics(
                project_path, file_structure, self.analysis_results
            )
            self.analysis_results.update(metrics)

            # Phase 9: Security-Scan
            await self._update_progress("🔒 Führe Security-Scan durch...", 90)
            security_issues = await self.security_scanner.scan_security(
                project_path, dependencies, file_structure
            )
            self.analysis_results["security_issues"] = security_issues

            # Phase 10: Test-Coverage analysieren
            await self._update_progress("🧪 Analysiere Test-Coverage...", 95)
            test_coverage = await self.test_coverage_analyzer.analyze_test_coverage(
                project_path, file_structure
            )
            self.analysis_results["test_coverage"] = test_coverage

            # Phase 11: Finalisierung
            await self._update_progress("✅ Analyse abgeschlossen!", 100)
            self.analysis_results["analysis_status"] = "completed"

            # Generiere Berichte
            await self.report_generator.generate_reports(project_path, self.analysis_results)

            return self.analysis_results

        except Exception as e:
            logger.error(f"Fehler bei der Projekt-Analyse: {e}")
            self.analysis_results["analysis_status"] = "error"
            self.analysis_results["error"] = str(e)
            raise

    async def _scan_files(self, project_path: str) -> Dict[str, Any]:
        """Scannt alle Dateien im Projekt mit Live-Updates"""
        file_structure = {"all_files": [], "directories": [], "file_types": {}, "ignored_files": []}

        try:
            project_root = Path(project_path)

            # Ignore-Patterns
            ignore_patterns = {
                ".git",
                "__pycache__",
                "node_modules",
                ".venv",
                "venv",
                ".env",
                ".DS_Store",
                "*.pyc",
                "*.pyo",
                "*.pyd",
                "*.log",
                "*.tmp",
                "*.cache",
                ".pytest_cache",
                "Lib",
                "site-packages",
                "dist-packages",
                "build",
                "dist",
                ".build",
                ".dist",
                ".vscode",
                ".idea",
                ".vs",
                "Thumbs.db",
                "desktop.ini",
                "*.zip",
                "*.tar",
                "*.gz",
                "*.rar",
                "*.7z",
                "*.mp4",
                "*.avi",
                "*.mov",
                "*.wmv",
                "*.flv",
                "*.mp3",
                "*.wav",
                "*.flac",
                "*.aac",
                "*.jpg",
                "*.jpeg",
                "*.png",
                "*.gif",
                "*.bmp",
                "*.tiff",
                "*.pdf",
                "*.doc",
                "*.docx",
                "*.xls",
                "*.xlsx",
                "*.ppt",
                "*.pptx",
            }

            all_paths = list(project_root.rglob("*"))
            total_files = len([p for p in all_paths if p.is_file()])
            processed_files = 0

            for file_path in all_paths:
                # Prüfe Ignore-Patterns
                file_path_str = str(file_path)
                should_ignore = any(pattern in file_path_str for pattern in ignore_patterns)

                # Ignoriere sehr große Dateien (>10MB)
                if file_path.is_file():
                    try:
                        if file_path.stat().st_size > 10 * 1024 * 1024:
                            should_ignore = True
                    except:
                        should_ignore = True

                if should_ignore:
                    file_structure["ignored_files"].append(str(file_path))
                    continue

                if file_path.is_file():
                    file_structure["all_files"].append(
                        {
                            "path": str(file_path.relative_to(project_root)),
                            "size": file_path.stat().st_size,
                            "extension": file_path.suffix,
                            "modified": datetime.fromtimestamp(
                                file_path.stat().st_mtime
                            ).isoformat(),
                        }
                    )

                    # Zähle Dateitypen
                    ext = file_path.suffix.lower()
                    file_structure["file_types"][ext] = file_structure["file_types"].get(ext, 0) + 1

                    processed_files += 1

                    # Live-Update
                    if processed_files % 10 == 0 or file_path.suffix in [
                        ".py",
                        ".js",
                        ".ts",
                        ".tsx",
                        ".jsx",
                    ]:
                        progress = (
                            int((processed_files / total_files) * 100) if total_files > 0 else 0
                        )
                        await self._update_progress(
                            f"📁 Scanne Dateien... ({processed_files}/{total_files})",
                            progress,
                            {
                                "current_file": str(file_path.relative_to(project_root)),
                                "files_analyzed": processed_files,
                                "total_files": total_files,
                            },
                        )

                elif file_path.is_dir():
                    file_structure["directories"].append(str(file_path.relative_to(project_root)))

        except Exception as e:
            logger.error(f"Fehler beim Datei-Scan: {e}")

        return file_structure

    async def _perform_ast_analysis(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Führt AST-Analyse durch und delegiert Komplexitätsberechnung"""
        ast_results = {
            "analyzed_files": [],
            "total_functions": 0,
            "total_classes": 0,
            "total_imports": 0,
            "languages_analyzed": set(),
            "complexity_summary": {},
            "code_issues_summary": [],
        }

        try:
            # Analysiere wichtige Code-Dateien
            code_extensions = {
                ".py",
                ".js",
                ".ts",
                ".jsx",
                ".tsx",
                ".java",
                ".cpp",
                ".c",
                ".cs",
                ".php",
                ".rb",
                ".go",
                ".rs",
            }

            code_files = [
                f
                for f in file_structure.get("all_files", [])
                if (
                    f["extension"].lower() in code_extensions
                    and f["size"] < 1024 * 1024
                    and not any(
                        ignore in f["path"]
                        for ignore in ["Lib/", "site-packages/", "dist-packages/", "__pycache__/"]
                    )
                )
            ]

            # Begrenze auf 100 Dateien
            if len(code_files) > 100:
                important_files = [
                    f
                    for f in code_files
                    if any(
                        important in f["path"]
                        for important in ["src/", "app/", "main.", "index.", "app.py", "main.py"]
                    )
                ]
                other_files = [f for f in code_files if f not in important_files]
                code_files = important_files + other_files[: 100 - len(important_files)]

            total_code_files = len(code_files)
            analyzed_files = 0

            for file_info in code_files:
                file_path = Path(project_path) / file_info["path"]

                try:
                    analyzed_files += 1
                    progress = (
                        int((analyzed_files / total_code_files) * 100)
                        if total_code_files > 0
                        else 0
                    )
                    await self._update_progress(
                        f"🌳 AST-Analyse... ({analyzed_files}/{total_code_files})",
                        progress,
                        {
                            "current_file": file_info["path"],
                            "files_analyzed": analyzed_files,
                            "total_files": total_code_files,
                        },
                    )

                    analysis_result = await self.ast_analyzer.analyze_file(str(file_path))

                    if "error" not in analysis_result:
                        ast_results["analyzed_files"].append(analysis_result)

                        # Sammle Statistiken
                        ast_results["total_functions"] += len(analysis_result.get("functions", []))
                        ast_results["total_classes"] += len(analysis_result.get("classes", []))
                        ast_results["total_imports"] += len(analysis_result.get("imports", []))
                        ast_results["languages_analyzed"].add(
                            analysis_result.get("language", "unknown")
                        )

                        # Sammle Code-Issues
                        issues = analysis_result.get("code_issues", [])
                        for issue in issues:
                            issue["file"] = file_info["path"]
                            ast_results["code_issues_summary"].append(issue)

                except Exception as e:
                    logger.debug(f"Fehler bei AST-Analyse von {file_info['path']}: {e}")
                    continue

            # Konvertiere Set zu Liste
            ast_results["languages_analyzed"] = list(ast_results["languages_analyzed"])

            # Delegate complexity calculation to MetricsCalculator
            ast_results["complexity_summary"] = (
                self.metrics_calculator.calculate_ast_complexity_summary(
                    ast_results["analyzed_files"]
                )
            )

            # Sortiere Code-Issues
            ast_results["code_issues_summary"].sort(
                key=lambda x: {"high": 3, "medium": 2, "low": 1}.get(x.get("severity", "low"), 1),
                reverse=True,
            )

            logger.info(
                f"AST-Analyse abgeschlossen: {len(ast_results['analyzed_files'])} Dateien analysiert"
            )

        except Exception as e:
            logger.error(f"Fehler bei AST-Analyse: {e}")
            ast_results["error"] = str(e)

        return ast_results

    async def _update_progress(self, message: str, percentage: int, details: Dict = None):
        """Aktualisiert den Fortschritt mit Details"""
        if self.progress_callback:
            await self.progress_callback(message, percentage, details)

        if details and "current_file" in details:
            logger.info(f"Progress: {percentage}% - {message} | File: {details['current_file']}")
        elif details and "files_analyzed" in details:
            logger.info(
                f"Progress: {percentage}% - {message} | Files: {details['files_analyzed']}/{details['total_files']}"
            )
        else:
            logger.info(f"Progress: {percentage}% - {message}")

    def get_analysis_results(self) -> Dict[str, Any]:
        """Gibt die aktuellen Analyse-Ergebnisse zurück"""
        return self.analysis_results.copy()

    def is_analysis_complete(self) -> bool:
        """Prüft ob die Analyse abgeschlossen ist"""
        return self.analysis_results.get("analysis_status") == "completed"
