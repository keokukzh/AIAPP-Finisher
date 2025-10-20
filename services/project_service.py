"""
Project Service for KI-Projektmanagement-System
Contains business logic for project analysis and management
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ProjectService:
    """Service class for project-related operations"""

    def __init__(self, project_analyzer, model_manager):
        self.project_analyzer = project_analyzer
        self.model_manager = model_manager
        self.current_project: Optional[str] = None
        self.analysis_results: Optional[Dict[str, Any]] = None

    async def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """
        Analyzes a project and returns the results

        Args:
            project_path: Path to the project directory

        Returns:
            Dictionary containing analysis results
        """
        try:
            logger.info(f"🔍 Starting analysis of {project_path}")

            # Validate project path
            if not Path(project_path).exists():
                raise ValueError(f"Project path does not exist: {project_path}")

            # Perform analysis
            self.analysis_results = self.project_analyzer.analyze(project_path)
            self.current_project = project_path

            logger.info(f"✅ Analysis completed for {project_path}")

            return self.analysis_results

        except Exception as e:
            logger.error(f"❌ Error during project analysis: {e}")
            raise

    def get_analysis_results(self) -> Optional[Dict[str, Any]]:
        """Returns the current analysis results"""
        return self.analysis_results

    def get_current_project(self) -> Optional[str]:
        """Returns the current project path"""
        return self.current_project

    def clear_analysis(self):
        """Clears the current analysis results"""
        self.analysis_results = None
        self.current_project = None
        logger.info("🗑️ Analysis results cleared")
