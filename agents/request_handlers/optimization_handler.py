"""
Optimization Request Handler - Handles optimization requests
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class OptimizationRequestHandler:
    """Handles optimization-related requests"""

    def __init__(self, model_manager, prompt_templates):
        self.model_manager = model_manager
        self.prompt_templates = prompt_templates

    async def handle_optimization_request(
        self, user_message: str, project_context: Dict[str, Any]
    ) -> str:
        """Behandelt Optimierungs-Anfragen"""
        try:
            if not project_context:
                return "❌ Kein Projekt-Kontext verfügbar. Bitte führe zuerst eine Projekt-Analyse durch."

            project_type = self._get_project_type(project_context)
            main_framework = self._get_main_framework(project_context)

            # Erstelle Optimierungsvorschläge
            prompt = self.prompt_templates.get_template(
                "optimization_suggestions",
                project_type=project_type,
                framework=main_framework,
                project_size=project_context.get("file_count", 0),
                performance_issues="Unknown",
                bundle_size="Unknown",
                load_time="Unknown",
                memory_usage="Unknown",
                cpu_usage="Unknown",
            )

            response = await self.model_manager.generate_response(prompt)
            return response

        except Exception as e:
            logger.error(f"Fehler bei Optimierungs-Anfrage: {e}")
            return f"❌ Fehler bei der Optimierungs-Analyse: {str(e)}"

    async def handle_deployment_request(
        self, user_message: str, project_context: Dict[str, Any]
    ) -> str:
        """Behandelt Deployment-Anfragen"""
        try:
            if not project_context:
                return "❌ Kein Projekt-Kontext verfügbar. Bitte führe zuerst eine Projekt-Analyse durch."

            project_type = self._get_project_type(project_context)
            main_framework = self._get_main_framework(project_context)
            database_type = self._get_database_type(project_context)

            # Erstelle Deployment-Plan
            prompt = self.prompt_templates.get_template(
                "deployment_plan",
                project_type=project_type,
                framework=main_framework,
                dependencies=str(project_context.get("dependency_count", 0)),
                database=database_type,
                environment="production",
            )

            response = await self.model_manager.generate_response(prompt)
            return response

        except Exception as e:
            logger.error(f"Fehler bei Deployment-Anfrage: {e}")
            return f"❌ Fehler bei der Deployment-Planung: {str(e)}"

    async def handle_documentation_request(
        self, user_message: str, project_context: Dict[str, Any]
    ) -> str:
        """Behandelt Dokumentations-Anfragen"""
        try:
            if not project_context:
                return "❌ Kein Projekt-Kontext verfügbar. Bitte führe zuerst eine Projekt-Analyse durch."

            project_type = self._get_project_type(project_context)
            main_framework = self._get_main_framework(project_context)

            # Erstelle Dokumentations-Plan
            prompt = self.prompt_templates.get_template(
                "documentation",
                project_name=project_context.get("project_name", "Unknown"),
                project_type=project_type,
                framework=main_framework,
                target_audience="developers",
            )

            response = await self.model_manager.generate_response(prompt)
            return response

        except Exception as e:
            logger.error(f"Fehler bei Dokumentations-Anfrage: {e}")
            return f"❌ Fehler bei der Dokumentations-Erstellung: {str(e)}"

    async def suggest_optimizations(self, project_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Schlägt Optimierungen vor"""
        optimizations = []

        try:
            if not project_context:
                return optimizations

            # Performance-Optimierungen
            if project_context.get("lines_of_code", 0) > 10000:
                optimizations.append(
                    {
                        "type": "performance",
                        "title": "Code-Splitting implementieren",
                        "description": "Bei über 10.000 Zeilen Code sollte Code-Splitting implementiert werden",
                        "priority": "high",
                        "impact": "Signifikante Verbesserung der Ladezeiten",
                    }
                )

            # Security-Optimierungen
            security_issues = project_context.get("security_issues", [])
            if security_issues:
                optimizations.append(
                    {
                        "type": "security",
                        "title": "Security-Issues beheben",
                        "description": f"{len(security_issues)} Security-Issues gefunden",
                        "priority": "high",
                        "impact": "Verbesserung der Sicherheit",
                    }
                )

            # Test-Coverage
            test_coverage = project_context.get("test_coverage", {})
            coverage_percentage = test_coverage.get("coverage_percentage", 0)
            if coverage_percentage < 80:
                optimizations.append(
                    {
                        "type": "testing",
                        "title": "Test-Coverage erhöhen",
                        "description": f"Aktuelle Coverage: {coverage_percentage}%, Ziel: 80%",
                        "priority": "medium",
                        "impact": "Verbesserung der Code-Qualität",
                    }
                )

        except Exception as e:
            logger.error(f"Fehler bei Optimierungsvorschlägen: {e}")

        return optimizations

    def _get_project_type(self, project_context: Dict[str, Any]) -> str:
        """Bestimmt den Projekttyp"""
        frameworks = project_context.get("frameworks", [])
        if not frameworks:
            return "Unknown"

        has_frontend = any(f.get("type") == "Frontend" for f in frameworks)
        has_backend = any(f.get("type") == "Backend" for f in frameworks)

        if has_frontend and has_backend:
            return "Full-Stack"
        elif has_frontend:
            return "Frontend"
        elif has_backend:
            return "Backend"
        else:
            return "Unknown"

    def _get_main_framework(self, project_context: Dict[str, Any]) -> str:
        """Gibt das Haupt-Framework zurück"""
        frameworks = project_context.get("frameworks", [])
        if frameworks:
            return frameworks[0].get("name", "Unknown")
        return "Unknown"

    def _get_database_type(self, project_context: Dict[str, Any]) -> str:
        """Gibt den Datenbank-Typ zurück"""
        database_schema = project_context.get("database_schema", {})
        return database_schema.get("database_type", "Unknown")
