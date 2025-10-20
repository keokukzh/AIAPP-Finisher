"""
Framework Extractors - Django, Express.js, NestJS, Spring Boot
"""

import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class DjangoExtractor:
    """Extracts Django endpoints"""

    async def extract_endpoints(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extrahiert Django-Endpoints"""
        endpoints = []

        try:
            # Finde path() und url() Aufrufe
            path_pattern = r'path\s*\(\s*["\']([^"\']+)["\']'
            path_matches = re.finditer(path_pattern, content)

            for match in path_matches:
                path = match.group(1)

                # Finde die View-Funktion
                view_pattern = rf'path\s*\(\s*["\'][^"\']+["\']\s*,\s*([^,)]+)'
                view_match = re.search(view_pattern, content)
                view_name = view_match.group(1).strip() if view_match else "unknown"

                endpoints.append(
                    {
                        "path": path,
                        "method": "GET",
                        "function_name": view_name,
                        "framework": "Django",
                        "file_path": file_path,
                        "parameters": [],
                    }
                )

        except Exception as e:
            logger.error(f"Fehler bei Django-Endpoint-Extraktion: {e}")

        return endpoints


class ExpressExtractor:
    """Extracts Express.js endpoints"""

    async def extract_endpoints(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extrahiert Express.js-Endpoints"""
        endpoints = []

        try:
            # Finde app. und router. Methoden
            method_pattern = r'(?:app|router)\.(\w+)\s*\(\s*["\']([^"\']+)["\']'
            method_matches = re.finditer(method_pattern, content)

            for match in method_matches:
                method = match.group(1).upper()
                path = match.group(2)

                # Finde die Callback-Funktion
                callback_pattern = rf'(?:app|router)\.{match.group(1)}\s*\(\s*["\'][^"\']+["\']\s*,\s*(?:async\s+)?(?:function\s+(\w+)|(\w+)\s*=>)'
                callback_match = re.search(callback_pattern, content)
                function_name = (
                    callback_match.group(1) or callback_match.group(2)
                    if callback_match
                    else "anonymous"
                )

                endpoints.append(
                    {
                        "path": path,
                        "method": method,
                        "function_name": function_name,
                        "framework": "Express.js",
                        "file_path": file_path,
                        "parameters": await self._extract_parameters(content, function_name),
                    }
                )

        except Exception as e:
            logger.error(f"Fehler bei Express-Endpoint-Extraktion: {e}")

        return endpoints

    async def _extract_parameters(self, content: str, function_name: str) -> List[Dict[str, Any]]:
        """Extrahiert Express.js-Parameter"""
        parameters = []

        try:
            # Finde die Funktion
            func_pattern = (
                rf"(?:async\s+)?(?:function\s+{function_name}|{function_name}\s*=>)\s*\(([^)]+)\)"
            )
            func_match = re.search(func_pattern, content)

            if func_match:
                params_str = func_match.group(1)
                param_list = [p.strip() for p in params_str.split(",")]

                for param in param_list:
                    if param and param not in ["req", "res", "next"]:
                        parameters.append({"name": param, "type": "unknown", "required": True})

        except Exception as e:
            logger.debug(f"Fehler bei Express-Parameter-Extraktion: {e}")

        return parameters


class NestJSExtractor:
    """Extracts NestJS endpoints"""

    async def extract_endpoints(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extrahiert NestJS-Endpoints"""
        endpoints = []

        try:
            # Finde @Controller
            controller_pattern = r'@Controller\s*\(\s*["\']([^"\']+)["\']'
            controller_match = re.search(controller_pattern, content)
            base_path = controller_match.group(1) if controller_match else ""

            # Finde HTTP-Method Decorators
            method_pattern = r'@(\w+)\s*\(\s*["\']([^"\']+)["\']'
            method_matches = re.finditer(method_pattern, content)

            for match in method_matches:
                method = match.group(1).upper()
                path = match.group(2)

                # Kombiniere Base-Path mit Endpoint-Path
                full_path = f"{base_path}/{path}".replace("//", "/")

                # Finde die zugehörige Methode
                method_func_pattern = (
                    rf'@{match.group(1)}\s*\(\s*["\'][^"\']+["\']\s*\)\s*\n(?:async\s+)?(\w+)\s*\('
                )
                method_func_match = re.search(method_func_pattern, content, re.MULTILINE)
                function_name = method_func_match.group(1) if method_func_match else "unknown"

                endpoints.append(
                    {
                        "path": full_path,
                        "method": method,
                        "function_name": function_name,
                        "framework": "NestJS",
                        "file_path": file_path,
                        "parameters": [],
                    }
                )

        except Exception as e:
            logger.error(f"Fehler bei NestJS-Endpoint-Extraktion: {e}")

        return endpoints


class SpringBootExtractor:
    """Extracts Spring Boot endpoints"""

    async def extract_endpoints(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extrahiert Spring Boot-Endpoints"""
        endpoints = []

        try:
            # Finde @RequestMapping
            request_mapping_pattern = r'@RequestMapping\s*\(\s*["\']([^"\']+)["\']'
            request_mapping_match = re.search(request_mapping_pattern, content)
            base_path = request_mapping_match.group(1) if request_mapping_match else ""

            # Finde HTTP-Method Mappings
            method_pattern = r'@(\w+Mapping)\s*\(\s*["\']([^"\']+)["\']'
            method_matches = re.finditer(method_pattern, content)

            for match in method_matches:
                mapping_type = match.group(1)
                path = match.group(2)

                # Extrahiere HTTP-Methode aus Mapping-Typ
                method = mapping_type.replace("Mapping", "").upper()

                # Kombiniere Base-Path mit Endpoint-Path
                full_path = f"{base_path}/{path}".replace("//", "/")

                # Finde die zugehörige Methode
                method_func_pattern = rf'@{mapping_type}\s*\(\s*["\'][^"\']+["\']\s*\)\s*\n(?:public\s+)?(\w+)\s+(\w+)\s*\('
                method_func_match = re.search(method_func_pattern, content, re.MULTILINE)
                function_name = method_func_match.group(2) if method_func_match else "unknown"

                endpoints.append(
                    {
                        "path": full_path,
                        "method": method,
                        "function_name": function_name,
                        "framework": "Spring Boot",
                        "file_path": file_path,
                        "parameters": [],
                    }
                )

        except Exception as e:
            logger.error(f"Fehler bei Spring-Endpoint-Extraktion: {e}")

        return endpoints
