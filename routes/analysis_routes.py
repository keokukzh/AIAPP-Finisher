"""
Analysis Routes for KI-Projektmanagement-System
Handles project analysis, results, reports, and artifacts endpoints
"""

import logging
import os
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/analysis", tags=["analysis"])

# Global state will be updated by the analysis workflow
_stored_analysis_results = None
_stored_current_project = None


class ProjectAnalysisRequest(BaseModel):
    """Request model for project analysis.

    Attributes:
        project_path: Absolute or relative path to the project to analyze.
    """

    project_path: str


@router.post("/analyze")
async def analyze_project(
    request: ProjectAnalysisRequest,
    workflow_orchestrator,
    ensure_components_initialized,
    global_analysis_results_setter=None,  # Optional callback to update app.py globals
    global_current_project_setter=None,
):
    """Starts a project analysis workflow"""
    try:
        import asyncio

        project_path = request.project_path
        if not project_path:
            raise HTTPException(status_code=400, detail="project_path is required")

        if not os.path.exists(project_path):
            raise HTTPException(status_code=404, detail="Project path not found")

        # Ensure components are initialized
        await ensure_components_initialized()

        # Generate workflow_id
        workflow_id = f"project_analysis_{len(workflow_orchestrator.workflow_history)}"

        # Start workflow asynchronously
        async def run_analysis_and_store():
            global _stored_analysis_results, _stored_current_project
            try:
                logger.info(f"🔄 Starting analysis for: {project_path}")
                result = await workflow_orchestrator.execute_workflow(
                    "simple_analysis", {"project_path": project_path}
                )

                # 🐛 FIX: Store the results in module-level variables
                _stored_analysis_results = result.get("analysis", result)
                _stored_current_project = project_path

                # Also update app.py globals if setter provided
                if global_analysis_results_setter:
                    global_analysis_results_setter(_stored_analysis_results)
                if global_current_project_setter:
                    global_current_project_setter(project_path)

                logger.info(f"✅ Analysis completed and stored for {project_path}")
                keys = list(_stored_analysis_results.keys()) if _stored_analysis_results else "None"
                logger.info(f"   Results keys: {keys}")

                # 🤖 Automatically generate optimizations with urgency scoring
                try:
                    # Use the global model_manager (already initialized)
                    # We need to get it from app.py's globals
                    import sys

                    from optimization.optimization_engine import OptimizationEngine

                    app_module = sys.modules.get("app")
                    if app_module and hasattr(app_module, "model_manager"):
                        model_mgr = app_module.model_manager
                    else:
                        model_mgr = None

                    opt_engine = OptimizationEngine(model_manager=model_mgr)
                    logger.info("🤖 Generating AI optimizations...")
                    opt_results = await opt_engine.analyze_with_urgency(_stored_analysis_results)
                    _stored_analysis_results["optimizations"] = opt_results
                    logger.info(f"✅ Generated {len(opt_results)} prioritized suggestions")
                except Exception as opt_error:
                    logger.warning(f"⚠️ Optimization generation failed (non-critical): {opt_error}")

                # 💾 Save to MongoDB
                try:
                    from database.mongo_client import get_mongo_client

                    mongo = get_mongo_client()
                    project_id = await mongo.save_analysis(
                        project_path=project_path,
                        results=_stored_analysis_results,
                        status="completed",
                    )
                    if project_id:
                        logger.info(f"💾 Saved to MongoDB: {project_id}")
                except Exception as mongo_error:
                    logger.warning(f"⚠️ MongoDB save failed (non-critical): {mongo_error}")

                return result
            except Exception as e:
                logger.error(f"❌ Error in analysis workflow: {e}", exc_info=True)
                raise

        asyncio.create_task(run_analysis_and_store())

        return {
            "status": "started",
            "workflow_id": workflow_id,
            "project_path": project_path,
            "message": "Analyse gestartet - check /api/analysis/results in 30-60 seconds",
        }
    except Exception as e:
        logger.error(f"❌ Error starting project analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results")
async def get_analysis_results():
    """Return the latest analysis results from in-memory cache."""

    if _stored_analysis_results is None:
        raise HTTPException(
            status_code=404,
            detail="No analysis results available. Run /api/analysis/analyze first.",
        )

    return {
        "project_path": _stored_current_project,
        "results": _stored_analysis_results,
        "status": "completed",
    }


@router.get("/reports")
async def list_reports():
    """List generated analysis reports in analysis_output directory."""
    try:
        reports_dir = Path("analysis_output")
        if not reports_dir.exists():
            return {"reports": []}

        reports = []
        for file_path in reports_dir.glob("*.md"):
            reports.append(
                {
                    "name": file_path.name,
                    "path": str(file_path),
                    "size": file_path.stat().st_size,
                    "modified": file_path.stat().st_mtime,
                }
            )

        return {"reports": reports}
    except Exception as e:
        logger.error(f"❌ Error listing reports: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/artifacts")
async def list_artifacts():
    """List generated artifacts under output/artifacts recursively."""
    try:
        artifacts_dir = Path("output/artifacts")
        if not artifacts_dir.exists():
            return {"artifacts": []}

        artifacts = []
        for file_path in artifacts_dir.rglob("*"):
            if file_path.is_file():
                artifacts.append(
                    {
                        "name": file_path.name,
                        "path": str(file_path),
                        "size": file_path.stat().st_size,
                        "modified": file_path.stat().st_mtime,
                    }
                )

        return {"artifacts": artifacts}
    except Exception as e:
        logger.error(f"❌ Error listing artifacts: {e}")
        raise HTTPException(status_code=500, detail=str(e))
