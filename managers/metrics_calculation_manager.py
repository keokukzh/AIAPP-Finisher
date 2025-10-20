"""
Metrics Calculation Manager - Coordinates metrics calculation
Implements Manager pattern for metrics analysis
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class MetricsCalculationManager:
    """Manages and coordinates metrics calculation using composition"""

    def __init__(self, metrics_calculator):
        # Composition over inheritance - inject dependency
        self.metrics_calculator = metrics_calculator

        self.metrics_cache = {}
        self.metrics_trends = []

    async def calculate_all_metrics(
        self,
        project_path: str,
        file_structure: Dict[str, Any],
        ast_analysis: Dict[str, Any],
        progress_callback=None,
    ) -> Dict[str, Any]:
        """Coordinate complete metrics calculation"""
        results = {
            "lines_of_code": 0,
            "complexity": 0,
            "maintainability_index": 0,
            "technical_debt": 0,
            "code_quality_score": 0,
            "by_language": {},
            "by_file": [],
        }

        try:
            if progress_callback:
                progress_callback("Calculating metrics", 0.0)

            # Calculate metrics using calculator
            metrics_results = await self.metrics_calculator.calculate_metrics(
                project_path, file_structure, ast_analysis
            )

            results.update(metrics_results)

            # Calculate overall scores
            results["code_quality_score"] = self._calculate_quality_score(results)
            results["technical_debt"] = self._estimate_technical_debt(results)

            # Record trends
            self.metrics_trends.append(
                {
                    "project_path": project_path,
                    "lines_of_code": results["lines_of_code"],
                    "complexity": results["complexity"],
                    "quality_score": results["code_quality_score"],
                }
            )

            if progress_callback:
                progress_callback("Metrics calculation complete", 1.0)

            logger.info(
                f"Metrics calculated: {results['lines_of_code']} LOC, "
                f"complexity: {results['complexity']}, "
                f"quality score: {results['code_quality_score']}"
            )

        except Exception as e:
            logger.error(f"Error calculating metrics: {e}")
            raise

        return results

    def _calculate_quality_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall code quality score"""
        score = 100.0

        # Penalize high complexity
        complexity = metrics.get("complexity", 0)
        if complexity > 50:
            score -= min(30, (complexity - 50) * 0.5)

        # Penalize low maintainability
        maintainability = metrics.get("maintainability_index", 100)
        if maintainability < 70:
            score -= (70 - maintainability) * 0.3

        return max(0, min(100, score))

    def _estimate_technical_debt(self, metrics: Dict[str, Any]) -> float:
        """Estimate technical debt in hours"""
        loc = metrics.get("lines_of_code", 0)
        complexity = metrics.get("complexity", 0)

        # Simple estimation: complex code takes longer to refactor
        debt = (complexity / 10) * (loc / 1000) * 2

        return round(debt, 2)

    def get_cached_metrics(self, project_path: str) -> Dict[str, Any]:
        """Get cached metrics"""
        return self.metrics_cache.get(project_path)

    def cache_metrics(self, project_path: str, results: Dict[str, Any]):
        """Cache metrics"""
        self.metrics_cache[project_path] = results

    def get_metrics_trends(self) -> List[Dict[str, Any]]:
        """Get metrics trends"""
        return self.metrics_trends
