"""
API Extraction Manager - Coordinates API endpoint extraction
Implements Manager pattern for API analysis
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class APIExtractionManager:
    """Manages and coordinates API endpoint extraction using composition"""

    def __init__(self, api_analyzer):
        # Composition over inheritance - inject dependency
        self.api_analyzer = api_analyzer

        self.extraction_cache = {}

    async def extract_all_endpoints(
        self,
        project_path: str,
        file_structure: Dict[str, Any],
        frameworks: List[Dict[str, Any]],
        progress_callback=None,
    ) -> Dict[str, Any]:
        """Coordinate complete API endpoint extraction"""
        results = {
            "endpoints": [],
            "by_framework": {},
            "total_endpoints": 0,
            "authentication": [],
            "middleware": [],
            "cors_config": {},
        }

        try:
            if progress_callback:
                progress_callback("Extracting API endpoints", 0.0)

            # Extract endpoints using analyzer
            api_results = await self.api_analyzer.extract_endpoints(project_path, file_structure)

            results["endpoints"] = api_results.get("endpoints", [])
            results["total_endpoints"] = len(results["endpoints"])
            results["authentication"] = api_results.get("authentication", [])
            results["middleware"] = api_results.get("middleware", [])
            results["cors_config"] = api_results.get("cors_config", {})

            # Group by framework
            for endpoint in results["endpoints"]:
                framework = endpoint.get("framework", "Unknown")
                if framework not in results["by_framework"]:
                    results["by_framework"][framework] = []
                results["by_framework"][framework].append(endpoint)

            if progress_callback:
                progress_callback("API extraction complete", 1.0)

            logger.info(f"API extraction complete: {results['total_endpoints']} endpoints found")

        except Exception as e:
            logger.error(f"Error in API extraction: {e}")
            raise

        return results

    def get_cached_extraction(self, project_path: str) -> Dict[str, Any]:
        """Get cached extraction results"""
        return self.extraction_cache.get(project_path)

    def cache_extraction(self, project_path: str, results: Dict[str, Any]):
        """Cache extraction results"""
        self.extraction_cache[project_path] = results
