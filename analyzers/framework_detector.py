"""Framework detection module for project analysis.

This module provides the FrameworkDetector class which coordinates specialized
frontend and backend detectors to identify all frameworks and libraries used
in a project. Supports detection of 20+ popular frameworks including React,
Vue, Django, Flask, FastAPI, and more.

Typical usage example:
    detector = FrameworkDetector()
    frameworks = await detector.detect_frameworks(
        "/path/to/project",
        file_structure_data
    )
    print(f"Found {len(frameworks)} frameworks")

Classes:
    FrameworkDetector: Main coordinator for framework detection operations.
"""

import logging
from typing import Any, Dict, List

from .framework_detectors import BackendDetector, FrontendDetector

logger = logging.getLogger(__name__)


class FrameworkDetector:
    """Coordinates framework detection across frontend and backend technologies.

    Delegates detection to specialized FrontendDetector and BackendDetector
    instances, aggregating results into a unified framework list. Each detector
    analyzes project files, dependencies, and configuration to identify frameworks.

    Attributes:
        frontend_detector: Detector for frontend frameworks (React, Vue, Angular, etc.).
        backend_detector: Detector for backend frameworks (Django, Flask, FastAPI, etc.).
    """

    def __init__(self) -> None:
        """Initialize FrameworkDetector with specialized detectors.

        Creates instances of FrontendDetector and BackendDetector for
        comprehensive framework analysis.
        """
        self.frontend_detector = FrontendDetector()
        self.backend_detector = BackendDetector()

    async def detect_frameworks(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Detect all frameworks used in the project.

        Coordinates frontend and backend framework detection by delegating
        to specialized detectors. Aggregates all detected frameworks into
        a single list with metadata.

        Args:
            project_path: Absolute path to project root directory.
            file_structure: Dictionary containing project file structure with
                keys 'all_files', 'directories', and 'file_types'.

        Returns:
            List of dictionaries, each containing framework information:
                - name: Framework name (e.g., 'React', 'FastAPI')
                - type: Category ('Frontend' or 'Backend')
                - version: Detected version string (if available)
                - confidence: Detection confidence level (if available)

        Example:
            >>> detector = FrameworkDetector()
            >>> frameworks = await detector.detect_frameworks(
            ...     "/path/to/project",
            ...     {"all_files": [...], "directories": [...]}
            ... )
            >>> print(frameworks[0]['name'])
            'FastAPI'

        Note:
            Returns empty list if detection fails. Errors are logged but not raised.
        """
        detected_frameworks = []

        try:
            # Detect frontend frameworks
            frontend = await self.frontend_detector.detect(project_path, file_structure)
            detected_frameworks.extend(frontend)

            # Detect backend frameworks
            backend = await self.backend_detector.detect(project_path, file_structure)
            detected_frameworks.extend(backend)

            logger.info(f"Detected {len(detected_frameworks)} frameworks")

        except Exception as e:
            logger.error(f"Error detecting frameworks: {e}")

        return detected_frameworks
