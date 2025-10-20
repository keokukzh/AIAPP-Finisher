"""
FastAPI Endpoint Extractor
"""

import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class FastAPIExtractor:
    """Extracts FastAPI endpoints"""

    async def extract_endpoints(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extrahiert FastAPI-Endpoints"""
        endpoints = []

        try:
            # Finde @app. und @router. Decorators
            decorator_pattern = r'@(?:app|router)\.(\w+)\s*\(\s*["\']([^"\']+)["\']'
            decorator_matches = re.finditer(decorator_pattern, content)

            for match in decorator_matches:
                method = match.group(1).upper()
                path = match.group(2)

                # Finde die zugehörige Funktion
                func_pattern = rf'@(?:app|router)\.{match.group(1)}\s*\(\s*["\'][^"\']+["\']\s*\)\s*\n(?:async\s+)?def\s+(\w+)\s*\('
                func_match = re.search(func_pattern, content, re.MULTILINE)
                function_name = func_match.group(1) if func_match else "unknown"

                endpoints.append(
                    {
                        "path": path,
                        "method": method,
                        "function_name": function_name,
                        "framework": "FastAPI",
                        "file_path": file_path,
                        "parameters": await self._extract_parameters(content, function_name),
                        "response_model": await self._extract_response_model(
                            content, function_name
                        ),
                    }
                )

        except Exception as e:
            logger.error(f"Fehler bei FastAPI-Endpoint-Extraktion: {e}")

        return endpoints

    async def _extract_parameters(self, content: str, function_name: str) -> List[Dict[str, Any]]:
        """Extrahiert FastAPI-Parameter"""
        parameters = []

        try:
            # Finde die Funktion
            func_pattern = rf"(?:async\s+)?def\s+{function_name}\s*\(([^)]+)\)"
            func_match = re.search(func_pattern, content)

            if func_match:
                params_str = func_match.group(1)
                param_list = [p.strip() for p in params_str.split(",")]

                for param in param_list:
                    if ":" in param:
                        name, type_hint = param.split(":", 1)
                        name = name.strip()
                        type_hint = type_hint.strip()

                        parameters.append(
                            {
                                "name": name,
                                "type": type_hint,
                                "required": "Optional" not in type_hint,
                            }
                        )

        except Exception as e:
            logger.debug(f"Fehler bei FastAPI-Parameter-Extraktion: {e}")

        return parameters

    async def _extract_response_model(self, content: str, function_name: str) -> str:
        """Extrahiert FastAPI-Response-Model"""
        try:
            # Finde Response-Model in der Funktion
            response_pattern = rf"def\s+{function_name}.*?->\s*(\w+)"
            response_match = re.search(response_pattern, content, re.DOTALL)

            if response_match:
                return response_match.group(1)

        except Exception as e:
            logger.debug(f"Fehler bei FastAPI-Response-Model-Extraktion: {e}")

        return None
