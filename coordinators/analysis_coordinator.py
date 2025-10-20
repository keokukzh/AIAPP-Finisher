"""
Analysis Coordinator - Coordinates full project analysis
Implements Coordinator pattern for analysis
"""

import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


class AnalysisCoordinator:
    """Coordinates complete project analysis using composition"""

    def __init__(
        self,
        file_analysis_manager,
        api_extraction_manager,
        security_scan_manager,
        metrics_calculation_manager,
        database_analyzer,
        dependency_analyzer,
    ):
        # Composition over inheritance - inject all dependencies
        self.file_analysis_manager = file_analysis_manager
        self.api_extraction_manager = api_extraction_manager
        self.security_scan_manager = security_scan_manager
        self.metrics_calculation_manager = metrics_calculation_manager
        self.database_analyzer = database_analyzer
        self.dependency_analyzer = dependency_analyzer

        self.analysis_history = []

    async def perform_full_analysis(
        self, project_path: str, file_structure: Dict[str, Any], progress_callback=None
    ) -> Dict[str, Any]:
        """Coordinate complete project analysis"""
        results = {
            "project_path": project_path,
            "project_name": project_path.split("/")[-1],
            "timestamp": datetime.now().isoformat(),
            "file_analysis": {},
            "api_analysis": {},
            "security_analysis": {},
            "metrics": {},
            "database_schema": {},
            "dependencies": {},
        }

        try:
            start_time = datetime.now()

            # Phase 1: File Analysis (Languages, Frameworks, AST)
            if progress_callback:
                progress_callback("Analyzing files", 0.15)

            file_results = await self.file_analysis_manager.analyze_files(
                project_path, file_structure, progress_callback
            )
            results["file_analysis"] = file_results

            # Phase 2: API Extraction
            if progress_callback:
                progress_callback("Extracting API endpoints", 0.30)

            api_results = await self.api_extraction_manager.extract_all_endpoints(
                project_path, file_structure, file_results.get("frameworks", []), progress_callback
            )
            results["api_analysis"] = api_results

            # Phase 3: Dependency Analysis
            if progress_callback:
                progress_callback("Analyzing dependencies", 0.45)

            dependency_results = await self.dependency_analyzer.analyze_dependencies(
                project_path, file_structure
            )
            results["dependencies"] = dependency_results

            # Phase 4: Database Schema
            if progress_callback:
                progress_callback("Extracting database schema", 0.60)

            db_results = await self.database_analyzer.extract_schema(project_path, file_structure)
            results["database_schema"] = db_results

            # Phase 5: Security Scan
            if progress_callback:
                progress_callback("Performing security scan", 0.75)

            security_results = await self.security_scan_manager.perform_full_scan(
                project_path, file_structure, dependency_results, progress_callback
            )
            results["security_analysis"] = security_results

            # Phase 6: Metrics Calculation
            if progress_callback:
                progress_callback("Calculating metrics", 0.90)

            metrics_results = await self.metrics_calculation_manager.calculate_all_metrics(
                project_path,
                file_structure,
                file_results.get("ast_analysis", {}),
                progress_callback,
            )
            results["metrics"] = metrics_results

            # Calculate totals
            end_time = datetime.now()
            results["analysis_duration"] = (end_time - start_time).total_seconds()
            results["file_count"] = file_results.get("file_count", 0)
            results["lines_of_code"] = metrics_results.get("lines_of_code", 0)
            results["languages"] = file_results.get("languages", [])
            results["frameworks"] = file_results.get("frameworks", [])
            results["api_endpoints"] = api_results.get("endpoints", [])
            results["dependency_count"] = len(dependency_results.get("packages", []))
            results["security_score"] = security_results.get("security_score", 100)
            results["code_quality_score"] = metrics_results.get("code_quality_score", 0)

            # Record in history
            self.analysis_history.append(
                {
                    "project_path": project_path,
                    "timestamp": start_time.isoformat(),
                    "duration": results["analysis_duration"],
                    "file_count": results["file_count"],
                    "lines_of_code": results["lines_of_code"],
                }
            )

            if progress_callback:
                progress_callback("Analysis complete", 1.0)

            logger.info(
                f"Full analysis complete for {project_path}: "
                f"{results['file_count']} files, "
                f"{results['lines_of_code']} LOC, "
                f"duration: {results['analysis_duration']:.2f}s"
            )

        except Exception as e:
            logger.error(f"Error coordinating analysis: {e}")
            raise

        return results

    def get_analysis_history(self):
        """Get analysis history"""
        return self.analysis_history
