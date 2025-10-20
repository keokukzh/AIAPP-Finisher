"""
Context Engineer - Smart Context Selection for LLM Analysis

Based on HumanLayer's context engineering patterns.
Provides intelligent file selection and relevance scoring for optimal
LLM context window utilization.

Key features:
- Dependency graph analysis
- File importance scoring (PageRank-like)
- Token budget management
- Semantic chunking
"""

import logging
import os
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

logger = logging.getLogger(__name__)


class ContextEngineer:
    """
    Smart context selection for LLM analysis

    Analyzes project structure and dependency relationships
    to select the most relevant files within a token budget.
    """

    def __init__(self, max_tokens: int = 100000):
        """
        Initialize context engineer

        Args:
            max_tokens: Maximum tokens for LLM context
        """
        self.max_tokens = max_tokens
        self.avg_tokens_per_line = 4  # Rough estimate

    def build_analysis_context(
        self, project_path: str, focus_areas: List[str] = None
    ) -> Dict[str, Any]:
        """
        Build optimized context for LLM analysis

        Args:
            project_path: Path to project root
            focus_areas: Optional list of focus areas (e.g., ['security', 'performance'])

        Returns:
            Dict with selected files, dependency graph, and metadata
        """
        logger.info(f"🔍 Building analysis context for: {project_path}")

        # 1. Scan and index files
        all_files = self._scan_project_files(project_path)
        logger.info(f"   Found {len(all_files)} files")

        # 2. Build dependency graph
        dependency_graph = self._build_dependency_graph(all_files, project_path)
        logger.info(f"   Built dependency graph with {len(dependency_graph)} nodes")

        # 3. Score files by importance
        scored_files = self._score_files(dependency_graph, all_files, focus_areas)
        logger.info(f"   Scored {len(scored_files)} files")

        # 4. Select files within token budget
        selected = self._select_within_budget(scored_files, all_files)
        logger.info(f"   Selected {len(selected)} files (budget: {self.max_tokens} tokens)")

        # 5. Extract metadata
        metadata = self._extract_metadata(selected, project_path)

        return {
            "files": selected,
            "dependency_graph": dependency_graph,
            "metadata": metadata,
            "total_files": len(all_files),
            "selected_count": len(selected),
            "coverage_percent": (len(selected) / len(all_files) * 100) if all_files else 0,
        }

    def _scan_project_files(self, project_path: str) -> List[str]:
        """Scan project and return list of relevant files"""
        relevant_extensions = {
            ".py",
            ".js",
            ".ts",
            ".jsx",
            ".tsx",
            ".java",
            ".go",
            ".rs",
            ".c",
            ".cpp",
            ".h",
            ".hpp",
            ".cs",
            ".rb",
            ".php",
            ".swift",
            ".kt",
            ".scala",
            ".md",
            ".yaml",
            ".yml",
            ".json",
            ".toml",
        }

        ignore_dirs = {
            "node_modules",
            "__pycache__",
            ".git",
            "venv",
            "env",
            "dist",
            "build",
            ".next",
            "out",
            "target",
            "bin",
            "obj",
        }

        files = []

        try:
            for root, dirs, filenames in os.walk(project_path):
                # Filter out ignored directories
                dirs[:] = [d for d in dirs if d not in ignore_dirs]

                for filename in filenames:
                    ext = Path(filename).suffix.lower()
                    if ext in relevant_extensions:
                        file_path = os.path.join(root, filename)
                        files.append(file_path)

        except Exception as e:
            logger.error(f"❌ Error scanning files: {e}")

        return files

    def _build_dependency_graph(self, files: List[str], project_root: str) -> Dict[str, Set[str]]:
        """
        Build dependency graph from import statements

        Returns:
            Dict mapping file paths to set of files they import
        """
        graph = defaultdict(set)

        for file_path in files:
            try:
                dependencies = self._extract_dependencies(file_path, project_root)
                if dependencies:
                    graph[file_path] = dependencies
            except Exception as e:
                logger.debug(f"Could not parse dependencies for {file_path}: {e}")

        return dict(graph)

    def _extract_dependencies(self, file_path: str, project_root: str) -> Set[str]:
        """Extract import statements from file"""
        dependencies = set()

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

                # Simple regex-like extraction (can be enhanced with AST)
                lines = content.split("\n")

                for line in lines:
                    line = line.strip()

                    # Python imports
                    if line.startswith("import ") or line.startswith("from "):
                        # Extract module name
                        parts = line.split()
                        if len(parts) >= 2:
                            module = parts[1].split(".")[0]
                            dependencies.add(module)

                    # JavaScript/TypeScript imports
                    elif "import" in line and ("from" in line or "require" in line):
                        # Extract module name from quotes
                        if '"' in line or "'" in line:
                            quote_char = '"' if '"' in line else "'"
                            parts = line.split(quote_char)
                            if len(parts) >= 2:
                                module = parts[1]
                                dependencies.add(module)

        except Exception as e:
            logger.debug(f"Could not read {file_path}: {e}")

        return dependencies

    def _score_files(
        self,
        dependency_graph: Dict[str, Set[str]],
        all_files: List[str],
        focus_areas: List[str] = None,
    ) -> List[Tuple[str, float]]:
        """
        Score files by importance using PageRank-like algorithm

        Returns:
            List of (file_path, score) tuples, sorted by score descending
        """
        scores = {}

        # Initialize scores
        for file_path in all_files:
            scores[file_path] = 1.0

        # PageRank iterations
        iterations = 10
        damping = 0.85

        for _ in range(iterations):
            new_scores = {}

            for file_path in all_files:
                # Base score
                score = 1 - damping

                # Add contributions from files that import this one
                for other_file, deps in dependency_graph.items():
                    if file_path in deps or any(file_path.endswith(d) for d in deps):
                        out_degree = len(deps) if deps else 1
                        score += damping * (scores.get(other_file, 1.0) / out_degree)

                new_scores[file_path] = score

            scores = new_scores

        # Bonus for focus areas
        if focus_areas:
            for file_path in all_files:
                filename = Path(file_path).name.lower()
                for area in focus_areas:
                    if area.lower() in filename:
                        scores[file_path] *= 1.5

        # Bonus for main files
        for file_path in all_files:
            filename = Path(file_path).name.lower()
            if filename in ["main.py", "app.py", "index.js", "main.ts", "server.py"]:
                scores[file_path] *= 2.0
            elif filename.startswith("test_"):
                scores[file_path] *= 0.5  # Deprioritize tests

        # Sort by score descending
        sorted_files = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return sorted_files

    def _select_within_budget(
        self, scored_files: List[Tuple[str, float]], all_files: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Select top N files that fit within token budget

        Returns:
            List of dicts with file info: path, score, lines, estimated_tokens
        """
        selected = []
        current_tokens = 0

        for file_path, score in scored_files:
            # Estimate file size in tokens
            try:
                line_count = self._count_lines(file_path)
                estimated_tokens = line_count * self.avg_tokens_per_line

                # Check budget
                if current_tokens + estimated_tokens <= self.max_tokens:
                    selected.append(
                        {
                            "path": file_path,
                            "score": round(score, 2),
                            "lines": line_count,
                            "estimated_tokens": estimated_tokens,
                        }
                    )
                    current_tokens += estimated_tokens
                else:
                    # Budget exhausted
                    break

            except Exception as e:
                logger.debug(f"Could not process {file_path}: {e}")

        return selected

    def _count_lines(self, file_path: str) -> int:
        """Count lines in file"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return len(f.readlines())
        except:
            return 0

    def _extract_metadata(
        self, selected_files: List[Dict[str, Any]], project_root: str
    ) -> Dict[str, Any]:
        """Extract metadata from selected files"""
        total_lines = sum(f["lines"] for f in selected_files)
        total_tokens = sum(f["estimated_tokens"] for f in selected_files)

        # Extract file types
        file_types = defaultdict(int)
        for f in selected_files:
            ext = Path(f["path"]).suffix
            file_types[ext] += 1

        # Extract directories
        directories = set()
        for f in selected_files:
            rel_path = os.path.relpath(f["path"], project_root)
            directory = os.path.dirname(rel_path)
            if directory:
                directories.add(directory)

        return {
            "total_lines": total_lines,
            "total_tokens": total_tokens,
            "file_types": dict(file_types),
            "directories_covered": list(directories),
            "avg_score": (
                sum(f["score"] for f in selected_files) / len(selected_files)
                if selected_files
                else 0
            ),
        }


def get_context_engineer() -> ContextEngineer:
    """Get global context engineer instance"""
    return ContextEngineer()
