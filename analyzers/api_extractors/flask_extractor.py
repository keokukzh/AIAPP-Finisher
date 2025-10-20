"""
Flask Endpoint Extractor
"""

import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class FlaskExtractor:
    """Extracts Flask endpoints"""

    async def extract_endpoints(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extrahiert Flask-Endpoints"""
        endpoints = []

        try:
            # Finde @app.route und @blueprint.route Decorators
            route_pattern = r'@(?:app|blueprint)\.route\s*\(\s*["\']([^"\']+)["\']'
            route_matches = re.finditer(route_pattern, content)

            for match in route_matches:
                path = match.group(1)

                # Finde HTTP-Methoden
                methods_pattern = rf'@(?:app|blueprint)\.route\s*\(\s*["\'][^"\']+["\']\s*,\s*methods\s*=\s*\[([^\]]+)\]'
                methods_match = re.search(methods_pattern, content)
                methods = ["GET"]  # Default

                if methods_match:
                    methods_str = methods_match.group(1)
                    methods = [m.strip().strip("\"'") for m in methods_str.split(",")]

                # Finde die zugehörige Funktion
                func_pattern = rf'@(?:app|blueprint)\.route\s*\(\s*["\'][^"\']+["\']\s*[^)]*\)\s*\n(?:async\s+)?def\s+(\w+)\s*\('
                func_match = re.search(func_pattern, content, re.MULTILINE)
                function_name = func_match.group(1) if func_match else "unknown"

                for method in methods:
                    endpoints.append(
                        {
                            "path": path,
                            "method": method.upper(),
                            "function_name": function_name,
                            "framework": "Flask",
                            "file_path": file_path,
                            "parameters": await self._extract_parameters(content, function_name),
                        }
                    )

        except Exception as e:
            logger.error(f"Fehler bei Flask-Endpoint-Extraktion: {e}")

        return endpoints

    async def _extract_parameters(self, content: str, function_name: str) -> List[Dict[str, Any]]:
        """Extrahiert Flask-Parameter"""
        parameters = []

        try:
            # Finde die Funktion
            func_pattern = rf"(?:async\s+)?def\s+{function_name}\s*\(([^)]+)\)"
            func_match = re.search(func_pattern, content)

            if func_match:
                params_str = func_match.group(1)
                param_list = [p.strip() for p in params_str.split(",")]

                for param in param_list:
                    if param and param not in ["request", "session", "g"]:
                        parameters.append({"name": param, "type": "unknown", "required": True})

        except Exception as e:
            logger.debug(f"Fehler bei Flask-Parameter-Extraktion: {e}")

        return parameters
