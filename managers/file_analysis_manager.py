"""
File Analysis Manager - Coordinates all file analysis operations
Implements Manager pattern for file analysis
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class FileAnalysisManager:
    """Manages and coordinates file analysis operations using composition"""

    def __init__(self, language_detector, framework_detector, ast_analyzer):
        # Composition over inheritance - inject dependencies
        self.language_detector = language_detector
        self.framework_detector = framework_detector
        self.ast_analyzer = ast_analyzer

        self.analysis_cache = {}

    async def analyze_files(
        self, project_path: str, file_structure: Dict[str, Any], progress_callback=None
    ) -> Dict[str, Any]:
        """Coordinate complete file analysis"""
        results = {
            "languages": [],
            "frameworks": [],
            "ast_analysis": {},
            "file_count": 0,
            "total_lines": 0,
        }

        try:
            # Phase 1: Detect languages
            if progress_callback:
                progress_callback("Detecting languages", 0.25)

            languages = await self.language_detector.detect_languages(project_path, file_structure)
            results["languages"] = languages

            # Phase 2: Detect frameworks
            if progress_callback:
                progress_callback("Detecting frameworks", 0.50)

            frameworks = await self.framework_detector.detect_frameworks(
                project_path, file_structure
            )
            results["frameworks"] = frameworks

            # Phase 3: AST analysis
            if progress_callback:
                progress_callback("Performing AST analysis", 0.75)

            ast_results = await self.ast_analyzer.analyze_project(project_path, file_structure)
            results["ast_analysis"] = ast_results

            # Calculate totals
            results["file_count"] = len(file_structure.get("all_files", []))
            results["total_lines"] = sum(
                f.get("lines", 0) for f in file_structure.get("all_files", [])
            )

            if progress_callback:
                progress_callback("File analysis complete", 1.0)

            logger.info(
                f"File analysis complete: {results['file_count']} files, "
                f"{len(languages)} languages, {len(frameworks)} frameworks"
            )

        except Exception as e:
            logger.error(f"Error in file analysis: {e}")
            raise

        return results

    def get_cached_analysis(self, project_path: str) -> Dict[str, Any]:
        """Get cached analysis results"""
        return self.analysis_cache.get(project_path)

    def cache_analysis(self, project_path: str, results: Dict[str, Any]):
        """Cache analysis results"""
        self.analysis_cache[project_path] = results
