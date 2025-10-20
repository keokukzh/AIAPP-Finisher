"""Workflow Orchestrator.

Manages registration, execution, and status tracking for workflows. Provides
helpers for running the full project analysis workflow and querying runtime
status/history.
"""

import logging
from typing import Any, Dict, List, Optional

from workflows.base_workflow import BaseWorkflow
from workflows.project_analysis_workflow import ProjectAnalysisWorkflow
from workflows.simple_analysis_workflow import SimpleAnalysisWorkflow

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """Orchestrates and manages workflows.

    Attributes:
        workflows: Registry mapping workflow names to workflow instances.
        running_workflows: Map of workflow_id to in-progress workflow instances.
        workflow_history: List of recent workflow execution records.
    """

    def __init__(self) -> None:
        self.workflows = {}
        self.running_workflows = {}
        self.workflow_history = []

        # Register default workflows
        self.register_workflow("project_analysis", ProjectAnalysisWorkflow())
        self.register_workflow("simple_analysis", SimpleAnalysisWorkflow())

    def register_workflow(self, name: str, workflow: BaseWorkflow) -> None:
        """Register a workflow.

        Args:
            name: Unique workflow name.
            workflow: Workflow instance implementing execute() and status accessors.
        """
        self.workflows[name] = workflow
        logger.info(f"Registered workflow: {name}")

    async def execute_workflow(
        self, workflow_name: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a workflow by name.

        Args:
            workflow_name: Name of a registered workflow.
            context: Optional execution context dictionary.

        Returns:
            Workflow result dictionary from workflow.execute().
        """
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow '{workflow_name}' not found")

        workflow = self.workflows[workflow_name]
        workflow_id = f"{workflow_name}_{len(self.workflow_history)}"

        try:
            self.running_workflows[workflow_id] = workflow
            logger.info(f"Starting workflow: {workflow_name}")

            result = await workflow.execute(context or {})

            self.workflow_history.append(
                {"id": workflow_id, "name": workflow_name, "status": "completed", "result": result}
            )

            logger.info(f"Completed workflow: {workflow_name}")
            return result

        except Exception as e:
            logger.error(f"Workflow '{workflow_name}' failed: {e}")
            self.workflow_history.append(
                {"id": workflow_id, "name": workflow_name, "status": "failed", "error": str(e)}
            )
            raise
        finally:
            if workflow_id in self.running_workflows:
                del self.running_workflows[workflow_id]

    async def execute_project_analysis(self, project_path: str) -> Dict[str, Any]:
        """Execute the complete project analysis workflow.

        Args:
            project_path: Absolute or relative path to the project root.
        """
        context = {"project_path": project_path}
        return await self.execute_workflow("project_analysis", context)

    def get_workflow_status(self, workflow_id: Optional[str] = None) -> Dict[str, Any]:
        """Get status for a specific workflow or overall orchestrator state.

        Args:
            workflow_id: Optional specific workflow identifier.
        """
        if workflow_id:
            if workflow_id in self.running_workflows:
                return self.running_workflows[workflow_id].get_status()
            else:
                history_item = next(
                    (h for h in self.workflow_history if h["id"] == workflow_id), None
                )
                return history_item or {"error": "Workflow not found"}
        else:
            return {
                "registered_workflows": list(self.workflows.keys()),
                "running_workflows": list(self.running_workflows.keys()),
                "workflow_history": self.workflow_history[-10:],  # Last 10 workflows
            }

    def get_available_workflows(self) -> List[str]:
        """Get list of available workflows."""
        return list(self.workflows.keys())
