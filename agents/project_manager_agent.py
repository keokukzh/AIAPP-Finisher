"""
KI-Projektmanager Agent - Hauptintelligenz des Systems
Refactored to use specialized intent analyzer and request handlers
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from llm.model_manager import ModelManager
from llm.prompt_templates import PromptTemplates

from .intent_analyzer import IntentAnalyzer
from .request_handlers import AnalysisRequestHandler, OptimizationRequestHandler

logger = logging.getLogger(__name__)


class ProjectManagerAgent:
    """AI project manager agent coordinating analysis and optimization.

    Coordinates intent analysis and request handling across analysis and
    optimization domains. Maintains minimal in-memory state for the
    current project and recent conversation history.

    Attributes:
        model_manager: Interface for interacting with the active LLM provider.
        prompt_templates: Reusable prompt templates for agent interactions.
        intent_analyzer: Analyzer that infers user intent from messages.
        analysis_handler: Handles analysis-related requests.
        optimization_handler: Handles optimization-related requests.
        status: Current lifecycle status string (initialized/ready/error/... ).
        current_project: Current project name or identifier.
        project_context: Dictionary of the latest analysis results and metadata.
        conversation_history: List of chat message records for context.
        active_tasks: List of currently running task identifiers.
        completed_tasks: List of completed task identifiers.
        capabilities: List of supported high-level capabilities.
    """

    def __init__(self, model_manager: ModelManager) -> None:
        """Initialize agent dependencies and state.

        Args:
            model_manager: Configured `ModelManager` instance to use for LLM calls.
        """
        self.model_manager = model_manager
        self.prompt_templates = PromptTemplates()

        # Initialize specialized components
        self.intent_analyzer = IntentAnalyzer()
        self.analysis_handler = AnalysisRequestHandler(model_manager, self.prompt_templates)
        self.optimization_handler = OptimizationRequestHandler(model_manager, self.prompt_templates)

        # Agent-Status
        self.status = "initialized"
        self.current_project = None
        self.project_context = {}
        self.conversation_history = []
        self.active_tasks = []
        self.completed_tasks = []

        # Agent-Fähigkeiten
        self.capabilities = [
            "project_analysis",
            "code_review",
            "optimization_suggestions",
            "test_generation",
            "documentation",
            "security_analysis",
            "deployment_planning",
            "chat_support",
        ]

    async def initialize(self) -> None:
        """Initialize underlying services and set agent ready state.

        Raises:
            Exception: Propagates exceptions from underlying model manager initialization.
        """
        try:
            await self.model_manager.initialize()
            self.status = "ready"
            logger.info("KI-Projektmanager Agent initialisiert")

        except Exception as e:
            self.status = "error"
            logger.error(f"Fehler bei der Agent-Initialisierung: {e}")
            raise

    async def set_project_context(self, project_analysis: Dict[str, Any]) -> None:
        """Set current project context and compute a lightweight summary.

        Args:
            project_analysis: Aggregated analysis results and metadata for the project.

        Raises:
            Exception: Propagates if summary creation fails unexpectedly.
        """
        try:
            self.current_project = project_analysis.get("project_name", "Unknown")
            self.project_context = project_analysis

            # Erstelle Projekt-Zusammenfassung
            project_summary = await self._create_project_summary(project_analysis)
            self.project_context["summary"] = project_summary

            logger.info(f"Projekt-Kontext gesetzt: {self.current_project}")

        except Exception as e:
            logger.error(f"Fehler beim Setzen des Projekt-Kontexts: {e}")
            raise

    async def chat(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Handle a chat message and return the assistant response.

        Args:
            user_message: The raw user message.
            context: Optional contextual data to augment routing/handlers.

        Returns:
            Assistant response string.
        """
        try:
            # Füge Nachricht zur Historie hinzu
            self.conversation_history.append(
                {"role": "user", "message": user_message, "timestamp": datetime.now().isoformat()}
            )

            # Analysiere User-Intent via IntentAnalyzer
            intent = await self.intent_analyzer.analyze_intent(user_message)

            # Route to appropriate handler based on intent
            response = await self._route_request(intent, user_message, context)

            # Füge Antwort zur Historie hinzu
            self.conversation_history.append(
                {
                    "role": "assistant",
                    "message": response,
                    "timestamp": datetime.now().isoformat(),
                    "intent": intent,
                }
            )

            return response

        except Exception as e:
            logger.error(f"Fehler beim Chat: {e}")
            return f"❌ Entschuldigung, es ist ein Fehler aufgetreten: {str(e)}"

    async def _route_request(
        self, intent: Dict[str, Any], user_message: str, context: Optional[Dict[str, Any]]
    ) -> str:
        """Route a request to the appropriate handler based on inferred intent.

        Args:
            intent: Intent dictionary produced by the intent analyzer.
            user_message: Original user message.
            context: Optional additional context.

        Returns:
            Handler response string.
        """
        intent_type = intent["type"]

        # Analysis-related intents
        if intent_type == "project_analysis":
            return await self.analysis_handler.handle_project_analysis(
                user_message, self.project_context
            )
        elif intent_type == "testing":
            return await self.analysis_handler.handle_testing_request(
                user_message, self.project_context
            )
        elif intent_type == "security":
            return await self.analysis_handler.handle_security_request(
                user_message, self.project_context
            )
        elif intent_type == "code_review":
            return await self.analysis_handler.handle_code_review_request(user_message, context)

        # Optimization-related intents
        elif intent_type == "optimization":
            return await self.optimization_handler.handle_optimization_request(
                user_message, self.project_context
            )
        elif intent_type == "deployment":
            return await self.optimization_handler.handle_deployment_request(
                user_message, self.project_context
            )
        elif intent_type == "documentation":
            return await self.optimization_handler.handle_documentation_request(
                user_message, self.project_context
            )

        # General chat
        else:
            return await self._handle_general_chat(user_message, context)

    async def _handle_general_chat(
        self, user_message: str, context: Optional[Dict[str, Any]]
    ) -> str:
        """Handle general chat requests with a templated response.

        Args:
            user_message: The user's free-form chat input.
            context: Optional contextual data to enrich the response.

        Returns:
            Generated assistant response string.
        """
        try:
            # Erstelle allgemeine Chat-Antwort
            prompt = self.prompt_templates.get_template(
                "chat_response",
                project_name=(
                    self.project_context.get("project_name", "Unknown")
                    if self.project_context
                    else "Kein Projekt geladen"
                ),
                project_type=self._get_project_type() if self.project_context else "Unknown",
                framework=self._get_main_framework() if self.project_context else "Unknown",
                project_status="Analysiert" if self.project_context else "Nicht analysiert",
                user_message=user_message,
                analysis_available="Ja" if self.project_context else "Nein",
                test_status="Unbekannt",
                deployment_status="Unbekannt",
                optimizations_available="Ja" if self.project_context else "Nein",
            )

            response = await self.model_manager.generate_response(prompt)
            return response

        except Exception as e:
            logger.error(f"Fehler bei allgemeinem Chat: {e}")
            return f"❌ Fehler bei der Chat-Antwort: {str(e)}"

    async def _create_project_summary(self, project_analysis: Dict[str, Any]) -> str:
        """Create a concise project summary from analysis results.

        Args:
            project_analysis: Aggregated analysis dictionary for the project.

        Returns:
            Multi-line markdown string with key project highlights.
        """
        try:
            summary_parts = []

            summary_parts.append(f"**Projekt:** {project_analysis.get('project_name', 'Unknown')}")
            summary_parts.append(f"**Dateien:** {project_analysis.get('file_count', 0)}")
            summary_parts.append(f"**Zeilen Code:** {project_analysis.get('lines_of_code', 0):,}")

            languages = project_analysis.get("languages", [])
            if languages:
                summary_parts.append(f"**Sprachen:** {', '.join(languages[:3])}")

            frameworks = project_analysis.get("frameworks", [])
            if frameworks:
                framework_names = [f["name"] for f in frameworks[:3]]
                summary_parts.append(f"**Frameworks:** {', '.join(framework_names)}")

            dependency_count = project_analysis.get("dependency_count", 0)
            if dependency_count > 0:
                summary_parts.append(f"**Dependencies:** {dependency_count}")

            return "\n".join(summary_parts)

        except Exception as e:
            logger.error(f"Fehler bei der Projekt-Zusammenfassung: {e}")
            return "Projekt-Zusammenfassung konnte nicht erstellt werden"

    def _get_project_type(self) -> str:
        """Determine project type from detected frameworks.

        Returns:
            One of: "Full-Stack", "Frontend", "Backend", or "Unknown".
        """
        if not self.project_context:
            return "Unknown"

        frameworks = self.project_context.get("frameworks", [])
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

    def _get_main_framework(self) -> str:
        """Return the primary framework name if available.

        Returns:
            Framework name string, or "Unknown" when not detected.
        """
        if not self.project_context:
            return "Unknown"

        frameworks = self.project_context.get("frameworks", [])
        if frameworks:
            return frameworks[0].get("name", "Unknown")

        return "Unknown"

    async def suggest_optimizations(self) -> List[Dict[str, Any]]:
        """Return prioritized optimization suggestions for the current project.

        Returns:
            List of suggestion dictionaries provided by the optimization handler.
        """
        return await self.optimization_handler.suggest_optimizations(self.project_context)

    async def get_status(self) -> Dict[str, Any]:
        """Return a snapshot of the agent's current status and metadata.

        Returns:
            Dictionary containing status, project info, capabilities, counters and model info.
        """
        return {
            "status": self.status,
            "current_project": self.current_project,
            "capabilities": self.capabilities,
            "conversation_count": len(self.conversation_history),
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "model_info": self.model_manager.get_current_model(),
        }

    async def cleanup(self) -> None:
        """Cleanup underlying services and update lifecycle status.

        Raises:
            Exception: Propagates exceptions from underlying cleanup operations.
        """
        try:
            await self.model_manager.cleanup()
            self.status = "cleaned_up"
            logger.info("KI-Projektmanager Agent bereinigt")

        except Exception as e:
            logger.error(f"Fehler bei der Bereinigung: {e}")
