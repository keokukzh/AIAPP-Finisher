"""
Analysis Request Handler - Handles project analysis requests
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class AnalysisRequestHandler:
    """Handles analysis-related requests"""

    def __init__(self, model_manager, prompt_templates):
        self.model_manager = model_manager
        self.prompt_templates = prompt_templates

    async def handle_project_analysis(
        self, user_message: str, project_context: Dict[str, Any]
    ) -> str:
        """Behandelt Projekt-Analyse-Anfragen"""
        try:
            if not project_context:
                return "❌ Kein Projekt-Kontext verfügbar. Bitte führe zuerst eine Projekt-Analyse durch."

            # Erstelle detaillierte Projekt-Analyse
            prompt = self.prompt_templates.get_template(
                "project_analysis",
                project_name=project_context.get("project_name", "Unknown"),
                project_path=project_context.get("project_path", "Unknown"),
                file_count=project_context.get("file_count", 0),
                lines_of_code=project_context.get("lines_of_code", 0),
                dependency_count=project_context.get("dependency_count", 0),
                technologies=", ".join(project_context.get("languages", [])),
                frameworks=", ".join([f["name"] for f in project_context.get("frameworks", [])]),
                api_endpoints=str(len(project_context.get("api_endpoints", []))),
                database_schema=str(
                    len(project_context.get("database_schema", {}).get("tables", []))
                ),
            )

            response = await self.model_manager.generate_response(prompt)
            return response

        except Exception as e:
            logger.error(f"Fehler bei Projekt-Analyse: {e}")
            return f"❌ Fehler bei der Projekt-Analyse: {str(e)}"

    async def handle_testing_request(
        self, user_message: str, project_context: Dict[str, Any]
    ) -> str:
        """Behandelt Testing-Anfragen"""
        try:
            if not project_context:
                return "❌ Kein Projekt-Kontext verfügbar. Bitte führe zuerst eine Projekt-Analyse durch."

            frameworks = project_context.get("frameworks", [])
            main_framework = frameworks[0].get("name") if frameworks else "Unknown"

            test_coverage = project_context.get("test_coverage", {})
            test_frameworks = test_coverage.get("test_frameworks", [])
            test_framework = test_frameworks[0] if test_frameworks else "pytest"

            languages = project_context.get("languages", [])
            main_language = languages[0] if languages else "Unknown"

            # Erstelle Test-Strategie
            prompt = self.prompt_templates.get_template(
                "test_generation",
                framework=main_framework,
                test_framework=test_framework,
                language=main_language,
                current_coverage=test_coverage.get("coverage_percentage", 0),
                components=", ".join([f["name"] for f in frameworks]),
            )

            response = await self.model_manager.generate_response(prompt)
            return response

        except Exception as e:
            logger.error(f"Fehler bei Testing-Anfrage: {e}")
            return f"❌ Fehler bei der Test-Generierung: {str(e)}"

    async def handle_security_request(
        self, user_message: str, project_context: Dict[str, Any]
    ) -> str:
        """Behandelt Security-Anfragen"""
        try:
            if not project_context:
                return "❌ Kein Projekt-Kontext verfügbar. Bitte führe zuerst eine Projekt-Analyse durch."

            frameworks = project_context.get("frameworks", [])
            project_type = (
                "Full-Stack"
                if len(frameworks) > 1
                else frameworks[0].get("type", "Unknown") if frameworks else "Unknown"
            )
            main_framework = frameworks[0].get("name") if frameworks else "Unknown"

            # Erstelle Security-Analyse
            vulnerabilities = project_context.get("security_issues", [])
            vulnerabilities_str = "\n".join(
                [f"- {v.get('message', 'Unknown')}" for v in vulnerabilities]
            )

            prompt = self.prompt_templates.get_template(
                "security_analysis",
                project_type=project_type,
                framework=main_framework,
                dependency_count=project_context.get("dependency_count", 0),
                api_count=len(project_context.get("api_endpoints", [])),
                vulnerabilities=vulnerabilities_str,
            )

            response = await self.model_manager.generate_response(prompt)
            return response

        except Exception as e:
            logger.error(f"Fehler bei Security-Anfrage: {e}")
            return f"❌ Fehler bei der Security-Analyse: {str(e)}"

    async def handle_code_review_request(
        self, user_message: str, context: Optional[Dict[str, Any]]
    ) -> str:
        """Behandelt Code-Review-Anfragen"""
        try:
            # Für Code-Review brauchen wir spezifischen Code
            if not context or "code" not in context:
                return """
                🔍 **Code-Review-Anfrage**
                
                Um einen Code-Review durchzuführen, brauche ich:
                - Den Code, der überprüft werden soll
                - Die Datei/Dateiname
                - Den Kontext (Funktion, Klasse, etc.)
                
                Bitte teile den Code mit mir, dann kann ich eine detaillierte Analyse durchführen.
                """

            # Erstelle Code-Review
            prompt = self.prompt_templates.get_template(
                "code_review",
                file_path=context.get("file_path", "Unknown"),
                function_name=context.get("function_name", "Unknown"),
                framework=context.get("framework", "Unknown"),
                language=context.get("language", "Unknown"),
                code=context.get("code", ""),
            )

            response = await self.model_manager.generate_response(prompt)
            return response

        except Exception as e:
            logger.error(f"Fehler bei Code-Review-Anfrage: {e}")
            return f"❌ Fehler beim Code-Review: {str(e)}"
