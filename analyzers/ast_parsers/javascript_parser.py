"""
JavaScript AST Parser - Parses JavaScript/TypeScript source code
"""

import logging
import re
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class JavaScriptParser:
    """Parses JavaScript/TypeScript source code"""

    async def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse a JavaScript/TypeScript file"""
        result = {"classes": [], "functions": [], "imports": [], "complexity": 0, "lines": 0}

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                result["lines"] = len(content.splitlines())

            # Extract classes
            class_pattern = r"class\s+(\w+)"
            for match in re.finditer(class_pattern, content):
                result["classes"].append(
                    {"name": match.group(1), "line": content[: match.start()].count("\n") + 1}
                )

            # Extract functions
            function_patterns = [
                r"function\s+(\w+)\s*\(",
                r"const\s+(\w+)\s*=\s*(?:async\s*)?\(",
                r"(\w+)\s*:\s*(?:async\s*)?function",
            ]

            for pattern in function_patterns:
                for match in re.finditer(pattern, content):
                    result["functions"].append(
                        {"name": match.group(1), "line": content[: match.start()].count("\n") + 1}
                    )

            # Extract imports
            import_patterns = [
                r'import\s+.*?\s+from\s+["\']([^"\']+)["\']',
                r'require\(["\']([^"\']+)["\']\)',
            ]

            for pattern in import_patterns:
                for match in re.finditer(pattern, content):
                    result["imports"].append(match.group(1))

            result["complexity"] = self._calculate_complexity(content)

        except Exception as e:
            logger.debug(f"Error parsing JavaScript file {file_path}: {e}")

        return result

    def _calculate_complexity(self, content: str) -> int:
        """Calculate approximate cyclomatic complexity"""
        complexity = 1

        # Count control flow statements
        control_keywords = ["if", "else if", "while", "for", "case", "catch"]
        for keyword in control_keywords:
            complexity += len(re.findall(rf"\b{keyword}\b", content))

        # Count logical operators
        complexity += len(re.findall(r"\&\&|\|\|", content))

        return complexity
