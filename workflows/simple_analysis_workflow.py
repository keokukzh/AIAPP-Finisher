"""
Einfacher Analyse-Workflow - nur Projekt-Analyse
"""

import logging
from typing import Any, Dict

from analyzers.project_analyzer import ProjectAnalyzer
from workflows.base_workflow import BaseWorkflow

logger = logging.getLogger(__name__)


class SimpleAnalysisWorkflow(BaseWorkflow):
    """Einfacher Workflow nur für Projekt-Analyse"""

    def __init__(self):
        super().__init__(
            name="simple_analysis",
            description="Einfache Projekt-Analyse ohne Agent/Skill-Generierung",
        )
        self.project_analyzer = ProjectAnalyzer()

        # Nur einen Schritt: Projekt-Analyse
        self.add_step("analyze_project", self._analyze_project)

    async def execute(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the simple analysis workflow"""
        if not context or "project_path" not in context:
            raise ValueError("Project path is required in context")

        self.status = "running"
        project_path = context["project_path"]

        try:
            # Nur Projekt-Analyse
            analysis_results = await self.run_step(
                "analyze_project", {"project_path": project_path}
            )

            # Workflow abgeschlossen
            self.status = "completed"
            self.results = {
                "analysis": analysis_results,
                "workflow_status": "completed",
                "phases": self.results.get("phases", []),
            }

            logger.info("✅ Simple analysis workflow completed successfully")
            return self.results

        except Exception as e:
            self.status = "failed"
            logger.error(f"❌ Simple analysis workflow failed: {e}")
            raise

    async def _analyze_project(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the project structure and content"""
        project_path = context["project_path"]

        # Progress callback für Live-Updates
        async def progress_callback(message: str, percentage: int, details: Dict = None):
            self._update_phase_status("analyze_project", "running", percentage, details)

        return await self.project_analyzer.analyze_project(project_path, progress_callback)
