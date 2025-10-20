"""
Workflow Coordinator - Coordinates workflow generation and execution
Implements Coordinator pattern for workflows
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class WorkflowCoordinator:
    """Coordinates workflow generation and execution using composition"""

    def __init__(self, workflow_generator, workflow_orchestrator):
        # Composition over inheritance - inject dependencies
        self.workflow_generator = workflow_generator
        self.workflow_orchestrator = workflow_orchestrator

        self.active_workflows = {}
        self.workflow_history = []

    async def generate_and_execute_workflows(
        self,
        analysis_results: Dict[str, Any],
        workflow_types: List[str] = None,
        progress_callback=None,
    ) -> Dict[str, Any]:
        """Generate and execute workflows for a project"""
        results = {
            "workflows_generated": [],
            "workflows_executed": [],
            "failed_workflows": [],
            "execution_time": 0,
        }

        try:
            start_time = datetime.now()

            # Phase 1: Generate workflows
            if progress_callback:
                progress_callback("Generating workflows", 0.0)

            generated = await self.workflow_generator.generate_workflows_for_project(
                analysis_results
            )

            results["workflows_generated"] = list(generated.keys())

            # Phase 2: Execute workflows
            if progress_callback:
                progress_callback("Executing workflows", 0.5)

            for workflow_type, workflow_data in generated.items():
                if workflow_types and workflow_type not in workflow_types:
                    continue

                try:
                    # Register and execute workflow
                    workflow_id = f"{workflow_type}_{len(self.active_workflows)}"
                    self.active_workflows[workflow_id] = {
                        "type": workflow_type,
                        "status": "running",
                        "data": workflow_data,
                    }

                    # Execute via orchestrator
                    execution_result = await self.workflow_orchestrator.execute_workflow(
                        workflow_type, analysis_results
                    )

                    results["workflows_executed"].append(workflow_type)
                    self.active_workflows[workflow_id]["status"] = "completed"

                except Exception as e:
                    logger.error(f"Failed to execute workflow {workflow_type}: {e}")
                    results["failed_workflows"].append({"type": workflow_type, "error": str(e)})
                    self.active_workflows[workflow_id]["status"] = "failed"

            end_time = datetime.now()
            results["execution_time"] = (end_time - start_time).total_seconds()

            # Record in history
            self.workflow_history.append(
                {
                    "timestamp": start_time.isoformat(),
                    "generated": len(results["workflows_generated"]),
                    "executed": len(results["workflows_executed"]),
                    "failed": len(results["failed_workflows"]),
                }
            )

            if progress_callback:
                progress_callback("Workflows complete", 1.0)

            logger.info(
                f"Workflow coordination complete: {len(results['workflows_executed'])} executed, "
                f"{len(results['failed_workflows'])} failed"
            )

        except Exception as e:
            logger.error(f"Error coordinating workflows: {e}")
            raise

        return results

    async def get_workflow_status(self, workflow_id: str = None) -> Dict[str, Any]:
        """Get status of workflows"""
        if workflow_id:
            return self.active_workflows.get(workflow_id, {})
        else:
            return {"active_count": len(self.active_workflows), "workflows": self.active_workflows}

    def get_workflow_history(self) -> List[Dict[str, Any]]:
        """Get workflow history"""
        return self.workflow_history
