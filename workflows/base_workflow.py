"""
Base Workflow Class
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class BaseWorkflow(ABC):
    """Base class for all workflows"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.steps = []
        self.status = "idle"
        self.results = {}

    @abstractmethod
    async def execute(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the workflow"""
        pass

    def add_step(self, step_name: str, step_function, dependencies: List[str] = None):
        """Add a step to the workflow"""
        self.steps.append(
            {
                "name": step_name,
                "function": step_function,
                "dependencies": dependencies or [],
                "status": "pending",
            }
        )

    async def run_step(self, step_name: str, context: Dict[str, Any] = None):
        """Run a specific step with progress tracking"""
        step = next((s for s in self.steps if s["name"] == step_name), None)
        if not step:
            raise ValueError(f"Step '{step_name}' not found")

        try:
            # Update phase status to "running"
            self._update_phase_status(step_name, "running", 0, {"current_action": "Starting..."})

            step["status"] = "running"
            result = await step["function"](context or {})

            # Update phase status to "completed"
            self._update_phase_status(step_name, "completed", 100, {"current_action": "Completed"})

            step["status"] = "completed"
            return result
        except Exception as e:
            # Update phase status to "error"
            self._update_phase_status(step_name, "error", 0, {"current_action": f"Error: {str(e)}"})

            step["status"] = "failed"
            logger.error(f"Step '{step_name}' failed: {e}")
            raise

    def _update_phase_status(
        self, phase_name: str, status: str, progress: int, details: Dict = None
    ):
        """Update phase status for progress tracking with detailed live updates"""
        from datetime import datetime

        # Find or create phase in results
        if "phases" not in self.results:
            self.results["phases"] = []

        phase = next((p for p in self.results["phases"] if p["name"] == phase_name), None)
        if not phase:
            phase = {
                "name": phase_name,
                "status": status,
                "progress": progress,
                "start_time": None,
                "end_time": None,
                "details": details or {},
            }
            self.results["phases"].append(phase)
        else:
            phase["status"] = status
            phase["progress"] = progress
            if details:
                phase["details"].update(details)

        # Update timing
        if status == "running" and not phase["start_time"]:
            phase["start_time"] = datetime.now().isoformat()
        elif status in ["completed", "error"] and not phase["end_time"]:
            phase["end_time"] = datetime.now().isoformat()

        # Update overall progress
        if self.results["phases"]:
            total_progress = sum(p["progress"] for p in self.results["phases"])
            self.results["overall_progress"] = total_progress // len(self.results["phases"])

        # Update current phase
        if status == "running":
            self.results["current_phase"] = phase_name

        # Log progress for debugging
        if details and "current_file" in details:
            logger.info(f"📁 {phase_name}: {details.get('current_file', '')} ({progress}%)")
        elif details and "files_analyzed" in details:
            logger.info(
                f"📊 {phase_name}: {details.get('files_analyzed', 0)}/{details.get('total_files', 0)} files ({progress}%)"
            )

    def get_status(self) -> Dict[str, Any]:
        """Get workflow status"""
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "steps": [{"name": s["name"], "status": s["status"]} for s in self.steps],
            "results": self.results,
        }
