"""
Workflow Routes for KI-Projektmanagement-System
Handles workflow execution, status, and progress tracking
"""

import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/workflows", tags=["workflows"])


class WorkflowExecutionRequest(BaseModel):
    """Request model for workflow execution"""

    workflow_type: str
    parameters: Dict[str, Any] = {}


@router.post("/execute/{workflow_type}")
async def execute_workflow(workflow_type: str, parameters: Dict[str, Any], workflow_orchestrator):
    """Executes a specific workflow"""
    try:
        result = await workflow_orchestrator.execute_workflow(workflow_type, parameters)

        return {"status": "completed", "workflow_type": workflow_type, "result": result}

    except Exception as e:
        logger.error(f"❌ Error executing workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/run-complete")
async def run_complete_workflow(project_path: str, workflow_orchestrator):
    """Runs the complete analysis + generation workflow"""
    try:
        # Execute analysis workflow
        analysis_result = await workflow_orchestrator.execute_workflow(
            "project_analysis", {"project_path": project_path}
        )

        # Execute agent generation workflow
        generation_result = await workflow_orchestrator.execute_workflow(
            "agent_generation", {"analysis_results": analysis_result}
        )

        return {"status": "completed", "analysis": analysis_result, "generation": generation_result}

    except Exception as e:
        logger.error(f"❌ Error in complete workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_workflow_status(workflow_orchestrator):
    """Returns the status of all workflows"""
    try:
        running = workflow_orchestrator.running_workflows
        history = workflow_orchestrator.workflow_history

        return {
            "running_workflows": len(running),
            "total_workflows": len(history),
            "workflows": {
                "running": list(running.keys()),
                "completed": [w["workflow_id"] for w in history],
            },
        }

    except Exception as e:
        logger.error(f"❌ Error getting workflow status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/progress/{workflow_id}")
async def get_workflow_progress(workflow_id: str, workflow_orchestrator):
    """Returns the progress of a specific workflow"""
    try:
        # Check running workflows
        if workflow_id in workflow_orchestrator.running_workflows:
            workflow = workflow_orchestrator.running_workflows[workflow_id]
            return {
                "workflow_id": workflow_id,
                "status": "running",
                "current_phase": workflow.get("current_phase", ""),
                "overall_progress": workflow.get("overall_progress", 0),
                "phases": workflow.get("phases", []),
            }

        # Check completed workflows
        for workflow in workflow_orchestrator.workflow_history:
            if workflow.get("workflow_id") == workflow_id:
                return {
                    "workflow_id": workflow_id,
                    "status": "completed",
                    "result": workflow.get("result"),
                }

        raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting workflow progress: {e}")
        raise HTTPException(status_code=500, detail=str(e))
