"""
Graph Builder - Builds dependency graphs
"""

import logging
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


class GraphBuilder:
    """Builds dependency relationship graphs"""

    async def build_dependency_graph(self, all_dependencies: Dict[str, Any]) -> Dict[str, Any]:
        """Builds a dependency graph from parsed dependencies"""
        graph = {"nodes": [], "edges": [], "stats": {"total_packages": 0, "by_language": {}}}

        try:
            # Create nodes for each package
            all_packages = set()

            for language, deps in all_dependencies.items():
                if isinstance(deps, dict):
                    for dep_type, packages in deps.items():
                        if isinstance(packages, list):
                            for package in packages:
                                all_packages.add((package, language))
                elif isinstance(deps, list):
                    for package in deps:
                        all_packages.add((package, language))

            # Add nodes
            for package, language in all_packages:
                graph["nodes"].append({"id": package, "label": package, "language": language})

            # Update stats
            graph["stats"]["total_packages"] = len(all_packages)

            # Count by language
            language_counts = {}
            for _, language in all_packages:
                language_counts[language] = language_counts.get(language, 0) + 1
            graph["stats"]["by_language"] = language_counts

        except Exception as e:
            logger.error(f"Error building dependency graph: {e}")

        return graph

    async def analyze_dependency_tree(self, dependencies: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes dependency tree structure"""
        analysis = {
            "depth": 0,
            "circular_dependencies": [],
            "unused_dependencies": [],
            "outdated_dependencies": [],
        }

        try:
            # Basic tree analysis
            analysis["depth"] = self._calculate_max_depth(dependencies)

        except Exception as e:
            logger.error(f"Error analyzing dependency tree: {e}")

        return analysis

    def _calculate_max_depth(self, dependencies: Dict[str, Any], current_depth: int = 0) -> int:
        """Recursively calculates maximum dependency depth"""
        if not dependencies:
            return current_depth

        max_depth = current_depth

        for key, value in dependencies.items():
            if isinstance(value, dict):
                depth = self._calculate_max_depth(value, current_depth + 1)
                max_depth = max(max_depth, depth)

        return max_depth
