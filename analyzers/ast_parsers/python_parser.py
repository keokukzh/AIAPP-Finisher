"""
Python AST Parser - Parses Python source code
"""

import ast
import logging
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class PythonParser:
    """Parses Python source code using AST"""

    async def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse a Python file and extract AST information"""
        result = {"classes": [], "functions": [], "imports": [], "complexity": 0, "lines": 0}

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                result["lines"] = len(content.splitlines())

            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    result["classes"].append(
                        {
                            "name": node.name,
                            "line": node.lineno,
                            "methods": [
                                m.name for m in node.body if isinstance(m, ast.FunctionDef)
                            ],
                        }
                    )

                elif isinstance(node, ast.FunctionDef):
                    result["functions"].append(
                        {"name": node.name, "line": node.lineno, "args": len(node.args.args)}
                    )

                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            result["imports"].append(alias.name)
                    else:
                        result["imports"].append(node.module if node.module else "relative")

            result["complexity"] = self._calculate_complexity(tree)

        except Exception as e:
            logger.debug(f"Error parsing Python file {file_path}: {e}")

        return result

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1

        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1

        return complexity
