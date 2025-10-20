"""API endpoint extraction module for REST API analysis.

This module provides the APIAnalyzer class which extracts API endpoints,
authentication methods, middleware configurations, and OpenAPI specifications
from projects using various API frameworks (FastAPI, Flask, Django, Express.js,
NestJS, Spring Boot).

Coordinates specialized framework extractors to provide comprehensive API
documentation and analysis.

Typical usage example:
    analyzer = APIAnalyzer()
    api_info = await analyzer.extract_endpoints(
        "/path/to/project",
        file_structure_data
    )
    print(f"Found {len(api_info['endpoints'])} API endpoints")

Classes:
    APIAnalyzer: Main coordinator for API endpoint extraction and analysis.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from .api_extractors import (
    DjangoExtractor,
    ExpressExtractor,
    FastAPIExtractor,
    FlaskExtractor,
    NestJSExtractor,
    SpringBootExtractor,
)

logger = logging.getLogger(__name__)


class APIAnalyzer:
    """Coordinates API endpoint extraction across multiple frameworks.

    Delegates extraction to specialized framework extractors for FastAPI, Flask,
    Django, Express.js, NestJS, and Spring Boot. Analyzes authentication,
    middleware, CORS configuration, and OpenAPI specifications.

    Attributes:
        api_patterns: Mapping of framework names to import patterns and extractors.
        http_methods: Set of standard HTTP method names.
        openapi_patterns: Patterns for detecting OpenAPI/Swagger specifications.
    """

    def __init__(self) -> None:
        """Initialize APIAnalyzer with framework extractors and patterns.

        Creates instances of specialized extractors for each supported API framework
        and defines detection patterns for frameworks, HTTP methods, and OpenAPI specs.
        """
        self.api_patterns = {
            "FastAPI": {"imports": ["fastapi", "from fastapi"], "extractor": FastAPIExtractor()},
            "Flask": {"imports": ["flask", "from flask"], "extractor": FlaskExtractor()},
            "Django": {
                "imports": ["django.urls", "from django.urls"],
                "extractor": DjangoExtractor(),
            },
            "Express.js": {"imports": ["express", "from express"], "extractor": ExpressExtractor()},
            "NestJS": {"imports": ["@nestjs", "from @nestjs"], "extractor": NestJSExtractor()},
            "Spring Boot": {
                "imports": ["org.springframework", "from org.springframework"],
                "extractor": SpringBootExtractor(),
            },
        }

        self.http_methods = {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"}

        self.openapi_patterns = {
            "swagger": ["swagger", "openapi", "swagger-ui"],
            "openapi_spec": ["openapi.json", "swagger.json", "api-docs.json"],
        }

    async def extract_endpoints(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract all API endpoints and metadata from the project.

        Performs comprehensive API analysis including framework detection, endpoint
        extraction, authentication analysis, middleware identification, CORS
        configuration extraction, and OpenAPI spec parsing.

        Args:
            project_path: Absolute path to project root directory.
            file_structure: Dictionary containing project file structure with
                'all_files' key listing all project files.

        Returns:
            Dictionary containing complete API analysis:
                - endpoints: List of endpoint definitions with methods, paths, handlers
                - api_framework: Detected API framework name (or None)
                - base_url: Base URL/prefix for the API
                - authentication: List of authentication methods (JWT, OAuth, etc.)
                - middleware: List of middleware functions/classes
                - openapi_spec: Parsed OpenAPI/Swagger specification (or None)
                - documentation: List of API documentation file paths
                - rate_limiting: List of rate limiting configurations
                - cors_config: CORS configuration dictionary

        Example:
            >>> analyzer = APIAnalyzer()
            >>> api_info = await analyzer.extract_endpoints(
            ...     "/path/to/project",
            ...     {"all_files": [{"path": "app.py", "extension": ".py"}, ...]}
            ... )
            >>> print(f"Framework: {api_info['api_framework']}")
            'FastAPI'
            >>> print(f"Endpoints: {len(api_info['endpoints'])}")
            25

        Note:
            Returns API structure with empty lists if extraction fails.
            Errors are logged but not raised.
        """
        api_info = {
            "endpoints": [],
            "api_framework": None,
            "base_url": None,
            "authentication": [],
            "middleware": [],
            "openapi_spec": None,
            "documentation": [],
            "rate_limiting": [],
            "cors_config": None,
        }

        try:
            # 1. Erkenne API-Framework
            api_framework = await self._detect_api_framework(project_path, file_structure)
            api_info["api_framework"] = api_framework

            # 2. Extrahiere Endpoints basierend auf Framework
            if api_framework:
                endpoints = await self._extract_framework_endpoints(
                    project_path, file_structure, api_framework
                )
                api_info["endpoints"] = endpoints

            # 3. Extrahiere OpenAPI/Swagger-Spezifikation
            openapi_spec = await self._extract_openapi_spec(project_path, file_structure)
            api_info["openapi_spec"] = openapi_spec

            # 4. Analysiere Authentifizierung
            authentication = await self._analyze_authentication(project_path, file_structure)
            api_info["authentication"] = authentication

            # 5. Analysiere Middleware
            middleware = await self._analyze_middleware(project_path, file_structure)
            api_info["middleware"] = middleware

            # 6. Analysiere CORS-Konfiguration
            cors_config = await self._analyze_cors_config(project_path, file_structure)
            api_info["cors_config"] = cors_config

            # 7. Finde API-Dokumentation
            documentation = await self._find_api_documentation(project_path, file_structure)
            api_info["documentation"] = documentation

            logger.info(
                f"Extrahiert: {len(api_info['endpoints'])} Endpoints, Framework: {api_framework}"
            )
            return api_info

        except Exception as e:
            logger.error(f"Fehler bei der API-Extraktion: {e}")
            return api_info

    async def _detect_api_framework(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> Optional[str]:
        """Detect the API framework used in the project.

        Args:
            project_path: Absolute path to project root directory.
            file_structure: Dictionary containing 'all_files' with file metadata.

        Returns:
            Name of detected API framework, or None if no framework detected.
        """
        try:
            all_files = file_structure.get("all_files", [])

            for file_info in all_files:
                if file_info["extension"].lower() in {".py", ".js", ".ts", ".java"}:
                    file_path = Path(project_path) / file_info["path"]

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                            for framework_name, framework_info in self.api_patterns.items():
                                if "imports" in framework_info:
                                    for import_pattern in framework_info["imports"]:
                                        if import_pattern in content:
                                            return framework_name

                    except Exception:
                        continue

            return None

        except Exception as e:
            logger.error(f"Fehler bei der API-Framework-Erkennung: {e}")
            return None

    async def _extract_framework_endpoints(
        self, project_path: str, file_structure: Dict[str, Any], api_framework: str
    ) -> List[Dict[str, Any]]:
        """Extrahiert Endpoints basierend auf dem erkannten Framework"""
        endpoints = []

        try:
            all_files = file_structure.get("all_files", [])
            framework_info = self.api_patterns.get(api_framework, {})
            extractor = framework_info.get("extractor")

            if not extractor:
                return endpoints

            for file_info in all_files:
                if file_info["extension"].lower() in {".py", ".js", ".ts", ".java"}:
                    file_path = Path(project_path) / file_info["path"]

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                            # Prüfe ob API-Imports vorhanden sind
                            if "imports" in framework_info:
                                has_imports = any(
                                    imp in content for imp in framework_info["imports"]
                                )
                                if not has_imports:
                                    continue

                            # Delegiere Extraktion an spezialisierten Extractor
                            file_endpoints = await extractor.extract_endpoints(
                                content, file_info["path"]
                            )
                            endpoints.extend(file_endpoints)

                    except Exception as e:
                        logger.debug(f"Fehler beim Lesen von {file_path}: {e}")
                        continue

            return endpoints

        except Exception as e:
            logger.error(f"Fehler bei der Endpoint-Extraktion: {e}")
            return endpoints

    async def _extract_openapi_spec(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extrahiert OpenAPI/Swagger-Spezifikation"""
        openapi_spec = None

        try:
            all_files = file_structure.get("all_files", [])

            for file_info in all_files:
                file_name = file_info["path"].lower()

                # Prüfe auf OpenAPI-Spec-Dateien
                if any(pattern in file_name for pattern in self.openapi_patterns["openapi_spec"]):
                    file_path = Path(project_path) / file_info["path"]

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            if file_path.suffix.lower() == ".json":
                                openapi_spec = json.load(f)
                            else:
                                content = f.read()
                                openapi_spec = json.loads(content)

                        break

                    except Exception as e:
                        logger.debug(f"Fehler beim Lesen von OpenAPI-Spec: {e}")
                        continue

            # Prüfe auch auf Swagger-Konfiguration in Code
            if not openapi_spec:
                openapi_spec = await self._extract_swagger_config(project_path, file_structure)

        except Exception as e:
            logger.error(f"Fehler bei OpenAPI-Spec-Extraktion: {e}")

        return openapi_spec

    async def _extract_swagger_config(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extrahiert Swagger-Konfiguration aus Code"""
        swagger_config = None

        try:
            all_files = file_structure.get("all_files", [])

            for file_info in all_files:
                if file_info["extension"].lower() in {".py", ".js", ".ts"}:
                    file_path = Path(project_path) / file_info["path"]

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                            if any(
                                pattern in content.lower()
                                for pattern in self.openapi_patterns["swagger"]
                            ):
                                swagger_config = {
                                    "title": "API Documentation",
                                    "version": "1.0.0",
                                    "description": "Auto-generated API documentation",
                                    "swagger_ui": True,
                                }
                                break

                    except Exception:
                        continue

        except Exception as e:
            logger.error(f"Fehler bei Swagger-Config-Extraktion: {e}")

        return swagger_config

    async def _analyze_authentication(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analysiert Authentifizierung"""
        authentication = []

        try:
            all_files = file_structure.get("all_files", [])

            for file_info in all_files:
                if file_info["extension"].lower() in {".py", ".js", ".ts"}:
                    file_path = Path(project_path) / file_info["path"]

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read().lower()

                            auth_patterns = {
                                "jwt": ["jwt", "jsonwebtoken", "access_token"],
                                "oauth": ["oauth", "oauth2", "authorization_code"],
                                "basic": ["basic_auth", "http_basic"],
                                "session": ["session", "login", "logout"],
                                "api_key": ["api_key", "apikey", "x-api-key"],
                                "bearer": ["bearer", "bearer_token"],
                            }

                            for auth_type, patterns in auth_patterns.items():
                                if any(pattern in content for pattern in patterns):
                                    authentication.append(
                                        {
                                            "type": auth_type,
                                            "file_path": file_info["path"],
                                            "confidence": 0.8,
                                        }
                                    )

                    except Exception:
                        continue

        except Exception as e:
            logger.error(f"Fehler bei Authentifizierungs-Analyse: {e}")

        return authentication

    async def _analyze_middleware(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analysiert Middleware"""
        middleware = []

        try:
            all_files = file_structure.get("all_files", [])

            for file_info in all_files:
                if file_info["extension"].lower() in {".py", ".js", ".ts"}:
                    file_path = Path(project_path) / file_info["path"]

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read().lower()

                            middleware_patterns = {
                                "cors": ["cors", "cross-origin"],
                                "logging": ["logging", "logger", "log"],
                                "rate_limiting": ["rate_limit", "throttle", "limiter"],
                                "compression": ["compression", "gzip", "deflate"],
                                "security": ["helmet", "security", "csrf"],
                                "authentication": ["auth", "jwt", "oauth"],
                            }

                            for middleware_type, patterns in middleware_patterns.items():
                                if any(pattern in content for pattern in patterns):
                                    middleware.append(
                                        {
                                            "type": middleware_type,
                                            "file_path": file_info["path"],
                                            "confidence": 0.7,
                                        }
                                    )

                    except Exception:
                        continue

        except Exception as e:
            logger.error(f"Fehler bei Middleware-Analyse: {e}")

        return middleware

    async def _analyze_cors_config(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analysiert CORS-Konfiguration"""
        cors_config = None

        try:
            all_files = file_structure.get("all_files", [])

            for file_info in all_files:
                if file_info["extension"].lower() in {".py", ".js", ".ts"}:
                    file_path = Path(project_path) / file_info["path"]

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                            if "cors" in content.lower():
                                cors_config = {
                                    "enabled": True,
                                    "origins": ["*"],
                                    "methods": ["GET", "POST", "PUT", "DELETE"],
                                    "headers": ["Content-Type", "Authorization"],
                                }
                                break

                    except Exception:
                        continue

        except Exception as e:
            logger.error(f"Fehler bei CORS-Analyse: {e}")

        return cors_config

    async def _find_api_documentation(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Findet API-Dokumentation"""
        documentation = []

        try:
            all_files = file_structure.get("all_files", [])

            for file_info in all_files:
                file_name = file_info["path"].lower()

                if any(
                    keyword in file_name for keyword in ["api", "docs", "documentation", "readme"]
                ):
                    documentation.append(
                        {
                            "name": Path(file_info["path"]).name,
                            "path": file_info["path"],
                            "type": "documentation",
                        }
                    )

        except Exception as e:
            logger.error(f"Fehler bei Dokumentations-Suche: {e}")

        return documentation
