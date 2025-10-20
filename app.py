"""
KI-Projektmanagement-System - Main Application
Refactored to use lifecycle and dependencies modules
"""

import logging
from pathlib import Path
from typing import Any, Dict

import uvicorn
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app_dependencies import (
    get_agent_generator,
    get_agent_orchestrator,
    get_analysis_results,
    get_current_project,
    get_loaded_modules,
    get_project_analyzer,
    get_workflow_generator,
    get_workflow_orchestrator,
    register_module,
    set_analysis_results,
    set_current_project,
)
from app_lifecycle import get_project_manager_agent, initialize_components, shutdown_components
from optimization.optimization_engine import OptimizationEngine
from output.artifact_generator import ArtifactGenerator
from output.report_generator import ReportGenerator
from settings import Settings

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="KI-Projektmanagement-System",
    description="Ein intelligentes KI-Projektmanagement-System mit automatischer Projekt-Analyse",
    version="2.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize settings
settings = Settings()


# ============================================================================
# LIFECYCLE EVENTS
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    await initialize_components()
    logger.info("🚀 KI-Projektmanagement-System started")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await shutdown_components()
    logger.info("👋 KI-Projektmanagement-System stopped")


# ============================================================================
# CORE ENDPOINTS
# ============================================================================


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "KI-Projektmanagement-System",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "status": "/status",
            "analyze": "/analyze-project",
            "chat": "/chat",
            "models": "/models",
            "workflows": "/workflow-status",
        },
    }


@app.get("/status")
async def get_status():
    """Get system status"""
    try:
        agent = await get_project_manager_agent()
        agent_status = await agent.get_status()

        return {
            "status": "healthy",
            "current_project": get_current_project(),
            "analysis_available": bool(get_analysis_results()),
            "agent_status": agent_status,
            "loaded_modules": {k: len(v) for k, v in get_loaded_modules().items()},
        }
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ANALYSIS ENDPOINTS
# ============================================================================


@app.post("/analyze-project")
async def analyze_project(request: Dict[str, Any], background_tasks: BackgroundTasks):
    """Start project analysis"""
    try:
        project_path = request.get("project_path")
        if not project_path:
            raise HTTPException(status_code=400, detail="project_path required")

        if not Path(project_path).exists():
            raise HTTPException(status_code=404, detail="Project path not found")

        set_current_project(project_path)

        # Run analysis in background
        analyzer = await get_project_analyzer()
        background_tasks.add_task(_run_analysis, analyzer, project_path)

        return {
            "status": "started",
            "message": "Project analysis started",
            "project_path": project_path,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def _run_analysis(analyzer, project_path: str):
    """Background task for project analysis"""
    try:
        results = await analyzer.analyze_project(project_path)
        set_analysis_results(results)

        # Set project context for agent
        agent = await get_project_manager_agent()
        await agent.set_project_context(results)

        logger.info(f"✅ Analysis completed for {project_path}")
    except Exception as e:
        logger.error(f"❌ Error during analysis: {e}")


@app.get("/analysis-results")
async def get_analysis():
    """Get analysis results"""
    results = get_analysis_results()
    if not results:
        raise HTTPException(status_code=404, detail="No analysis results available")
    return results


# ============================================================================
# CHAT ENDPOINTS
# ============================================================================


@app.post("/chat")
async def chat_with_agent(message: str, context: Dict[str, Any] = None):
    """Chat with AI project manager"""
    try:
        if not message:
            raise HTTPException(status_code=400, detail="message required")

        agent = await get_project_manager_agent()
        response = await agent.chat(message, context)

        return {"status": "success", "response": response, "message": message}
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# AGENT & WORKFLOW ENDPOINTS
# ============================================================================


@app.post("/generate-agents")
async def generate_agents():
    """Generate agents from analysis"""
    try:
        results = get_analysis_results()
        if not results:
            raise HTTPException(status_code=404, detail="No analysis results")

        generator = await get_agent_generator()
        agents = await generator.generate_agents_for_project(results)

        return {"status": "success", "agents_generated": len(agents), "agents": agents}
    except Exception as e:
        logger.error(f"Error generating agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agent-status")
async def get_agent_status():
    """Get status of all agents"""
    try:
        orchestrator = await get_agent_orchestrator()
        return await orchestrator.get_all_agent_status()
    except Exception as e:
        logger.error(f"Error getting agent status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflow-status")
async def get_workflow_status():
    """Get status of all workflows"""
    try:
        orchestrator = await get_workflow_orchestrator()
        return orchestrator.get_workflow_status()
    except Exception as e:
        logger.error(f"Error getting workflow status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/optimizations")
async def get_optimization_suggestions():
    """Get prioritized optimization suggestions"""
    try:
        results = get_analysis_results()
        if not results:
            raise HTTPException(status_code=404, detail="No analysis results available")

        agent = await get_project_manager_agent()
        optimizations = await agent.suggest_optimizations()

        return {"status": "success", "optimizations": optimizations, "count": len(optimizations)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting optimizations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# MODEL ENDPOINTS
# ============================================================================


@app.get("/models")
async def get_available_models():
    """Get available LLM models"""
    try:
        from app_lifecycle import model_manager

        return model_manager.get_available_models()
    except Exception as e:
        logger.error(f"Error getting models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/set-model")
async def set_active_model(model_name: str, model_type: str = "openai"):
    """Set active LLM model"""
    try:
        from app_lifecycle import model_manager

        await model_manager.set_model(model_name, model_type)

        return {"status": "success", "model": model_name, "type": model_type}
    except Exception as e:
        logger.error(f"Error setting model: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
